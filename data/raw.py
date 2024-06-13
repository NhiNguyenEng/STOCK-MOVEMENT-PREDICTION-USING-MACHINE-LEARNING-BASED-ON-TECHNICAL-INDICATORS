import pandas as pd
import numpy as np
import sys
import os

# Thêm đường dẫn thư mục gốc của dự án vào PYTHONPATH
project_path = '/Users/nhinguyen/Documents/KLTN/STOCK-MOVEMENT-PREDICTION-USING-MACHINE-LEARNING-BASED-ON-TECHNICAL-INDICATORS'
if project_path not in sys.path:
    sys.path.append(project_path)

stocks = pd.read_csv(os.path.join(project_path, 'data/bid_ohlc.csv'))
stocks = stocks[stocks['trading_date'] >= '2014-01-01']
stocks = stocks.sort_values(['trading_date'])


fundamental_metrics = pd.read_csv(os.path.join(project_path, 'data/bid_fa.csv'))