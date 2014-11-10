# -*- coding: utf-8 -*-
from django.http import HttpResponse,Http404
import datetime
from django.shortcuts import render_to_response


def hello(request):
    return HttpResponse("Hello world")


def cur_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>现在时间是 %s.</body></html>" % now
    return HttpResponse(html)


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    #assert Fales
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def template_test(request):
    person_name = 'houlipeng'
    company = 'XY'
    ship_date = datetime.datetime.now()
    item_list = ['itme1' , 'itme2', 'itme3']
    return render_to_response('template-test.html',{'person_name':person_name , 'company':company , 'ship_date':ship_date , 'item_list':item_list})