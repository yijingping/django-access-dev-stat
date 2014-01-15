from django.conf.urls.defaults import patterns

urlpatterns = patterns('access_dev_stat.views',
    (r'^$', 'index'),
    (r'^alive/$', 'alive'),
)
