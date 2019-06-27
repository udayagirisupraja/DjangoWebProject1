#varsha
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
import pickle
import os
import matplotlib.backends.backend_pdf

path = 'C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\' #path to dictionaries folder
#INCOMPLETE
subpath =  'C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\' # path to dictionaies folder

def all_logs_plot(test = False):
        pdf = matplotlib.backends.backend_pdf.PdfPages("C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\sys_infra_app.pdf")
        with open(os.path.join(subpath,'sysInfraApp_Dictionary'+ '.txt'), 'rb') as handle:
            dic = pickle.loads(handle.read())
        
        lst = list(dic.values())
        x = np.arange(3)
        print(x, lst)
        plt.title("File")
        plt.ylabel('Frequency');
        plt.xlabel('Errors');
        plt.bar(x, height = lst)
        
        plt.xticks(x, ['application','infra','system'])
        if not test:
            print ("Application: ", lst[0] ,"\nInfra: ", lst[1], "\nSystem: ", lst[2], "\n")
            
            #figure = plt.gcf() #saving to pdf
            pdf.savefig(bbox_inches = "tight")#saving to pdf
            #plt.show()
        pdf.close()
        plt.close()
