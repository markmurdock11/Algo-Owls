# importing requisite libraries
import requests
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi

def fetch_data(ticker):
    """Function to automatically pull closing price data from Alpaca"""
    """  example syntax: fetch_data(["TSLA"])  """
    
    # Insert Personal Secret Keys (check .ENV to match syntax if error occurs)
    alpaca_api_key = os.getenv("APCA_API_KEY_ID")
    alpaca_secret_key = os.getenv("APCA_API_SECRET_KEY")
    # Create the Alpaca API object
    alpaca = tradeapi.REST(
        alpaca_api_key,
        alpaca_secret_key,
        api_version= "v2")
    
    # Backdating the Data to the first day of 2020
    back_date = pd.Timestamp("2020-01-01", tz="America/New_York").isoformat()

    # Choosing the ticker we want (need to figure out how to make this the input)
    #ticker = ["TSLA"]
    
    # Using our assumption of 15min intervals for trading
    timeframe = "15Min"
    
    # Creating a dataframe with every characteristic of ticker Alpaca allows
    df_ticker = alpaca.get_barset(
        ticker,
        timeframe,
        start=back_date
        ).df
    
    # Selecting only the closing price for the ticker
    closing_price = pd.DataFrame()

    for time_period in ticker:
        closing_price[time_period] = df_ticker[time_period]["close"]

    closing_price.dropna()

    closing_price.rename(columns= {closing_price.columns[0]: "close"}, inplace=True)
    closing_price = pd.DataFrame(closing_price)
    return closing_price

    # Bollinger Band function to capture signal
def bollinger_band_signal_generator(dataframe_name, closing_price_column_name = 'close', bollinger_band_window = 20, num_standard_deviation = 2):
    """Creates Bollinger Band indicator with signal for long position based on closing price
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
            bollinger_band_long (flt): Column of generated signals (1.0 = True, 0.0 = False)
    """
    # Calculate mean and standard deviation
    dataframe_name['bollinger_band_middle'] = dataframe_name[closing_price_column_name].rolling(window=bollinger_band_window).mean()
    dataframe_name['bollinger_band_std'] = dataframe_name[closing_price_column_name].rolling(window=bollinger_band_window).std()

    # Calculate upper bollinger band and lower bollinger band
    dataframe_name['bollinger_band_upper'] = dataframe_name['bollinger_band_middle'] + (dataframe_name['bollinger_band_std'] * num_standard_deviation)
    dataframe_name['bollinger_band_lower'] = dataframe_name['bollinger_band_middle'] - (dataframe_name['bollinger_band_std'] * num_standard_deviation)

    # Create signal column
    dataframe_name['bollinger_band_long'] = np.where(dataframe_name[closing_price_column_name] > dataframe_name['bollinger_band_upper'], 1.0, 0.0)
    
    # Drop NaN values
    dataframe_name.dropna(inplace=True)

    # Return dataframe with features and target
    return dataframe_name

def keltner_channel():
    return True

def x_mov_crossover():
    return True

def signal_generator(bollinger, keltner, crossover):
    return True

def trade_strategy_modeling(all_signals):
    return True

def execute_backtest(trade_strategy):
    return True

def create_dash(metrics_from_backtest):
    return True

def main(connector):
    return True
