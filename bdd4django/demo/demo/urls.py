from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #Poll
    url(r'^vote/(?P<poll_id>\d+)/$', 'polls.views.vote', name='vote'),
    url(r'^total_votes/(?P<poll_id>\d+)/$', 'polls.views.total_votes', name='total_votes'),

)
