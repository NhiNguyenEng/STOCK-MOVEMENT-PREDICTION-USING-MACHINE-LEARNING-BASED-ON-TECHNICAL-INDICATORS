import pandas as pd


def run_backtest(df: pd.DataFrame):
    backtest_pm2 = pd.DataFrame()  # Create an empty DataFrame to store the results

    df['holding_days'] = (df["close_date"] - df["open_date"]).dt.days 
    df = df[df['status'] == "CLOSED"]
    df["pnl"] = (df["close_price"] / df["open_price"] - 1)*100
    df = df[df[['pnl']].notnull().all(1)]
    df['annualize_pnl'] = df['pnl'] / df['holding_days'] * 365    

    win_deal = df[df['pnl'] > 0]
    fail_deal = df[df['pnl'] < 0]
    group_win = win_deal.groupby("ticker")
    group_fail = fail_deal.groupby("ticker")
    
    filtered_group = df.groupby("ticker")
    backtest_pm2['total_deals'] = filtered_group.size()  # Count the total deals for each ticker 
    backtest_pm2['win_rate'] = (group_win.size() / backtest_pm2['total_deals'] ).round(2)
    backtest_pm2['fail_rate'] = (group_fail.size() / backtest_pm2['total_deals']).round(2)

    backtest_pm2['take_profit'] = group_win['pnl'].mean().round(2)
    backtest_pm2['cut_loss'] = group_fail['pnl'].mean().round(2)
    backtest_pm2['holding_avg'] = filtered_group['holding_days'].mean()
    backtest_pm2['holding_med'] = filtered_group['holding_days'].median()
    backtest_pm2['holding_min'] = filtered_group['holding_days'].min()
    backtest_pm2['holding_max'] = filtered_group['holding_days'].max()
    backtest_pm2['start_date'] = filtered_group["open_date"].min()
    backtest_pm2['end_date'] = filtered_group["close_date"].max()
    backtest_pm2['holding_year_avg'] = (backtest_pm2['end_date']- backtest_pm2['start_date']).dt.days / 365
    backtest_pm2['pnl_avg'] = filtered_group['pnl'].mean()
    backtest_pm2['pnl_med'] = filtered_group['pnl'].median()
    backtest_pm2['pnl_min'] = filtered_group['pnl'].min()
    backtest_pm2['pnl_max'] = filtered_group['pnl'].max()
    backtest_pm2['annualized_pnl_avg'] = filtered_group['annualize_pnl'].mean()
    backtest_pm2['annualized_pnl_med'] = filtered_group['annualize_pnl'].median()
    backtest_pm2['annualized_pnl_min'] = filtered_group['annualize_pnl'].min()
    backtest_pm2['annualized_pnl_max'] = filtered_group['annualize_pnl'].max()
    backtest_pm2['avg_deal_per_year'] = backtest_pm2['total_deals'] / backtest_pm2['holding_year_avg']

    return backtest_pm2.reset_index()

