import numpy as np
import pywt

#set parameters
frameNum = 60
totalScale = 64
exScale = 32

wname = 'gaus4'

nChannel = 32

def cwteeg(x,datalength = 128):
    output = np.zeros([nChannel, totalScale, frameNum])
    
    for ch in range(nChannel):
        data1 = np.zeros([datalength])
        for dl in range(datalength):
            data1[dl] = x[dl][ch]

        coef, freqs = pywt.cwt(data1, np.arange(1,totalScale+1), wname)

        S = abs(np.array(coef) * np.array(coef))
        SC = 100 * S / sum(sum(S))

        start = 0
        for k in range(frameNum):
            output[ch,:,k] = np.sum(SC[:,start:k+1], axis = 1)
            start += 1

    exoutput = output[:,8:40,:].reshape(nChannel * exScale,frameNum)

    temp_output = np.array([exoutput])

    x_min = temp_output.min(axis = (1,2),keepdims=True)
    x_max = temp_output.max(axis = (1,2),keepdims=True)
    dfs_normal = (temp_output-x_min)/(x_max-x_min)

    reshape_dfs = np.split(dfs_normal, frameNum/3, axis=2)
    reshape_dfs = np.array(reshape_dfs)
    reshape_dfs = np.reshape(reshape_dfs,[-1,1024,3])
    
    return reshape_dfs