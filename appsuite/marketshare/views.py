# -*- coding: utf-8 -*-
from marketshare.ms import web_scraper
from marketshare.models import GetSymbol
from django.http import HttpResponse
from django.template import loader,RequestContext
from django import forms
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


class LoginForm(forms.Form):
    username=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput())


def dashboard(request):
    template=loader.get_template("dashboard.html")
    rc=RequestContext(request, {})
    return HttpResponse(template.render(rc)) 


def index(request):

    if request.method == "POST":
        form=LoginForm(request.POST)
        print "received POST"
        if form.is_valid():
            print "FORM is valid"
            username, pwd = request.POST.get('username', None),request.POST.get('password', None)
            if not username or not pwd:
                return HttpResponse("username and password not present")
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist, ex:
                print "Creating new user..."
                user = User.objects.create_user(username, username, pwd)
            if user:
                print "Authenticating..."
                user = authenticate(username=username, password=pwd)
                print "Logging in user"
                login(request, user)
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




def listpage(request):
    symbol = 'spy'
    print symbol
    data = web_scraper(symbol)
    print data
    template=loader.get_template("marketshare.html")
    rc=RequestContext(request, {"data": data})
    return HttpResponse(template.render(rc))


def dologout(request):
    logout(request)
    return redirect("index")

if __name__ == '__main__':
    index(request)
