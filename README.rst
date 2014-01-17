=====
Access Device Statistics
=====

AccessDevStat is a simple Django app to calculate every requst agent.

and it has offered a page to see alive agent number and opened agent number in these days.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Install
   pip install  git+https://github.com/yijingping/django-access-dev-stat#egg=django_access_dev_stat

1. Add "access_dev_stat" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'access_dev_stat',
    )

2. Include the access_dev_stat URLconf in your project urls.py like this::

    url(r'^access_dev_stat/', include('access_dev_stat.urls')),


3. Start the development server and visit http://127.0.0.1:8000/access_dev_stat/

