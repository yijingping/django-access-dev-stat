Configuration
=============

Server Side Configuration
-------------------------

Explicit Date Range
~~~~~~~~~~~~~~~~~~~
if you want control record date range. set the start date and the end date in ``settings.py`` 

    # control available date range
    from datetime import date
    ACCESS_DEV_STAT_DATE_RANGE = (date(2014,1,1), date(2099,1,1)) 


Explicit View Founction 
~~~~~~~~~~~~~~~~~~~~~~~~
you can record  view founction optionally, by configuring in ``settings.py``

include all::

    ACCESS_DEV_STAT_INCLUDE_VIEWS = []
    ACCESS_DEV_STAT_EXCLUDE_VIEWS = []

include only explicit view founction::

    ACCESS_DEV_STAT_INCLUDE_VIEWS = ['func_name_1', 'func_name_2', 'func_name_3']
    ACCESS_DEV_STAT_EXCLUDE_VIEWS = []

exclude explicit view founction, include others::

    ACCESS_DEV_STAT_INCLUDE_VIEWS = []
    ACCESS_DEV_STAT_EXCLUDE_VIEWS = ['func_name_1', 'func_name_2', 'func_name_3']


Client Side Configuration
-------------------------

Set cookies in every requst, these cookies' name was set in ``settings.py``::

    # cookie name set in every request 
    GUID_COOKIE_NAME = '_guid'
    DEVICE_COOKIE_NAME = '_device'
    PLATFORM_COOKIE_NAME = '_platform'
    CHANNEL_COOKIE_NAME = '_channel'
    VERSION_COOKIE_NAME = '_version'

These cookies' value was depend on you agent. Here is some example::

    _guid = '93466123007793498587'       # uuid.guid()
    _device = '9932ae98bcfa89'       # deviceid
    _platform = 'android'        # `android` or `iPhone`
    _channel = 'baidu'          # `baidu`, `360`, `hiapk`
    _version = '2.5.2'          # your app version
