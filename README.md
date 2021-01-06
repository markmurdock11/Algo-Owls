# Algo-Owls

## Team Members
Carolina Jonathan Christian Mark

## Project Idea

### Brief Overview: 

We are creating an algorithmic trading bot that uses a supervised machine learning model to analyze Bollinger and Keltner bands in conjunction with slow and fast exponential moving averages to make buy/sell decisions. 

Basically, we want Bot Carolina to beat Normal Carolina. 

### How we are going to do it:

-*Platform of choice*: 

Alpaca, creating a white-labeled bot to trade securities

-*Which tools/libraries we are going to use*: 

Most likely scikit and tensor flow

-*Assumptions we are using*: 

60 minute trading intervals, bollinger/keltner bands (2 standard deviations and 20 periods), exponential moving average (slow=21, fast=9), *(probably) highly liquid securities*, long positions, backdate 1 year and then scale

## Breakdown of Tasks

Carolina: exponential moving averages + keltner channel creation

Jonathan: bollinger band

Christian: metrics/indicators

Mark: Data extraction/cleaning (API pipeline)

Group Work (start by Saturday): Dashboard and machine learning model

