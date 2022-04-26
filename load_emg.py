import os
import numpy as np
import pickle
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder

alias = 'emg'
trial = 'contrastive_ss'
basepath = os.path.join(os.getcwd(), 'data', alias)

phase_lst = ['train','val','test']
phase_fraction_lst = [0.6, 0.2, 0.2]
modality = 'emg'
fraction = 1
term = 'All Terms'
desired_leads = ['I']

n_samples = 204
train_set = np.random.choice(np.arange(n_samples), int(n_samples * phase_fraction_lst[0]), replace=False)
val_set = np.random.choice(np.setdiff1d(np.arange(n_samples), train_set),
                           int(n_samples * phase_fraction_lst[1]), replace=False)


# modality -> fraction -> phase -> term
input_dict = {}
output_dict = {}
pid_dict = {}
input_dict[modality] = {}
output_dict[modality] = {}
pid_dict[modality] = {}
input_dict[modality][fraction] = {}
output_dict[modality][fraction] = {}
pid_dict[modality][fraction] = {}
labels = [0, 1, 2]
enc = LabelEncoder()
enc.fit(labels)

for phase in phase_lst:
    input_dict[modality][fraction][phase] = {}
    output_dict[modality][fraction][phase] = {}
    pid_dict[modality][fraction][phase] = {}
    input_dict[modality][fraction][phase][term] = []
    output_dict[modality][fraction][phase][term] = []
    pid_dict[modality][fraction][phase][term] = []


sample_fs = 4000 # Hz
target_fs = 4000 # Hz
downsample_stride = sample_fs // target_fs
target_fs = sample_fs // downsample_stride
window_len = 2500 # samples
n_channels = 1
data_file_names = ['emg_healthy.txt', 'emg_myopathy.txt', 'emg_neuropathy.txt']
pid = 0

for data_file_name, label in zip(data_file_names, labels):
    encoded_label = enc.transform(np.array([label])).item() # each file corresponds to a label
    signal = np.loadtxt(os.path.join(basepath, data_file_name))[:,1:2] # first column is timestamp, not needed
    signal = signal[::downsample_stride,:] # downsample
    signal_length = signal.shape[0]
    signal = signal[:signal_length // window_len * window_len,:]
    signal_length = signal.shape[0]
    signals = signal.reshape((signal_length // window_len, window_len))
    for i in range(signals.shape[0]):
        if i in train_set:
            phase = phase_lst[0]
        elif i in val_set:
            phase = phase_lst[1]
        else:
            phase = phase_lst[2]
        input_dict[modality][fraction][phase][term].append(signals[i, :])
        output_dict[modality][fraction][phase][term].append([encoded_label] * n_channels)
        pid_dict[modality][fraction][phase][term].append([pid] * n_channels)
        pid += 1

for phase in phase_lst:
    input_dict[modality][fraction][phase][term] = np.array(input_dict[modality][fraction][phase][term])
    output_dict[modality][fraction][phase][term] = np.array(output_dict[modality][fraction][phase][term])
    pid_dict[modality][fraction][phase][term] = np.array(pid_dict[modality][fraction][phase][term])

savepath = os.path.join(basepath, trial,'leads_%s' % str(desired_leads))
if os.path.isdir(savepath) == False:
    os.makedirs(savepath)

""" Save Frames and Labels Dicts """
with open(os.path.join(savepath,'frames_phases_%s.pkl' % alias),'wb') as f:
    pickle.dump(input_dict,f)

with open(os.path.join(savepath,'labels_phases_%s.pkl' % alias),'wb') as g:
    pickle.dump(output_dict,g)

with open(os.path.join(savepath,'pid_phases_%s.pkl' % alias),'wb') as h:
    pickle.dump(pid_dict,h)

print('Final Frames Saved!')
