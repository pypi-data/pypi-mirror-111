# -*- coding:utf-8 -*-
# /usr/bin/env python

#import akshare as ak
#import pandas as pd


#from QUANTAXIS.QAData.data_fq import _QA_data_stock_to_fq

import xhdata as xhdata

import faulthandler

faulthandler.enable()
from dotenv import load_dotenv
load_dotenv(verbose=True)

# 列名与数据对其显示
#pd.set_option('display.unicode.ambiguous_as_wide', True)
#pd.set_option('display.unicode.east_asian_width', True)
# 显示所有列
#pd.set_option('display.max_columns', None)
# 显示所有行
#pd.set_option('display.max_rows', None)


#stock_sse_summary_df = ak.stock_sse_summary()
#print(stock_sse_summary_df)

#stock_szse_summary_df = ak.stock_szse_summary()
#print(stock_szse_summary_df)

#stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
#print(stock_zh_a_spot_em_df)

#stock_zh_a_alerts_cls_df = ak.stock_zh_a_alerts_cls()
#print(stock_zh_a_alerts_cls_df)

#stock_changes_em_df = ak.stock_changes_em(symbol="大笔买入")
#print(stock_changes_em_df)

#stock_a_below_net_asset_statistics_df = ak.stock_a_below_net_asset_statistics(symbol="全部A股")
#print(stock_a_below_net_asset_statistics_df)


#stock_wc_hot_rank_df = ak.stock_wc_hot_rank()
#print(stock_wc_hot_rank_df)


#stock_info_sz_name_code_df = ak.stock_info_sz_name_code(indicator="A股列表")
#print(stock_info_sz_name_code_df)

#stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="603777", start_date="20210601", end_date='20210616')
#stock_zh_a_hist_df['code'] = "603777"
#stock_zh_a_hist_df.columns = ["data", "open", "close", "high", "low", "vol", "amount", "amplitude", "change_pct", "change_amount", "turnover_ratio", "code"]
#print(stock_zh_a_hist_df)


#stock_zh_a_tick_tx_df = ak.stock_zh_a_tick_tx(code="sz000001", trade_date="20210610")
#print(stock_zh_a_tick_tx_df)

#hfq_factor_df = ak.stock_zh_a_daily(symbol="sz000001", adjust="hfq-factor")
#print(hfq_factor_df)



#stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", start_date="20210510", end_date='20210518')
#print(stock_zh_a_hist_df)

#stock_em_fhps_df = ak.stock_em_fhps(date="20201231")
#print(stock_em_fhps_df)


#stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000001", start_date="20210510", end_date="20210518")
#print(stock_zh_a_daily_qfq_df)


#stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sz399552")
#stock_zh_index_daily_df.columns = ["-", "open", "hign", "low", "close", "volume"]
#stock_zh_index_daily_df.reset_index(inplace=True)
#print(stock_zh_index_daily_df)


stock_zh_a_daily_qfq_df = xhdata.stock_zh_a_daily(symbol= "000001",
    start_date= "2021-05-08",
    end_date= "2021-06-01",
	adjust = 'hfq',count=10)
print(stock_zh_a_daily_qfq_df)

