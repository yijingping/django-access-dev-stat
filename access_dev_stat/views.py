# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import simplejson
from datetime import date, timedelta
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse
from redis_cache import get_redis_connection


def index(request):
    context = {} 
    return render_to_response('access_dev_stat/index.html', context)

def alive(request):
    days,day_open,day_alive = [],[],[]
    today = date.today()
    for dt in reversed(range(20)):
        cur_day = today - timedelta(days=dt)
        days.append(cur_day.strftime('%m-%d'))

        day_str = cur_day.strftime('%Y-%m-%d')
        day_open.append(get_open_devs(day_str))
        day_alive.append(get_alive_devs(day_str))

    res = {
        'days': days,
        'day_open': day_open,
        'day_alive': day_alive
    }
    return HttpResponse(simplejson.dumps(res), mimetype="application/json; charset=utf-8")

'''
platforms = ['android', 'iPhone']
versions = ['2.5.2', '2.5.1', '2.5', '2.4.6', '2.4.3', '2.4.2', '2.4.1', '2.4', '2.3.1', '2.3', '2.2'
            , '2.1.5', '2.1.4', '2.1.2', '2.1.1', '2.1', '2.0.2', '2.0.1']
channels = ['daoyoudao2',]
'''

def get_alive_devs(day_str):
    conn = get_redis_connection(settings.ACCESS_DEV_STAT_CACHE_REDIS_KEY)
    keys = []
    for item in settings.ACCESS_DEV_STAT_INCLUDE_VIEWS: 
        keys.extend(conn.keys('%s:*:%s' % (day_str, item)))

    if keys: 
        res = conn.sunion(keys)
        return len(res)
    else:
        return 0

def get_open_devs(day_str):
    conn = get_redis_connection(settings.ACCESS_DEV_STAT_CACHE_REDIS_KEY)
    keys = []
    for item in settings.ACCESS_DEV_STAT_INCLUDE_VIEWS[1:]: 
        keys.extend(conn.keys('%s:*:%s' % (day_str, item)))

    if keys: 
        res = conn.sunion(keys)
        return len(res)
    else:
        return 0
