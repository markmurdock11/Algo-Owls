# **Algo-Owls**
A group project via the Rice University FinTech Bootcamp to demonstrate FinTech Financial Programming.

## Table of contents
* [General Information](#general-information)
* [Summary](#summary)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Installation Guide](#installation-guide)
* [Code Examples](#code-examples)
* [Sources](#sources)
* [Status](#status)
* [Contributors](#contributors)

---

## General Information

Securities trading can be complex for individuals and businesses.  Emotions can run wild and lead to dread, fear, hope, greed and envy, in no specific order.  Trying to control these emotions is a challenge, so this group decide to create the following repository to help us determine a strategy to produce go long signals and targets, test our theories and begin to automate our processes while incorporating some fintech we have learned in our bootcamp.  You will find the repository has the initial workings of an algorithmic trading bot that uses supervised machine learning models incorporating Tensorflow, Keras and Scikit-Learn libraries to analyze Bollinger Bands and Keltner Channels, for a squeeze breakout signal, in conjunction with slow and fast Exponential Moving Averages (EMA), for a directional signal, to make predicted decisions.  In addition to the previous models, an LSTM model to estimate price is also used to predict an entry point for a go long position.

---

## Summary

* The LSTM binary model caused barriers to the Machine Learning
* The two random forest classifiers offered 70% or above accuracy score
* The EMA crossover model needs reconfiguring to increase precision and to improve the precision-recall curve
* The squeeze random forest model was able to anticipate the "squeeze" state with a precision of 64%
* Tests were limited to one asset and one direction (bullish trades), so additional testing with other assets are needed.

---

## Screenshots

* Strategy and Indicators (Bollinger Band Upper and Lower inside Keltner Channel Upper and Lower with EMA crossover in up direction)
![Strategy and Indicators](./Images/strategy_and_indicators.gif)

---

## Technologies

* Python 3.7.7
* See [requirements.txt](./Resources/requirements.txt) for a list of libraries to create an environment.

---

## Installation Guide

1. Download the entire repository
2. Open Git Terminal
3. Navigate into the repository file path where you stored the files during the download.
4. The notebook files should be visible to run.
5. Make sure to create a separate virtual environment for the libraries (algo_owls_env).
6. Use [requirements.txt](requirements.txt) in the repository to install the libraries using the following commands:

    - conda deactivate
    - conda create -n algo_owls_env python=3.7.7
    - conda activate algo_owls_env
    - pip install -r requirements.txt
    - If the previous command has errors try:
        - conda install -r requirements.txt

---

## Code Examples



---

## Sources

- [1] https://rice.bootcampcontent.com/Rice-Coding-Bootcamp/rice-hou-fin-pt-09-2020-u-c/blob/master/class/15-Algorithmic-Trading/3/Activities/01-Ins_Trading_Signal_Features/Solved/trading_signal_features.ipynb

- [2] https://rice.bootcampcontent.com/Rice-Coding-Bootcamp/rice-hou-fin-pt-09-2020-u-c/blob/master/class/15-Algorithmic-Trading/1/Activities/01-Evr_Simple_Trading_Algorithm/Solved/simple_trading_algorithm.ipynb

- [3]

- [4]

- [5]

---

## Status

Project is: _In Progress_

---

## Contributors

* Carolina Benzaquen
* Christian Campbell
* Mark Murdock
* Jonathan Owens
