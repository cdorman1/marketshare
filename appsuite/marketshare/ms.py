# -*- coding: utf-8 -*-

import pyql
import sqlalchemy as sa
from sqlalchemy import exc


def pos_query():
    """Function for querying DB and returning results"""

    global result
    db_uri = 'mysql://tclerk:flamengo@cer-emdbl2/'
    engine = sa.create_engine(db_uri)
    engine.begin()
    try:
        connection = engine.connect()
        result = connection.execute("SELECT pm.Symbol, "
                                    "SUM(pm.Buys + pm.Sells) AS EM_Volume "
                                    "FROM history.pos_matrix AS pm "
                                    "WHERE pm.ProdType='Equity' "
                                    "AND pm.TradeDate=CURDATE() "
                                    "GROUP BY pm.Symbol;")

    except exc.SQLAlchemyError.message as sa_msg:
        print sa_msg
        pass

    return result


def web_scraper():

    em_data = pos_query()

    symbol = []
    em_vol = []
    for k in em_data:
        new_d = dict(k)
        symbol.append(new_d['Symbol'])
        em_vol.append(new_d['EM_Volume'])

    sym_vol = [int(item['Volume']) for item in pyql.lookup(symbol[:400])]
    mkt_shr = [round(x / y * 100, 2) for x, y in zip(em_vol[:400], sym_vol)]
    avg_vol = [str(item['AverageDailyVolume']) for item in
               pyql.lookup(symbol[:400])]
    em_vol = [vol for vol in em_vol]
    ms = map(float, mkt_shr)

    data = {'Symbol': symbol,
            'Avg_Volume(3m)': avg_vol,
            'Volume': sym_vol,
            'EM_Volume': em_vol,
            'Market_Share': ms}

    headings = ['Symbol', 'Avg_Volume(3m)', 'Volume',
                'EM_Volume', 'Market_Share']

    columns = [data[heading] for heading in headings]
    max_len = len(max(columns, key=len))

    for col in columns:
        col += [None] * (max_len - len(col))

    rows = [[col[i] for col in columns] for i in range(max_len)]
    data1 = dict(rows=rows, headings=headings)

    print data1
    return data1


def main():

    try:
        web_scraper()
    except Exception as e:
        print "ERROR!!!\n", e


if __name__ == '__main__':
    main()