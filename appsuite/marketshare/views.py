# -*- coding: utf-8 -*-
from marketshare.ms import web_scraper
from marketshare.models import MarketShare, MsForm
from django.http import HttpResponse
from django.template import loader, RequestContext, Context, Template
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from marketshare.marketshare_forms import LoginForm


@login_required(login_url="marketshare/index/")
def dashboard(request):
    if request.method=="POST":
        d=request.POST.copy()
        d.update({'owner':request.user.id})
        form=MsForm(d)
        if not form.is_valid():
            template=loader.get_template("dashboard.html")
            rc=RequestContext(request,{'form': form})
            return HttpResponse(template.render(rc))
        #save note to the database
        submission=form.save(commit=False)
        submission.owner=request.user
        submission.save()
        return redirect("dashboard")
    else:
        template=loader.get_template("dashboard.html")
        rc=RequestContext(request, {'form': MsForm()})
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
                user = User.objects.get(username__exact=username)
            except ObjectDoesNotExist, ex:
                print "Creating new user..."
                user = User.objects.create_user(username, username, pwd)
            if user:
                print "Authenticating..."
                user = authenticate(username=username, password=pwd)
            print "Logging in user"
            login(request, user)
            return redirect("listpage")
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
    symbol = ['aapl', 'tsla', 'spy', 'qqq', 'dgly', 'atml', 'ibm']
 #   print symbol
    data = web_scraper(symbol)
    print data
    template=loader.get_template("listpage.html")
    rc=RequestContext(request, {"data": data})
    return HttpResponse(template.render(rc))


def dologout(request):
    logout(request)
    return redirect("index")

if __name__ == '__main__':
    index(request)
