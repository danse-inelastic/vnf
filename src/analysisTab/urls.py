from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT }),
    (r'^analysis/menu/$', 'analysis.views.menu'),
    (r'^analysis/sqeCoh/getTrajectory/$', 'analysis.views.getTrajectory'),
    (r'^analysis/sqeCoh/pickTrajectory/$', 'analysis.views.pickTrajectory'),
    (r'^analysis/(?P<type>.*)/pickTrajectory/$', 'analysis.views.pickTrajectory'),
    (r'^analysis/(?P<type>.*)/settings/$', 'analysis.views.settings'),
    # Example:
    # (r'^analysisTab/', include('analysisTab.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
