"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views

import app.forms
import app.views

admin.autodiscover()

urlpatterns = [
    url(r'^', include('app.urls', namespace="app")),
    url('sysinfrawarn', app.views.sysinfrawarn, name = 'sysinfrawarn'),
    url('tenants_freq', app.views.tenants_freq, name = 'tenants_freq'),
    url(r'^about$', app.views.about, name='about'),
    url('IMS_graphs', app.views.IMS_graphs, name = 'IMS_graphs'),
    url(r'^file_upload$', app.views.file_upload, name='file_upload'),
    url('top_three_tenants_graph', app.views.top_three_tenants_graph, name = 'top_three_tenants_graph'),
]
