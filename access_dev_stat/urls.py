from django.conf.urls.defaults import patterns

urlpatterns = patterns('access_dev_stat.views',
    (r'^$', 'index'),
    (r'^app_alive/$', 'app_alive'),
    (r'^app_version/$', 'app_version'),
    (r'^app_channel/$', 'app_channel'),
    (r'^app_platform/$', 'app_platform'),
)
