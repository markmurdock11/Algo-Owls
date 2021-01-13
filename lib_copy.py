# importing requisite libraries
from stockstats import StockDataFrame as sdf
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
from pathlib import Path




def fetch_ohlcv(ticker, start_date= "2020-01-01", end_date = "2021-01-01"):
    """Function to automatically pull closing price data from Alpaca"""
    """  example syntax: get_dat_data("TSLA")  """
    
    # Insert Personal Secret Keys (check .ENV to match syntax if error occurs)
    alpaca_api_key = os.getenv("APCA_API_KEY_ID")
    alpaca_secret_key = os.getenv("APCA_API_SECRET_KEY")
    # Create the Alpaca API object
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version= "v2")
    
    # Backdating the Data to the first day of 2020
    back_date = pd.Timestamp(start_date, tz="America/New_York").isoformat()
    end_date = pd.Timestamp(end_date, tz="America/New_York").isoformat()

    # Choosing the ticker we want (need to figure out how to make this the input)
    #ticker = ["TSLA"]
    
    # Using our assumption of 15min intervals for trading
    timeframe = "15Min"
    
    # Creating a dataframe with every characteristic of ticker Alpaca allows
    df_ticker = alpaca.get_barset(
        ticker,
        timeframe,
        start=back_date,
        end = end_date
        ).df
    
    return df_ticker[ticker]

def bollinger_band_generator(dataframe_name, closing_price_column_name = 'close', bollinger_band_window = 20, num_standard_deviation = 2):
    """Creates Bollinger Band function
    Args:
        dataframe_name (dict): Single security dataframe containing at least closing prices
        closing_price_column_name (str): Name of column in dataframe containing closing prices
        bollinger_band_window (int): Desired timeframe window used for rolling calculations
        num_standard_deviation (int): Desired number of standard deviations to calculate
    Returns:
        A dataframe of:
            original data passed to function,
            bollinger_band_middle (flt): Column of values for middle band,
            bollinger_band_std (flt): Column of values to calculate standard deviation,
            bollinger_band_upper (flt): Column of values for upper band,
            bollinger_band_lower (flt): Column of values for lower band,
    """

    # Calculate mean and standard deviation
    dataframe_name['bollinger_band_middle'] = dataframe_name[closing_price_column_name].rolling(window=bollinger_band_window).mean()
    dataframe_name['bollinger_band_std'] = dataframe_name[closing_price_column_name].rolling(window=bollinger_band_window).std()

    # Calculate upper bollinger band and lower bollinger band
    dataframe_name['bollinger_band_upper'] = dataframe_name['bollinger_band_middle'] + (dataframe_name['bollinger_band_std'] * num_standard_deviation)
    dataframe_name['bollinger_band_lower'] = dataframe_name['bollinger_band_middle'] - (dataframe_name['bollinger_band_std'] * num_standard_deviation)

    # Drop NaN values
    dataframe_name.dropna(inplace=True)

    # Return dataframe with features and target
    return dataframe_name


def keltner_channel(df_ohlc, p_length = 20):
    
    stock = sdf.retype(df_ohlc)
    atr_column = pd.DataFrame(stock['atr'])
    df_final = df_ohlc
    df_final['atr'] = atr_column
    df_final['kcmid'] = df_final['close'].rolling(window=p_length).mean()
    df_final['kcup'] = df_final['kcmid']+df_final['atr']
    df_final['kclo'] = df_final['kcmid']-df_final['atr']
    
    return df_final

def ewma(dataframe_name, closing_price_column_name = 'close', fast_ema = 9, slow_ema = 21):
    # create EMAs columns
    dataframe_name['EMA9'] = dataframe_name[closing_price_column_name].ewm(span=fast_ema, adjust=False).mean()
    dataframe_name['EMA21'] = dataframe_name[closing_price_column_name].ewm(span=slow_ema, adjust=False).mean()

    # Return dataframe with features and target
    return dataframe_name

def adding_boll_kelt_ewma_dataframe(dataframe):
    lib_copy.bollinger_band_generator(dataframe)
    lib_copy.keltner_channel(dataframe)
    lib_copy.ewma(dataframe)

    return dataframe

