
import pandas as pd
import numpy as np

# Calculate the Exponential Moving Average (EMA) for a given time period
def calculate_ema(prices, days):
    ema = prices.ewm(span=days, adjust=False).mean()
    return ema

# Calculate the MACD indicator
def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
    short_ema = calculate_ema(prices, short_window)
    long_ema = calculate_ema(prices, long_window)
    macd = short_ema - long_ema
    signal = calculate_ema(macd, signal_window)
    return macd - signal

# Calculate the RSI indicator
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    average_gain = gain.rolling(window=period).mean()
    average_loss = loss.rolling(window=period).mean()
    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate moving averages
def calculate_ma(prices, period):
    return prices.rolling(window=period).mean()

def calculate_obv_grouped(close_prices, volumes):
    # Using change in price to determine the direction of OBV
    price_change = close_prices.diff()
    obv = volumes * np.sign(price_change).fillna(0)
    obv.iloc[0] = 0  # starting value of OBV is 0
    obv = obv.cumsum()  # cumulative sum to get the OBV
    return obv


# Calculate Price Rate of Change
def calculate_roc(prices, period=9):
    roc = prices.diff(periods=period) / prices.shift(periods=period)
    return roc

# Calculate the Stochastic Oscillator
def calculate_stochastic_oscillator(high_prices, low_prices, close_prices, k_period=14, d_period=3):
    low_min = low_prices.rolling(window=k_period).min()
    high_max = high_prices.rolling(window=k_period).max()
    k = ((close_prices - low_min) / (high_max - low_min)) * 100
    d = k.rolling(window=d_period).mean()  # This is the %D line
    return k, d

def calculate_indicators_for_group(df):
    df['MACD'] = calculate_macd(df['close'])
    df['RSI'] = calculate_rsi(df['close'])
    ma_20 = calculate_ma(df['close'], 20)
    ma_10 = calculate_ma(df['close'], 10)
    df['Compare Close MA(20)'] = df['close'] / ma_20
    df['Compare MA(10) MA(20)'] = ma_10 / ma_20
    df['OBV'] = calculate_obv_grouped(df['close'], df['volume'])
    df['Price ROC'] = calculate_roc(df['close'])
    df['Stochastic %K'], df['Stochastic %D'] = calculate_stochastic_oscillator(df['high'], df['low'], df['close'])

    df['market_regime'] = np.select([
        (df['trading_date'] >= '2013-01-01') & (df['trading_date'] < '2016-01-01'),
        (df['trading_date'] >= '2016-01-01') & (df['trading_date'] < '2018-01-01'),
        (df['trading_date'] >= '2018-01-01') & (df['trading_date'] < '2019-01-01'),
        (df['trading_date'] >= '2019-01-01') & (df['trading_date'] < '2020-01-01'),
        (df['trading_date'] >= '2020-01-01') & (df['trading_date'] < '2022-01-01'),
        (df['trading_date'] >= '2022-01-01')
    ], [1, 0, -1, 1, -1, 0], default=np.nan)                                   

    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()

    df['Close_vs_MA20'] = np.where(df['close'] > df['MA20'], 1, 0)
    df['MA10_vs_MA20'] = np.where(df['MA10'] > df['MA20'], 1, 0)

    df['Mean_t0_t5'] = df['close'].rolling(window=6).mean()
    df['Mean_t25_t30'] = df['close'].shift(-25).rolling(window=6).mean()

    df['Max_t0_t25'] = df['close'].shift(1).rolling(window=25, min_periods=1).max()
    df['Pct_Diff'] = (df['close'] / df['Max_t0_t25'] - 1) * 100
    conditions = [
        df['Pct_Diff'] >= 5,  # Chênh lệch >= 10%
        df['Pct_Diff'] < -5  # Chênh lệch <= -10%
    ]
    choices = [1, -1]
    df['Y'] = np.select(conditions, choices)
    # df['Y'] = np.select([df['Pct_Diff'] >= 5, df['Pct_Diff'] < 5],[1,-1])
    
    df.dropna(inplace=True)
    return df
