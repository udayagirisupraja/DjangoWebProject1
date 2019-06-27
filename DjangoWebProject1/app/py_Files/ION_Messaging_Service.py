import pandas as pd
import numpy as np
import os
from datetime import timedelta
import matplotlib.pyplot as plt
import re
from rake_nltk import Rake

data_file2 = dict()
i = 0
for csv_files in filter(lambda x: x.endswith('.csv'), os.listdir()):
    data_file2["dfile" + str(i)] = pd.read_csv(csv_files, encoding='latin-1')
    i = i + 1
print(len(data_file2))


"""
IONMessagingService  - next largest frequency tenant 

Here we consideration as follows:

categories  --> indexof the value of respective category in IONMessagingService_Ls

password Authentication = 0
communication Fail = 1
polling Daemon = 2
input String Closed = 3
account Disabled = 4
connection reset = 5
connection could not be made = 6
else = 7

"""
raw_KeyWords_List = []
src_Names = []
def classify_Msg(data_file2):
    IONMessagingService_Ls = [0] * 8
    l = len(data_file2)
    rake = Rake()

    for i in range(l):
        if 'application' in data_file2['_sourcecategory'][i]: 
            if 'IONMessagingService' in data_file2['_sourcename'][i]:
                particular_raw = data_file2['_raw'][i].lower()
                if 'password authentication' in particular_raw:
                    IONMessagingService_Ls[0] += 1
                elif 'communication Fail' in particular_raw:
                    IONMessagingService_Ls[1] += 1
                elif 'PollingDaemon' in particular_raw:
                    IONMessagingService_Ls[2] += 1
                elif 'input String Closed' in particular_raw:
                    IONMessagingService_Ls[3] += 1
                elif 'account Disabled' in particular_raw:
                    IONMessagingService_Ls[4] += 1
                elif 'connection reset' in particular_raw:
                    IONMessagingService_Ls[5] += 1
                elif 'connection could not be made' in particular_raw:
                    IONMessagingService_Ls[6] += 1
                else:
                    rake.extract_keywords_from_text(particular_raw)
                    keyWords = rake.get_ranked_phrases()
                    regex = r"\{(.*?)\}"
                    p = re.compile(regex)
                    result = p.search(particular_raw)
                    src_Names.append(result.group(1))
                    #print("Keywords of row ", (i + 2), " are: \n", keyWords, "\n")    #to view the particular row key words of raw
                    raw_KeyWords_List.append(keyWords)
                    IONMessagingService_Ls[7] += 1
    return (raw_KeyWords_List,src_Names, IONMessagingService_Ls)  


"""
Generates the list which contains of specified category (info, warn, error)
"""
def getLists(raw_KeyWords):
    category_List = [[], [], []]
    for keyWords in raw_KeyWords:
        if (' info ' in keyWords[0]):
            category_List[0].append(keyWords)
        elif(' warn ' in keyWords[0]):
            category_List[1].append(keyWords)
        elif(' error ' in keyWords[0]):
            category_List[2].append(keyWords)
    return(category_List)

"""
Generates the list which contains of specified message generators (ProvisioningEntitlementHelper, 
BaseRuntimeEntitlementHelper, MessagingExceptionMapper, Others)
"""

def getmsg_gen_Lists(msg_gen_KeyWords):
    msg_gen_catList = [[], [], [], [], [], []]
    for keyWords in msg_gen_KeyWords:
        if any ('provisioningentitlementhelper' in s for s in keyWords):
            msg_gen_catList[0].append(keyWords)
        elif any ('baseruntimeentitlementhelper' in s for s in keyWords):
            msg_gen_catList[1].append(keyWords)
        elif any ('messagingexceptionmapper' in s for s in keyWords):
            msg_gen_catList[2].append(keyWords)
        elif any ('messagingserviceexception' in s for s in keyWords):
            msg_gen_catList[3].append(keyWords)
        elif any ('applicationcachenotificationlistener' in s for s in keyWords):
            msg_gen_catList[4].append(keyWords)
        else:
            msg_gen_catList[5].append(keyWords)
    return(msg_gen_catList)


"""
Generates the list which contain specified message generators along with the source names, which is further used to extract the
tenant names.
"""

