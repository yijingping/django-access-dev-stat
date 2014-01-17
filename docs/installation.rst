Installation
============

Getting the code
----------------

The recommended way to install AccessDevStat latest version is via pip_::

    $ pip install -e git+https://github.com/yijingping/django-access-dev-stat#egg=django_access_dev_stat

.. _pip: http://www.pip-installer.org/

Quick Setup
-----------

copy the content of `settings.py.example` to the end of `settings.py`.  

Then check the settings line by line.

Explicit setup
--------------

Caches
~~~~~~~~~~~~~~
make sure your have a redis backend cache::

    CACHES = {                                                                  
        "redis": {                                                              
            "BACKEND": "redis_cache.cache.RedisCache",                          
            "LOCATION": "192.168.10.100:6379:0",                                
            "OPTIONS": {                                                        
                "CLIENT_CLASS": "redis_cache.client.DefaultClient",             
            }                                                                   
        },                                                                      
    }                                                                           
    

Settings
~~~~~~~~~~~~~~
enable this app in you django's `settings.py`::

    ACCESS_DEV_STAT = True
    if ACCESS_DEV_STAT: 
        MIDDLEWARE_CLASSES += (
            'access_dev_stat.middleware.AccessDevStatMiddleware',
        )
        INSTALLED_APPS += ( 'access_dev_stat',)

    # Whether log access record to file, if True, you can use `calc_stat.py` to get you data  
    # But for now, it is not supported. 
    ACCESS_DEV_STAT_LOG_TO_FILE = False
    # Whether log access record to redis
    ACCESS_DEV_STAT_LOG_TO_REDIS = True 
    # set to get redis from cache, default is 'redis'
    ACCESS_DEV_STAT_CACHE_REDIS_KEY = 'redis' 
    
    # cookie name set in every request 
    GUID_COOKIE_NAME = '_guid'
    DEVICE_COOKIE_NAME = '_device'
    PLATFORM_COOKIE_NAME = '_platform'
    CHANNEL_COOKIE_NAME = '_channel'
    VERSION_COOKIE_NAME = '_version'

More Confiure
~~~~~~~~~~~~~~
confiure record date range and record view function in `settings.py`::

    # control available date range
    from datetime import date
    ACCESS_DEV_STAT_DATE_RANGE = (date(2014,1,1), date(2099,1,1)) 
    
    # control your access views 
    # if blank, include all
    ACCESS_DEV_STAT_INCLUDE_VIEWS = ['func_name_1', 'func_name_2', 'func_name_3']
    # if blank, no exclude
    ACCESS_DEV_STAT_EXCLUDE_VIEWS = []

URLconf
~~~~~~~
Add AccessDevStat's URLs to your project's URLconf as follows::

    urlpatterns += patterns(
        (r'^access_dev_stat/', include('access_dev_stat.urls')),
    )


Start Your Project
------------------

Start your django project, Then it will record every request in your `ACCESS_DEV_STAT_INCLUDE_VIEWS`.
