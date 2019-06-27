import pandas as pd
import pickle
import os

import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_pdf import PdfPages

pp = PdfPages('C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\top_three_plots.pdf')

def get_plots(path):
    data_file2 = pd.read_csv(path)
    l = len(data_file2)    
    tenantCounts = OrderedDict()
    for i in range(l):
        if 'application' in data_file2['_sourcecategory'][i]:
            j = data_file2['_sourcename'][i].find('/grid-node-')
            start = data_file2['_sourcename'][i].find('-', j+10)
            end = data_file2['_sourcename'][i].find('_CloudService',start)
            if end == -1:
                end = data_file2['_sourcename'][i].find('-',j+11)
            tenant = data_file2['_sourcename'][i][start+1: end]
            if tenant in tenantCounts:
                tenantCounts[tenant] += 1
            else:
                tenantCounts[tenant] = 1
    tenantCounts = OrderedDict(sorted(tenantCounts.items(), key=lambda x:x[1], reverse=True))
    sortedTenantCounts = sorted(tenantCounts.items(), key=lambda x: x[1])

    Top_ten_tenants = []
    for i in  sortedTenantCounts[::-1]:

        if i[0].isupper():
            Top_ten_tenants.append(i)
        if len(Top_ten_tenants) == 3:
            break
    print(Top_ten_tenants)
    labels = ['INFO','WARN','ERROR']
    
    for tc in Top_ten_tenants:
            l = []
            l1 = [[]]
            keyword_list = [0] * 8
            print(tc[0], tc[1])
            for i in range(len(data_file2)):
                if 'application' in data_file2['_sourcecategory'][i]: 
                    if tc[0] in data_file2['_sourcename'][i]:
                        particular_raw = data_file2['_raw'][i]
                        l1.append(particular_raw)
           
          
            category_List = [[], [], []]
            for keyWords in l1:
                if ('INFO' in keyWords):
                    category_List[0].append(keyWords)
                elif('WARN' in keyWords):
                    category_List[1].append(keyWords)
                elif('ERROR' in keyWords):
                    category_List[2].append(keyWords)
            
            i = 0
            counts = [None] * len(category_List)
            for value in category_List:
                len(value)
                counts[i] = len(value)
                i = i + 1
            freq = counts
            title = plt.title("Category of stmnts (info, warn, error) of "+tc[0] ,fontweight='bold')
            plt.ylabel('Frequency');
            x = np.arange(3)
            
            plt.bar(x, height=freq) 
            plt.xticks(x, ['info','warn','error'])
            plt.legend([tc[0]], loc='upper left',fontsize = 10)
            pp.savefig(bbox_inches = "tight")
         
            #plt.show()
            
            
            for cl in range(3):
                if len(category_List[cl]) != 0:
                    l = category_List[cl] 
                    x2 = ['password authentication','Communication failure','PollingDaemon','input string closed','Account disabled','Connection reset', 'Connection could not be made','others']
                    keyword_list = [0] * 8
                    for i in l:
                        if 'password authentication' in i:
                            keyword_list[0] += 1
                        elif 'Communication failure' in i:
                            keyword_list[1] += 1
                        elif 'PollingDaemon' in i:
                            keyword_list[2] += 1
                        elif 'input string closed' in i:
                            keyword_list[3] += 1
                        elif 'Account disabled' in i:
                            keyword_list[4] += 1
                        elif 'Connection reset' in i:
                            keyword_list[5] += 1
                        elif 'Connection could not be made' in i:
                            keyword_list[6] += 1
                        else:
                            keyword_list[7] += 1
                    x = np.arange(8)
                    title = plt.title("Exception by Tenant " + tc[0] + "  "+labels[cl])
                    plt.ylabel('Frequency'); 
                    plt.bar(x, height = keyword_list, color = 'r')
                    plt.xticks(x,x2 )
                    plt.legend([labels[cl]], loc='upper left',fontsize = 10)
                    plt.xticks(rotation=90)
                    pp.savefig(bbox_inches = "tight")
                    #plt.show()
                    print(keyword_list)
                else:
                    print("no errors in "+ labels[cl] +" of "+ tc[0])
    
    pp.close()             
    return
        

def get_Tenants(path):
    #path = "C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\media\\log_Files" #path to uploaded csv file along with file name

    data_file2 = pd.read_csv(path, encoding='latin-1')

    l = len(data_file2)    
    tenantCounts = OrderedDict()
    for i in range(l):
        if 'application' in data_file2['_sourcecategory'][i]:
            j = data_file2['_sourcename'][i].find('/grid-node-')
            start = data_file2['_sourcename'][i].find('-', j+10)
            end = data_file2['_sourcename'][i].find('_CloudService',start)
            if end == -1:
                end = data_file2['_sourcename'][i].find('-',j+11)
            tenant = data_file2['_sourcename'][i][start+1: end]
            if tenant in tenantCounts:
                tenantCounts[tenant] += 1
            else:
                tenantCounts[tenant] = 1
    tenantCounts = OrderedDict(sorted(tenantCounts.items(), key=lambda x:x[1], reverse=True))
    sortedTenantCounts = sorted(tenantCounts.items(), key=lambda x: x[1])

    Top_ten_tenants = []
    for i in  sortedTenantCounts[::-1]:

        if i[0].isupper():
            Top_ten_tenants.append(i)
        if len(Top_ten_tenants) == 10:
            break

    return(Top_ten_tenants)
    
    