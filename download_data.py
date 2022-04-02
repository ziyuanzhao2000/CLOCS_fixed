import os
import subprocess

"""
Will download PhysioNet2020 dataset for now into a data folder in the script's directory

"""


try:
    os.mkdir('data')
except FileExistsError:
    print('data folder already exists!')
os.chdir('data')

basepath = f'{os.getcwd()}'

def flatten(newlist):
    return [item for items in newlist for item in items]

dataset_source_base_lst = ['https://storage.googleapis.com/physionet-challenge-2020-12-lead-ecg-public/',
                       'https://figshare.com/ndownloader/files/']
dataset_source_filenames_lst = [['PhysioNetChallenge2020_Training_CPSC'], ['15652862', '15653771']]
dataset_formats_lst = [['.tar.gz'], ['.zip', '.xlsx']]
dataset_download_need_format_lst = [True, False]
dataset_names_lst = ['PhysioNetChallenge2020_Training_CPSC', 'chapman_ecg']
empty_char = ''
cmd_lst =  flatten(
           [([f'mkdir {dataset_name}',
              f'wget -O ./{dataset_name}/{dataset_source_filename}{dataset_format} \
                        {dataset_source_base}{dataset_source_filename}{dataset_format if need_format else empty_char}'] + \
              ([f'tar -xzf {dataset_name}/{dataset_source_filename}{dataset_format} -C {dataset_name}', \
               f'rm {dataset_name}/{dataset_source_filename}{dataset_format}']
                    if dataset_format in ['.tar.gz', '.zip'] else [])
              )
                    for dataset_name, dataset_source_base, dataset_source_filenames, dataset_formats, need_format in
                        zip(dataset_names_lst, dataset_source_base_lst, dataset_source_filenames_lst,
                            dataset_formats_lst, dataset_download_need_format_lst)
                    for dataset_source_filename, dataset_format in zip(dataset_source_filenames, dataset_formats)]
           )

for cmd in cmd_lst:
    _ = subprocess.run(cmd.split())