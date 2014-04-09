# -*- coding: utf-8 -*-

import sys
#import MySQLdb
import locale
import lxml.html
from django.http import HttpResponse
from django.template import loader,RequestContext


locale.setlocale(locale.LC_ALL, '')

#NOTE: this script was written in Python 2.7 some of the string formatting
#may not translate when used with older versions 

#Use the code below if the output is something other than UTF-8
"""
import codecs
if sys.stdout.encoding != 'UTF-8':
  sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'strict')
if sys.stderr.encoding != 'UTF-8':
  sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'strict')  
"""  
    
    
def db_con(symbol):
#    
#    
#    db = MySQLdb.connect(host = "cer-emdbl2",
#                         user = "tclerk",
#                         passwd = "flamengo",
#                         db = "history")                 
#    cur = db.cursor()
#    try:
#        cur.execute ("SELECT sum(buys+sells) FROM history.pos_matrix WHERE symbol = \'{0}\' AND tradedate=curdate();".format(symbol)) 
#    except MySQLdb.Error, e:
#        try:
#            print "MySQL Error {0}: {1}".format(e.args[0], e.args[1])
#        except IndexError:
#            print "MySQL Error: {}".format(str(e))
#    
#    row = cur.fetchone()
#    vol = int(row[0])
    vol = 1000000
    return vol
        

def web_scraper(symbol):
    url = ('http://finance.yahoo.com/q?s=' + symbol )
    doc = lxml.html.parse(url)
    #find the first table contaning any tr and a td with class yfnc_tabledata1
    table = doc.xpath("//table[tr/td[@class='yfnc_tabledata1']]")[1]        
    text = []   
    for tr in table.xpath('./tr'):
        text.append(tr.text_content())
    split_txt = [i.split(':') for i in text]
    em_vol =  db_con(symbol) 
    ms = float(em_vol) / int(split_txt[2][1].replace(',', '')) * 100
    sym = "{}".format(str.upper(symbol))
    avg_vol = "{}".format(split_txt[3][1])
    sym_vol = "{}".format(split_txt[2][1])
    em_tvol = "{}".format(locale.format('%d', em_vol, 1))
    market_share = "{0:.2f}%".format(ms)
    return sym, avg_vol, sym_vol, em_tvol, market_share

#def web_scraper():
#    url = ('http://finance.yahoo.com/quotes/AAP,AAPL,ABB,ABX,ACE,ACGL,ACN,ACT')
#    doc = lxml.html.parse(url)
#    for tr in doc.xpath("//table[@class='yfi_portfolios_multiquote sortable yfi_table_row_order']//tr")[0]:
#        print tr.text_content()
  #  body_lst = []
  #  for elem in table.xpath('./tbody'):
  #      body_lst.append(elem.text_content().rstrip(' '))
  #  
  #  print body_lst
    
    

def index(request):
    symbol = 'spy'    
    print symbol
    data = web_scraper(symbol)
    print data
    template=loader.get_template("index.html")
    rc=RequestContext(request, {"data" : data} )
    return HttpResponse(template.render(rc)) 


if __name__ == '__main__':
    index(request)
