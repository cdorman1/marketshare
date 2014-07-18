# -*- coding: utf-8 -*-

import sys
import pyql
import json
import pprint

def web_scraper(symbol):

    sym_vol = [float(item['Volume']) for item in pyql.lookup(symbol)]
    ms = [round(1000000 / i * 100, 2) for i in sym_vol]
    data = {'symbol': [str(item['symbol']) for item in pyql.lookup(symbol)],
            'Avg_Volume(3m)': [str(item['AverageDailyVolume']) for  item in pyql.lookup(symbol)],
            'Volume': sym_vol,
            'EM_Volume': ['1000000'] * len(symbol),
            'Market_Share': map(float, ms)
            }
    headings = ['symbol', 'Avg_Volume(3m)', 'Volume', 'EM_Volume', 'Market_Share']
    columns = [data[heading] for heading in headings]
    max_len = len(max(columns, key=len))
    for col in columns:
        col += [None,] * (max_len - len(col))

    rows = [[col[i] for col in columns] for i in range(max_len)]
    data1 = dict(rows=rows, headings=headings)
    return data1


if __name__ == '__main__':
#    symbol = ['aapl', 'tsla', 'spy']
    web_scraper(symbol)

