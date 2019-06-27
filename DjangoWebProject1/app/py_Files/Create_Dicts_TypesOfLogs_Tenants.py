
import pandas as pd
import pickle
import os
from collections import OrderedDict
#INCOMPLETE
subpath = 'C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\' #path to data_files.txt


 # Returns dictionary with tenant as key and its freuency as value
def tenant_frequency(fileName):
    global data_files
    tenantCounts = OrderedDict()
    sourcecategory = data_files[fileName]['_sourcecategory']
    sourcename = data_files[fileName]['_sourcename']
    for e in range(len(data_files[fileName])):
        if 'application' in sourcecategory[e]:
            j = sourcename[e].find('/grid-node-')
            start = sourcename[e].find('-', j+10)
            end = sourcename[e].find('_CloudService',start)
            if end == -1:
                end = sourcename[e].find('-',j+11)
            tenant = sourcename[e][start+1: end]
            if tenant in tenantCounts:
                tenantCounts[tenant] += 1
            else:
                tenantCounts[tenant] = 1
    tenantCounts = OrderedDict(sorted(tenantCounts.items(), key=lambda x:x[1], reverse=True))
    return tenantCounts

# returns a list of application, infra , system logs frequencies dictionary
def app_infra_sys(fileName):
    frequencies = {
        "application_freq" : 0, "infra_freq" : 0, "system_freq" : 0
    }
    sourcecategory = data_files[fileName]['_sourcecategory']
    for file_row in range(len(data_files[fileName])):
        if 'application' in sourcecategory[file_row]: frequencies["application_freq"] += 1
        elif 'infra' in sourcecategory[file_row]:frequencies["infra_freq"] += 1
        else: frequencies["system_freq"] += 1
    return frequencies


data_files = []

def load_CDTO():
    global data_files
    global subpath
    #Stroring tenant frequency into text file
    with open(os.path.join(subpath,'data_files_dict.txt'), 'rb') as handle:
            data_files = pickle.loads(handle.read())
    txtFile = 'tenants_Dictionary' 
    with open(os.path.join(subpath,(txtFile + '.txt')), 'wb') as handle:
            pickle.dump(tenant_frequency('data_file'), handle)

    txtFile = 'sysInfraApp_Dictionary'
    with open(os.path.join(subpath,(txtFile + '.txt')), 'wb') as handle:
            pickle.dump(app_infra_sys('data_file'), handle)

