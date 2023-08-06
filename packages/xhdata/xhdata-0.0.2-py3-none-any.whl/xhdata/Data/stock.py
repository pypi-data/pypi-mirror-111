#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
import pandas as pd
import akshare as ak
from xhdata.Util.MongoClient import *


def stock_zh_a_daily(
        symbol: str = "000001",
        start_date: str = None,
        end_date: str = None,
        adjust: str = None,
        count=None,
        fields=None,
) -> pd.DataFrame:
    """
    获取股票日线数据
    :return: 历史行情
    :rtype: pandas.DataFrame
    """
    try:
        client = MongoClient().client.akshare
        coll = client.stock_day
        condition = {'code': str(symbol)[0:6]}

        if start_date is not None:
            condition['date'] = {"$gte": start_date}
        if end_date is not None:
            condition["date"] = {"$lt": end_date}
        if start_date is not None and end_date is not None:
            condition["date"] = {"$gte": start_date, "$lt": end_date}
            count = None

        res = coll.find(condition)
        if end_date is not None:
            res = res.sort("date", -1)
        if count is not None:
            res = res.limit(int(count))
        df = pd.DataFrame(list(res))
        df.sort_values("date", inplace=True)

        if adjust in ['qfq', 'hfq']:
            qfq = client.stock_fq_factor.find_one({'code': str(symbol)[0:6], 'adjust': adjust}, sort=[('date', -1)])
            if qfq is not None:
                df['open'] = df['open'].map(lambda x: x * float(qfq['factor']))
                df['close'] = df['close'].map(lambda x: x * float(qfq['factor']))
                df['high'] = df['high'].map(lambda x: x * float(qfq['factor']))
                df['low'] = df['low'].map(lambda x: x * float(qfq['factor']))

        return df
    except Exception as err:
        print(err)
