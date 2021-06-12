import pickle
import numpy as np
import numpy.matlib
import pywt

#default paramters
Fs = 128
Time = 63

#set parameters
frameNum = 60
totalScale = 64
exScale = 32
datastart = 128 * 3;
datalength = 8064 - datastart
wname = 'gaus4'

nLabel, nTrial, nUser, nChannel, nData  = 4, 40, 32, 32, 8064

for i in range(1,nUser+1):
    if i < 10:
        x = pickle.load(open("E:/Programming/EEG/DEAP Project/DEAP/s0"+str(i)+".dat", 'rb'), encoding='latin1')
        print("E:/Programming/EEG/DEAP Project/DEAP/s0"+str(i)+".dat")
    else:
        x = pickle.load(open("E:/Programming/EEG/DEAP Project/DEAP/s"+str(i)+".dat", 'rb'), encoding='latin1')
        print("E:/Programming/EEG/DEAP Project/DEAP/s"+str(i)+".dat")
    
    
    for tr in range(nTrial):
        fout_data = open("E:/Programming/EEG/DEAP Project/Files/User"+str(i)+"_Video"+str(tr+1)+".dat",'w')
        output = np.zeros([nChannel, totalScale, frameNum])
        
        for ch in range(nChannel):
            
            data1 = np.zeros([datalength])
            for dl in range(datalength):
                data1[dl] = x['data'][tr][ch][dl+datastart]
            f = np.arange(1,totalScale+1)
            f = (Fs / totalScale) * f
            wcf = pywt.central_frequency(wname)
            scal = (Fs * wcf) / f

            coef, freqs = pywt.cwt(data1, np.arange(1,totalScale+1), wname)

            S = abs(np.array(coef) * np.array(coef))
            SC = 100 * S / sum(sum(S))

            scaleEnergy = np.sum(S, axis = 1)
            o = numpy.matlib.repmat(scaleEnergy.reshape([64,1]),1,datalength)
            p = S / o
            entropy = - p * np.log(p)
            scaleEntropy = np.sum(entropy,axis = 1)
            EER = scaleEnergy / scaleEntropy

            frameSize = int(60 / frameNum)
            start = 0
            data2 = np.zeros([totalScale,frameNum])
            for k in range(frameNum):
                output[ch,:,k] = np.sum(SC[:,start:frameSize*k+1], axis = 1)
                start += frameSize

        print('Write '+str(tr))    
        exoutput = output[:,8:40,:].reshape(nChannel * exScale,frameNum)
        for k in range(nChannel * exScale):
            for j in range(frameNum):
                fout_data.write(str(exoutput[k,j])+' ')
            fout_data.write('\n')

        fout_data.close()
