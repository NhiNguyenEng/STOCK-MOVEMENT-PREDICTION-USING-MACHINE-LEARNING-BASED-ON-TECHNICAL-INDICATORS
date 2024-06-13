import pandas as pd
import numpy as np
import sys
import os

# Thêm đường dẫn thư mục gốc của dự án vào PYTHONPATH
project_path = '/Users/nhinguyen/Documents/KLTN/STOCK-MOVEMENT-PREDICTION-USING-MACHINE-LEARNING-BASED-ON-TECHNICAL-INDICATORS'
if project_path not in sys.path:
    sys.path.append(project_path)

fundamental_metrics = pd.read_csv(os.path.join(project_path, 'data/bid_fa.csv'))
fundamental_metrics = fundamental_metrics[['ticker', 'trading_date', 'pb', 'pe', 'roe', 'roa']]
fundamental_metrics = fundamental_metrics[['ticker', 'trading_date', 'pb', 'pe', 'roe', 'roa']]
fundamental_metrics['key'] = fundamental_metrics["ticker"] + fundamental_metrics["trading_date"].dt.strftime("%Y-%m-%d")
ticker = ['BID']
fundamental_metrics = fundamental_metrics[fundamental_metrics['ticker'].isin(ticker)]
fundamental_metrics