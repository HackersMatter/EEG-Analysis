# user defined modules
import Predict
import CWT_UI
import UI

import mne
import time
import numpy as np
import torch
import pandas as pd
import threading
from multiprocessing import Process
modelv, modela, device = Predict.loadmodel()
emotion = [['Sad','Angry'],
           ['Relaxed','Happy']]

chan = ['Fp1','AF3','F3','F7','FC5','FC1','C3','T7','CP5','CP1','P3','P7','PO3','O1','Oz','Pz','Fp2','AF4','Fz','F4','F8','FC6','FC2','Cz','C4','T8','CP6','CP2','P4','P8','PO4','O2']

dummy_df = pd.read_pickle("./input1.pkl")
mood = ''

app = UI.App()
for i in range(int(dummy_df.shape[0]/128)):
    start = time.time()

    data = np.array(dummy_df.iloc[i*128:(i*128)+128][:])
    dfs = CWT_UI.cwteeg(data)

    dfs = torch.from_numpy(dfs).float()

    result_a = Predict.predict(modela,dfs,device)
    result_v = Predict.predict(modelv,dfs,device)
    time.sleep(1)

    app.updateinfo(str(emotion[result_v][result_a]))
    if mood != str(emotion[result_v][result_a]):
        mood = str(emotion[result_v][result_a])
        app.updatetree(mood)
    print('Time: ', time.time() - start)
    print(result_v,result_a,emotion[result_v][result_a])