def signals_generator(dataframe_name):
    """Creates signals for long position
    Args:
        dataframe_name (dict): Dataframe containing indicator data for Bollinger Bands, EWMA, and Keltner Channels
    Returns:
        A dataframe of:
            original data passed to function,
            appended squeeze column signals of type float (1.0 = True, 0.0 = False),
            appended ema crossup column signals of type float (1.0 = True, 0.0 = False),
            appended ema crossdown column signals of type float (-1.0 = True, 0.0 = False)
            appended io_target column signals of type float (2.0 = Buy, -1.0 = Sell)
    """
    
    # Create signal for bollinger band is inside keltner channel
    selection = dataframe_name.loc[((dataframe_name['bollinger_band_upper'] < dataframe_name['kcup']) & (dataframe_name['bollinger_band_lower'] >= dataframe_name['kclo'])), :].index
    dataframe_name['squeeze'] = 0.0
    dataframe_name['squeeze'][selection] = 1

    # Create signal for crossover band (cross in the up direction)
    selection2 = dataframe_name.loc[((dataframe_name['EMA9'] > dataframe_name['EMA21']) & (dataframe_name['EMA9'].shift(1) < dataframe_name['EMA21'].shift(1))), :].index
    dataframe_name['crossup'] = 0.0
    dataframe_name['crossup'][selection2] = 1

    # Create signal for crossover band (cross in the down direction)
    selection3 = dataframe_name.loc[((dataframe_name['EMA9'] < dataframe_name['EMA21']) & (dataframe_name['EMA9'].shift(1) > dataframe_name['EMA21'].shift(1))), :].index
    dataframe_name['crossdown'] = 0.0
    dataframe_name['crossdown'][selection3] = -1

    # Target generation (buy in)
    selection4 = dataframe_name.loc[((dataframe_name['squeeze'] == 1.0) & (dataframe_name['crossup'] == 1.0)), :].index
    dataframe_name['target'] = 0.0
    dataframe_name['target'][selection4] = 1

    # In and Out target generation
    for index, row in dataframe_name.iterrows():
        dataframe_name.loc[index, 'io_target'] = row['squeeze'] + row['crossup'] + row['crossdown']

    # Return dataframe with features and target
    return dataframe_name


def lstm(
    dataframe,
    num_feature_cols = 2, 
    target_name = "target",
    epochs_num = 10,
    unit_number = 30,
    dropout_fraction=.2    
    ):

    """
    Make sure to have target in last column
    """

    X = dataframe.iloc[:, 0:num_feature_cols].values
    
    y = dataframe.iloc[:,-1].values
    
    X, y = np.array(X), np.array(y).reshape(-1,1)

    # Manually splitting the data
    split = int(0.7 * len(X))

    X_train = X[: split]
    X_test = X[split:]

    y_train = y[: split]
    y_test = y[split:]

    # Importing the MinMaxScaler from sklearn
    from sklearn.preprocessing import MinMaxScaler

    # Create a MinMaxScaler object
    scaler = MinMaxScaler()

    # Fit the MinMaxScaler object with the features data X
    scaler.fit(X)

    # Scale the features training and testing sets
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # Fit the MinMaxScaler object with the target data Y
    scaler.fit(y)

    # Scale the target training and testing sets
    y_train = scaler.transform(y_train)
    y_test = scaler.transform(y_test)

    # Importing required Keras modules
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout

    # Define the LSTM RNN model.
    model = Sequential()

    # Layer 1
    model.add(LSTM(
        units=unit_number,
        return_sequences=True,
        input_shape=(X_train.shape[1], 1))
        )
    model.add(Dropout(dropout_fraction))

    # Layer 2
    model.add(LSTM(units=number_units, return_sequences=True))
    model.add(Dropout(dropout_fraction))

    # Layer 3
    model.add(LSTM(units=number_units))
    model.add(Dropout(dropout_fraction))

    # Output layer
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer="adam", loss="mean_squared_error")

    # Train the model
    model.fit(X_train, y_train, epochs= epechs_num, shuffle=False, batch_size=90, verbose=1)

    # Make predictions using the testing data X_test
    predicted = model.predict(X_test)

    # Recover the original prices instead of the scaled version
    predicted_prices = scaler.inverse_transform(predicted)
    real_prices = scaler.inverse_transform(y_test.reshape(-1, 1))
    # Create a DataFrame of Real and Predicted values
    comparison = pd.DataFrame({
        "Actual Target": real_prices.ravel(),
        "Predicted Target": predicted_prices.ravel()
    }, index = dataframe.index[-len(real_prices): ]) 

    return model.summary(), model.evaluate(X_test, y_test, verbose=0), comparison.plot()
    
def trade_strategy_modeling(all_signals):
    return True

def execute_backtest(trade_strategy):
    return True

def create_dash(metrics_from_backtest):
    return True

def main(connector):
    return True