def getmsg_gen_Lists_Src_Names(msg_gen_KeyWords, src_names,index):
    msg_gen_catList = [[], [], [], [], [], []]
    msg_gen_KeyWords_len = len(msg_gen_KeyWords)
    msg_gen_List_src_Names = [[], [], [], [], [], []]
    
    for  i in range(msg_gen_KeyWords_len):
        #print(msg_gen_KeyWords_len[i][0])        
        if any ('provisioningentitlementhelper' in s for s in msg_gen_KeyWords[i]):
            msg_gen_catList[0].append(msg_gen_KeyWords[i])
            msg_gen_List_src_Names[0].append(src_names[i])
        elif any ('baseruntimeentitlementhelper' in s for s in msg_gen_KeyWords[i]):
            msg_gen_catList[1].append(msg_gen_KeyWords[i])
            msg_gen_List_src_Names[1].append(src_names[i])
        elif any ('messagingexceptionmapper' in s for s in msg_gen_KeyWords[i]):
            msg_gen_catList[2].append(msg_gen_KeyWords[i])
            msg_gen_List_src_Names[2].append(src_names[i])
        elif any ('messagingserviceexception' in s for s in msg_gen_KeyWords[i]):
            msg_gen_catList[3].append(msg_gen_KeyWords[i])
            msg_gen_List_src_Names[3].append(src_names[i])
        elif any ('applicationcachenotificationlistener' in s for s in msg_gen_KeyWords[i]):
            msg_gen_catList[4].append(msg_gen_KeyWords[i])
            msg_gen_List_src_Names[4].append(src_names[i])
        else:
            msg_gen_catList[5].append(msg_gen_KeyWords[i])
            msg_gen_List_src_Names[5].append(src_names[i])
        
    return(msg_gen_catList[index], msg_gen_List_src_Names[index])


"""
generates the frequencies of category
"""
def getFrequencies(input_List): 
    i = 0
    counts = [None] * len(input_List)
    for value in input_List:
        counts[i] = len(value)
        i = i + 1
    return(counts)


"""
returns the list of tenants along with the frequencies which are causing the MessageExceptionMarker
"""

def getTenants_IONMsg_Marker(raw_KeyWords_List, src_Names):
    msg_exc_list, msg_exc_tenant = getmsg_gen_Lists_Src_Names(raw_KeyWords_List, src_Names, 2)
    tenants_dict = dict()
    for i in range(len(msg_exc_list)):
        tenant = msg_exc_tenant[i]
        if(tenant in tenants_dict):
            tenants_dict[tenant] += 1
        else:
            tenants_dict[tenant] = 1
    return(tenants_dict)
#print(getTenants_Msg_Exc_Marker())


def ion_msg_service(data_file2, index):
    raw_KeyWords_List,src_Names, IONMessagingService_Ls = classify_Msg(data_file2)
    category_list = getLists(raw_KeyWords_List)
    msg_gen_catList = getmsg_gen_Lists(raw_KeyWords_List)
    freq = getFrequencies(category_list)
    msg_gen_freq = getFrequencies(msg_gen_catList)
    plt.title("Category of stmnts (info, warn, error)")
    plt.ylabel('Frequency');
    x = np.arange(3)
    plt.bar(x, height=freq) 
    plt.xticks(x, ['info','warn','error'])
    pdf.savefig()
    plt.show()
    
    plt.ylabel('Frequency');
    x = np.arange(len(msg_gen_freq))
    plt.title("Exception Class Category")
    plt.bar(x, height=msg_gen_freq) 
    plt.xticks(x, ['P','B', 'MEMap', 'MSE', 'AL', 'O'])
    pdf.savefig()
    plt.show()
    
    ls = getTenants_IONMsg_Marker(raw_KeyWords_List,src_Names)
    x_val = list(ls.keys())
    y_val = list(ls.values())
    x = x_val
    x_val = np.arange(len(y_val))
    plt.title("MessagingExceptionMapper")
    plt.ylabel('Frequency');
    plt.bar(x_val, height=y_val) 
    plt.xticks(x_val, x)
    plt.xticks(rotation=90)
    figure = plt.gcf() # get current figure
    figure.set_size_inches(7, 9)
    pdf.savefig()
    plt.show()
    
"""
To save the plotted figure into pdf
"""
import matplotlib.backends.backend_pdf
pdf = matplotlib.backends.backend_pdf.PdfPages("Analysing_IMS_plots.pdf")

"""
Converting UTC date format to general date format
"""
from datetime import datetime
from datetime import timedelta, time


def getStndTime(T1, minutes):
    int_minutes = (int(minutes[:2]) * 60) + (int(minutes[2:4]))
    return(T1 + timedelta(minutes=int_minutes))

def getGeneralDate(utc_date):
    dateTime_time = getStndTime(datetime.strptime(utc_date[:19], "%m/%d/%Y %H:%M:%S"), utc_date[-4:])
    return dateTime_time

getGeneralDate('02/27/2019 13:25:17.000 +0530').time()

for i in range(0, len(data_file2)):
    utc_date_file = data_file2['dfile' + str(i)]['_messagetime'][0]
    gnrl_date = getGeneralDate(utc_date_file)
    print(" File : " + str(gnrl_date))
    plt.suptitle('File: ' + str(gnrl_date), fontsize=14, fontweight='bold')  #setting the Title at intial
    ion_msg_service(data_file2.get("dfile" + str(i)), i)
    
    
pdf.close()
def getCatagories_Others():
    others_list, others_tenant = getmsg_gen_Lists_Src_Names(raw_KeyWords_List, src_Names, 5)
    print(len(others_list))
    others_dict = dict()
    for i in range(len(others_list)):
        tenant = others_tenant[i]
        if(tenant in others_dict):
            others_dict[tenant] += 1
        else:
            others_dict[tenant] = 1
    return(others_dict)

getCatagories_Others()