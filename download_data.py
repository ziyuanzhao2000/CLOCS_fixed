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
dataset_format = '.tar.gz'
dataset_names_lst = [['PhysioNetChallenge2020_Training_CPSC'], ['15652862', '15653771']]

cmd_lst =  flatten(
           [([f'mkdir {dataset_name}',
              f'wget -O ./{dataset_name}/{dataset_name}{dataset_format} \
                        {dataset_source_base}{dataset_name}{dataset_format}',
              f'tar -xzf {dataset_name}/{dataset_name}{dataset_format} -C {dataset_name}',
              f'rm {dataset_name}/{dataset_name}{dataset_format}'])
                    for dataset_source_base, dataset_names in zip(dataset_source_base_lst, dataset_names_lst)
                    for dataset_name in dataset_names]
           )

for cmd in cmd_lst:
    _ = subprocess.run(cmd.split())