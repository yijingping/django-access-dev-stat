# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import simplejson
from datetime import date, timedelta
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse
from redis_cache import get_redis_connection

platforms = ['android', 'iPhone']
versions = ['2.5.2', '2.5.1', '2.5', '2.4.6', '2.4.3', '2.4.2', '2.4.1', '2.4', '2.3.1', '2.3', '2.2'
            , '2.1.5', '2.1.4', '2.1.2', '2.1.1', '2.1', '2.0.2', '2.0.1']
channels = ['m99fang', 'baidu', '360', 'daoyoudao2', 'hiapk', '99fang', 'goapk', 'tengxun', '']

def index(request):
    t = request.GET.get('t', 'app_alive') 
    context = {} 
    return render_to_response('access_dev_stat/%s.html' % t, context)

def app_alive(request):
    platform = request.GET.get('platform') 
    days,day_open,day_alive = [],[],[]
    today = date.today()
    for dt in reversed(range(14)):
        cur_day = today - timedelta(days=dt)
        days.append(cur_day.strftime('%m-%d'))

        day_str = cur_day.strftime('%Y-%m-%d')
        day_open.append(get_open_devs(day_str, platform))
        day_alive.append(get_alive_devs(day_str, platform))

    res = {
        'days': days,
        'day_open': day_open,
        'day_alive': day_alive,
        'platform': platform
    }
    return HttpResponse(simplejson.dumps(res), mimetype="application/json; charset=utf-8")

def get_alive_devs(day_str, platform):
    conn = get_redis_connection(settings.ACCESS_DEV_STAT_CACHE_REDIS_KEY)
    keys = []
    for item in settings.ACCESS_DEV_STAT_INCLUDE_VIEWS: 
        keys.extend(conn.keys('%s:%s:*:%s' % (day_str, platform, item)))

    if keys: 
        res = conn.sunion(keys)
        return len(res)
    else:
        return 0

def get_open_devs(day_str, platform):
    conn = get_redis_connection(settings.ACCESS_DEV_STAT_CACHE_REDIS_KEY)
    keys = []
    for item in settings.ACCESS_DEV_STAT_INCLUDE_VIEWS[1:]: 
        keys.extend(conn.keys('%s:%s:*:%s' % (day_str, platform, item)))

    if keys: 
        res = conn.sunion(keys)
        return len(res)
    else:
        return 0

def app_platform(request):
    dates,android,iphone,other= [],[],[],[]
    today = date.today()
    for dt in reversed(range(14)):
        cur_day = today - timedelta(days=dt)
        dates.append(cur_day.strftime('%m-%d'))

        day_str = cur_day.strftime('%Y-%m-%d')
        and_count = get_platform_devs(day_str, 'android')
        iph_count = get_platform_devs(day_str, 'iPhone')
        oth_count = get_platform_devs(day_str, '*') - and_count - iph_count
        android.append(and_count )
        iphone.append(iph_count)
        other.append(oth_count)

    res = {
        'dates': dates,
        'android': android, 
        'iphone': iphone,
        'other': other
    }
    return HttpResponse(simplejson.dumps(res), mimetype="application/json; charset=utf-8")

def get_platform_devs(day_str, platform):
    conn = get_redis_connection(settings.ACCESS_DEV_STAT_CACHE_REDIS_KEY)
    keys = []
    for item in settings.ACCESS_DEV_STAT_INCLUDE_VIEWS[1:]: 
        keys.extend(conn.keys('%s:%s:*:*:%s' % (day_str, platform, item)))

    print keys
    if keys: 
        res = conn.sunion(keys)
        return len(res)
    else:
        return 0

def app_channel(request):
    platform = request.GET.get('platform') 
    dates,stats= [],[]
    length = 14 

    pchannels = {'android':channels, 'iPhone':['']}.get(platform)
    for idx,ch in enumerate(pchannels):
        stats.append({
                'name': ch,
                'data': [0] * length,
                'visible': False if idx > 4 else True,
                'marker': {
                    'symbol': 'circle',
                    'fillColor': 'white',
                    'lineColor': None,
                    'lineWidth': 2
                    }
        })

    # 其它
    stats.append({
        'name': '*',
        'data': [0] * length,
        'visible': False,
        'marker': {
            'symbol': 'circle',
            'fillColor': 'white',
            'lineColor': None,
            'lineWidth': 2
        }
    })

    today = date.today()
    for dt in reversed(range(length)):
        cur_day = today - timedelta(days=dt)
        dates.append(cur_day.strftime('%m-%d'))

        day_str = cur_day.strftime('%Y-%m-%d')
        total = 0
        for item in stats: 
            if item['name'] == '*':
                count = get_channel_devs(day_str, platform, item['name'])
                item['data'][length - dt - 1 ] = count - total
            else:
                count = get_channel_devs(day_str, platform, item['name'])
                total += count
                item['data'][length - dt - 1 ] = count
                

    stats[-2]['name'] = '空'
    stats[-1]['name'] = '其它'
    res = {
        'dates': dates,
        'stats': stats,
        'platform': platform
    }
    return HttpResponse(simplejson.dumps(res), mimetype="application/json; charset=utf-8")

def get_channel_devs(day_str, platform, channel):
    conn = get_redis_connection(settings.ACCESS_DEV_STAT_CACHE_REDIS_KEY)
    keys = []
    for item in settings.ACCESS_DEV_STAT_INCLUDE_VIEWS[1:]: 
        keys.extend(conn.keys('%s:%s:*:%s:%s' % (day_str, platform, channel, item)))

    if keys: 
        res = conn.sunion(keys)
        return len(res)
    else:
        return 0

def app_version(request):
    platform = request.GET.get('platform') 
    dates,stats= [],[]
    length = 14 

    for idx,ver in enumerate(versions):
        stats.append({
                'name': ver,
                'data': [0] * length,
                'visible': False if idx > 3 else True,
                'marker': {
                    'symbol': 'circle',
                    'fillColor': 'white',
                    'lineColor': None,
                    'lineWidth': 2
                    }
        })

    # 其它
    stats.append({
        'name': '*',
        'data': [0] * length,
        'visible': False,
        'marker': {
            'symbol': 'circle',
            'fillColor': 'white',
            'lineColor': None,
            'lineWidth': 2
        }
    })

    today = date.today()
    for dt in reversed(range(length)):
        cur_day = today - timedelta(days=dt)
        dates.append(cur_day.strftime('%m-%d'))

        day_str = cur_day.strftime('%Y-%m-%d')
        total = 0
        for item in stats: 
            if item['name'] == '*':
                count = get_version_devs(day_str, platform, item['name'])
                item['data'][length - dt - 1 ] = count - total
            else:
                count = get_version_devs(day_str, platform, item['name'])
                total += count
                item['data'][length - dt - 1 ] = count
                

    stats[-1]['name'] = '其它'
    res = {
        'dates': dates,
        'stats': stats,
        'platform': platform
    }
    return HttpResponse(simplejson.dumps(res), mimetype="application/json; charset=utf-8")

def get_version_devs(day_str, platform, version):
    conn = get_redis_connection(settings.ACCESS_DEV_STAT_CACHE_REDIS_KEY)
    keys = []
    for item in settings.ACCESS_DEV_STAT_INCLUDE_VIEWS[1:]: 
        keys.extend(conn.keys('%s:%s:%s:*:%s' % (day_str, platform, version, item)))

    if keys: 
        res = conn.sunion(keys)
        return len(res)
    else:
        return 0
