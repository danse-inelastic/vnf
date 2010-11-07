from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('analysis.views',
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^analysis/menu/$', 'menu'),
    (r'^analysis/sqeCoh/getTrajectory/$', 'getTrajectory'),
    (r'^analysis/sqeCoh/pickTrajectory/$', 'pickTrajectory'),
    (r'^analysis/(?P<type>.*)/pickTrajectory/$', 'pickTrajectory'),
    (r'^analysis/(?P<type>.*)/settings/$', 'settings'),
    # Example:
    # (r'^analysisTab/', include('analysisTab.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
