import pandas as pd
import pickle
import numpy as np

nLabel, nTrial, nUser, nChannel, nTime  = 4, 40, 32, 32, 8064
chan = ['Fp1','AF3','F3','F7','FC5','FC1','C3','T7','CP5','CP1','P3','P7','PO3','O1','Oz','Pz','Fp2','AF4','Fz','F4','F8','FC6','FC2','Cz','C4','T8','CP6','CP2','P4','P8','PO4','O2']

d = []

for i in range(2,3):
    if i < 10:
        fname = "E:/Programming/EEG/DEAP Project/DEAP/s0"+str(i)+".dat"
    else:
        fname = "E:/Programming/EEG/DEAP Project/DEAP/s"+str(i)+".dat" 
    x = pickle.load(open(fname, 'rb'), encoding='latin1')
    print(fname)
    for tr in range(nTrial):
        d1 = pd.DataFrame(np.transpose(x['data'][tr][:32][:]),columns=chan)
        #print(d1)
        d.append(d1)
d = pd.concat(d)
d.to_pickle('input2.pkl')
