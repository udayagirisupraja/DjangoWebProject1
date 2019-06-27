import os
import pandas as pd 
import pickle
#INCOMPLETE
path = "C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\log_Files\\" #path to uploaded csv file along with file name
subpath = 'C:\\Users\\supraja\\source\\repos\\DjangoWebProject1\\DjangoWebProject1\\pyt_Files\\pdf_Files\\' #path to output folder without file name


def loadCsv(file_path):
    global path
    global subpath
    data_files = dict()

    data_files['data_file'] = pd.read_csv(file_path, encoding='latin-1')

    with open(os.path.join(subpath,'data_files_dict.txt'), 'wb') as handle:
                pickle.dump(data_files, handle)

    with open(os.path.join(subpath,'data_files_dict.txt'), 'rb') as handle:
                dic = pickle.loads(handle.read())