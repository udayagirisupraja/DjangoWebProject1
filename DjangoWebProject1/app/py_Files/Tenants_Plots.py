#varsha
import pickle
import matplotlib.pyplot as plt
import os
from collections import OrderedDict
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.backends.backend_pdf


path = 'C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\' #path to dictionaries folder
subpath =  'C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\' # path to dictionaies folder
#ch

# plots bar graph for tenant vs frequency
def tenant_frequency_plot():
    pdf = matplotlib.backends.backend_pdf.PdfPages("C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\tenants.pdf")
    with open(os.path.join(subpath,'tenants_Dictionary' + '.txt'), 'rb') as handle:
            tenantCounts = pickle.loads(handle.read())
    #print(tenantCounts, type(tenantCounts))
    plt.title("TENANTS FREQUENCY")
    x = np.arange(2)
    plt.xlabel('Tenants')
    plt.ylabel('Frequency')
    #print(tenantCounts.values(), type(tenantCounts.values()))
    plt.bar(x, height = list(tenantCounts.values())[:2]) 
    plt.xticks(x, list(tenantCounts.keys())[:2])
    plt.xticks(rotation=90)
    #figure = plt.gcf() #saving to pdf
    #figure.set_size_inches(5, 5)
    pdf.savefig(bbox_inches = "tight")
   
    plt.close()
    
    tenantCounts.pop('IONMessagingService', None)
    tenantCounts.pop('ProvisioningService', None)
    for each in range(1,(len(tenantCounts)//30+1)):
        x = np.arange(30)
        plt.xlabel('Tenants')
        plt.ylabel('Frequency')
        plt.bar(x, height = list(tenantCounts.values())[(each-1)*30:each *30]) 
        plt.xticks(x, list(tenantCounts.keys())[(each-1)*30:each*30])
        plt.xticks(rotation=90)
        #figure = plt.gcf() #saving to pdf
        #figure.set_size_inches(5, 5)
        pdf.savefig(bbox_inches = "tight")
            #plt.show()
       

    rem = len(tenantCounts)%30    
    x = np.arange(rem)
    plt.xlabel('Tenants')
    plt.ylabel('Frequency')
    plt.bar(x, height = list(tenantCounts.values())[-rem:]) 
    plt.xticks(x, list(tenantCounts.keys())[-rem:])
    plt.xticks(rotation=90)
  
    #figure = plt.gcf() #saving to pdf
    #figure.set_size_inches(5, 5)
    pdf.savefig(bbox_inches = "tight")
    #plt.show()
    pdf.close()




