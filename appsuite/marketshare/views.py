# -*- coding: utf-8 -*-
from marketshare.ms import web_scraper
from marketshare.models import SymbolList
from django.http import HttpResponse
from django.template import loader,RequestContext
from django import forms
from django.shortcuts import redirect

class LoginForm(forms.Form):
    username=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput())


def index(request):

    if request.method == "POST":
        form=LoginForm(request.POST)
        print "received POST"
        if form.is_valid:
            print "FORM is valid"
            return redirect("dashboard")
        else:
            print "FORM is not valid"
            template=loader.get_template("index.html")
            rc=RequestContext(request, {'username': 'Chris Dorman', 'form':form} )
            return HttpResponse(template.render(rc))
    else:
        template=loader.get_template("index.html")
        rc=RequestContext(request, {'username': 'Chris Dorman', 'form':LoginForm()} )
        return HttpResponse(template.render(rc)) 


def dashboard(request):
    template=loader.get_template("dashboard.html")
    rc=RequestContext(request, {})
    return HttpResponse(template.render(rc)) 


def listpage(request):
    symbol = 'spy'
    print symbol
    data = web_scraper(symbol)
    print data
    template=loader.get_template("marketshare.html")
    rc=RequestContext(request, {"data": data})
    return HttpResponse(template.render(rc))


if __name__ == '__main__':
    index(request)
