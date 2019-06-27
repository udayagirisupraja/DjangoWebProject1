"""
Definition of urls for polls viewing and voting.
"""

from django.conf import settings 
from django.conf.urls.static import static 
from .views import *

from django.conf.urls import url

import app.views

urlpatterns = [
    url(r'^$', app.views.file_upload, name = 'file_upload'),
    url('file_upload', app.views.file_upload, name = 'file_upload'), 
    url('sysinfrawarn', app.views.sysinfrawarn, name = 'sysinfrawarn'),
    url('tenants_freq', app.views.tenants_freq, name = 'tenants_freq'),
    url('top_ten_tenants',app.views.top_ten_tenants, name='top_ten_tenants'),
    url('pdf_view', app.views.pdf_view, name = 'pdf_view'),
    url('IMS_graphs', app.views.IMS_graphs, name = 'IMS_graphs'),
    url('top_three_tenants_graph', app.views.top_three_tenants_graph, name = 'top_three_tenants_graph'),
 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 