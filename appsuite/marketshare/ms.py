# -*- coding: utf-8 -*-

import pyql
import sqlalchemy as sa
from sqlalchemy import exc


def pos_query():
    '''Function for querying DB and returning results'''
    
    DB_URI = 'mysql://tclerk:flamengo@cer-emdbl2/'
    engine = sa.create_engine(DB_URI)
    engine.begin()
    try:
        connection = engine.connect()
        result = connection.execute("SELECT pm.Symbol, "
                                    "SUM(pm.Buys + pm.Sells) AS EM_Volume "
                                    "FROM history.pos_matrix AS pm "
                                    "WHERE pm.ProdType='Equity' "
                                    "AND pm.TradeDate=CURDATE() "
                                    "GROUP BY pm.Symbol;"
                                    )
    except exc.SQLAlchemyError.message as sa_message:
        print sa_message
        pass
        
    return result  
 

def web_scraper():

    data = pos_query()
    symbol = []
    em_vol = []
    for k in data:
        new_d = dict(k)
        symbol.append(new_d['Symbol'])
        em_vol.append(new_d['EM_Volume'])
        
    print symbol[0:200], em_vol[0:200]
        
    sym_vol = [int(item['Volume']) for item in pyql.lookup(symbol[0:200])]
    ms = [round(x / y * 100, 2) for x, y in zip(em_vol[0:200], sym_vol)]
    data = {'Symbol': [str(item['symbol']) for item in pyql.lookup(symbol[0:200])],
            'Avg_Volume(3m)': [str(item['AverageDailyVolume']) for  item in
            pyql.lookup(symbol[0:200])],
            'Volume': sym_vol,
            'EM_Volume': [vol for vol in em_vol[0:200]],
            'Market_Share': map(float, ms)
            }
    print data['Market_Share']
    headings = ['Symbol', 'Avg_Volume(3m)', 'Volume',
                'EM_Volume', 'Market_Share']
    columns = [data[heading] for heading in headings]
    max_len = len(max(columns, key=len))
    for col in columns:
        col += [None,] * (max_len - len(col))

    rows = [[col[i] for col in columns] for i in range(max_len)]
    data1 = dict(rows=rows, headings=headings)
    return data1

def main():
    try:
        web_scraper()
    except Exception as e:
        print "ERROR!!!\n", e
        

if __name__ == '__main__':
    web_scraper()
