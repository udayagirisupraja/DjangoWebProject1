"""
Definition of views.
"""
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from os import path

import json
from .py_Files import *
from django.http import HttpResponse 
from django.shortcuts import redirect 
from django.shortcuts import render
from .forms import *
from .py_Files.Tenants_Plots import tenant_frequency_plot
from .py_Files.sys_infra_warns import all_logs_plot
from .py_Files.top_ten_tenants import get_Tenants, get_plots
from .py_Files.IMS_Plots import get_Ims_plots
from .py_Files.Create_Dicts_TypesOfLogs_Tenants import tenant_frequency, app_infra_sys, load_CDTO
from .py_Files.Load_CSV import loadCsv



file_path = '../DjangoWebProject1/pyt_Files/log_Files/'
pdf_path = 'C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\'
pdf_name = ''


#update pdf_name variable to dispplay pdf
def pdf_view(request):
    global pdf_path
    global pdf_name
    pdf_Name = pdf_name[:]
    pdf_file_path = pdf_path + pdf_Name
    print("Entered pdf-view():  ", pdf_file_path)
    
    with open(pdf_file_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type ='application/pdf')
        #response['Content-Disposition'] = ('inline;filename=' + pdf_Name)
        response['Content-Disposition'] = ('attachment;filename=' + pdf_Name)
        print("Exited pdf-view()")
        return response

    pdf.closed


#Top_Three_tenants display pdf
def top_three_tenants_graph(request):
    global pdf_name
    global file_path
    get_plots(file_path)
    pdf_name = 'top_three_plots.pdf'
    return HttpResponseRedirect('pdf_view')


#TOP_TEN_TENANTS
def top_ten_tenants(request):
    global file_path
    print("Entered into top_ten_tenants()")
    res = get_Tenants(file_path)
    #res =  [('WATERCARE_TST', 918), ('IESHOLDINGSLLC03_PRD', 576), ('PACE_PRD', 197), ('WATAMI_TRN', 171), ('CYCLEURO_PRD', 121), ('QUALA_PRD', 76), ('SWMINTL_PRD', 63), ('INFORHCM_PRD', 62), ('ACCENTURE_TRN', 57), ('ANDERSENCORP_DEV', 56)]
    print("Exited into top_ten_tenants(): res is ", res)
    return render(request, 'app/top_ten_tenants_display.html', {'ten_tents' : res})

#sysinfrawarn
def sysinfrawarn(request):
    global pdf_name
    global file_path
    all_logs_plot()
    pdf_name = 'sys_infra_app.pdf'
    return HttpResponseRedirect('pdf_view')


#tenants_freq
def tenants_freq(request):
    global pdf_name
    global file_path
    loadCsv(file_path)
    load_CDTO()
    pdf_name = 'tenants.pdf'
    tenant_frequency_plot()
    return HttpResponseRedirect('pdf_view')

def IMS_graphs(request):
    global pdf_name
    global file_path

    get_Ims_plots(file_path)
    pdf_name = 'Analysing_IMS_plots.pdf'
    return HttpResponseRedirect('pdf_view')



def file_upload(request):
    global file_path
    print("Entered into Image_upload")
    if request.method == 'POST':
        print("Entered into POST also")
        form = FileUploadForm(request.POST, request.FILES) 
        if form.is_valid:
            form.save()
            file_path  += request.FILES['log_File'].name
            return HttpResponseRedirect(top_ten_tenants)
            #return HttpResponseRedirect("top_ten_tenants")
    else:
        form = FileUploadForm() 
    print("goto hotel_image_form.html")
    return render(request, 'app/index.html', {'form' : form}) 




def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )