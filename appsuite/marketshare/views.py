# -*- coding: utf-8 -*-
from marketshare.ms import web_scraper

from django.http import HttpResponse
from django.template import loader,RequestContext
 

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
