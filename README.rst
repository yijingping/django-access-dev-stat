=====
Access Device Statistics
=====

AccessDevStat is a simple Django middleware to collect device info from every agent.

And also it offered charts to show these device statistics. 

From these charts, you can find: 

1) the the number of devices which are alive or opened in 2 weeks.

2) app channels, app versions, app platfrom statistics.


Here is some screen shot from my django app.

![app alive](docs/screenshot/alive.png)

![app alive](docs/screenshot/version.png)

By the way, it also do good on mobile.

![app alive](docs/screenshot/app_version.png)

![app alive](docs/screenshot/app_list.png)


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

