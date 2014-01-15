'''
access device statistics middleware 
'''

from __future__ import unicode_literals
from datetime import date
from django.conf import settings
from redis_cache import get_redis_connection

class AccessDevStatMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not settings.ACCESS_DEV_STAT:
            return None

        today = date.today()
        dr = settings.ACCESS_DEV_STAT_DATE_RANGE
        if not (dr[0] <= today <= dr[1]):
            return None

        fn = view_func.func_name
        if fn in settings.ACCESS_DEV_STAT_EXCLUDE_VIEWS:
            return None

        inc = settings.ACCESS_DEV_STAT_INCLUDE_VIEWS
        if inc and fn not in inc: 
            return None

        data = self.get_agent_info(request, view_func) 
        if settings.ACCESS_DEV_STAT_LOG_TO_FILE:
            self._log_to_file(data)

        if settings.ACCESS_DEV_STAT_LOG_TO_REDIS:
            self._log_to_redis(data)
              
    def get_agent_info(self, request, view_func):
        date_str = date.today().strftime('%Y-%m-%d')
        platform = request.COOKIES.get(settings.PLATFORM_COOKIE_NAME, '')
        version = request.COOKIES.get(settings.VERSION_COOKIE_NAME, '')
        channel = request.COOKIES.get(settings.CHANNEL_COOKIE_NAME, '')
        fn = view_func.func_name

        device = request.COOKIES.get(settings.DEVICE_COOKIE_NAME, '')

        key = '%s:%s:%s:%s:%s' % (date_str, platform, version, channel, fn) 
        res = {key: device}
        return res
        
    def _log_to_file(self, data):
        pass
 
    def _log_to_redis(self, data):
        conn = get_redis_connection(settings.ACCESS_DEV_STAT_CACHE_REDIS_KEY)
        for k,v in data.iteritems():
            conn.sadd(k,v)
