import pickle
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import pywt

#default paramters
Fs = 128
Time = 63

#set parameters
frameNum = 60
totalScale = 64
exScale = 32
datastart = 128 * 3
datalength = 8064 - datastart
wname = 'gaus4'

nLabel, nTrial, nUser, nChannel, nData  = 4, 40, 32, 32, 8064

averageEER = np.zeros([totalScale])
for i in range(1,nUser+1):
    if i < 10:
        x = pickle.load(open("E:/Programming/EEG/DEAP Project/DEAP/s0"+str(i)+".dat", 'rb'), encoding='latin1')
        print("E:/Programming/EEG/DEAP Project/DEAP/s0"+str(i)+".dat")
    else:
        x = pickle.load(open("E:/Programming/EEG/DEAP Project/DEAP/s"+str(i)+".dat", 'rb'), encoding='latin1')
        print("E:/Programming/EEG/DEAP Project/DEAP/s"+str(i)+".dat")
    
    sumEER = np.zeros([totalScale])
    for tr in range(nTrial):
        tempEER = np.zeros([totalScale,nChannel])

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
            
            tempEER[:,ch] = EER
        print(tr + 1)
        sumEER = sumEER + np.mean(tempEER,axis=1)

    averageEER = averageEER + (sumEER / 40)
    plt.plot(sumEER / 40,'*')
    plt.title('Average EER over all EEG channels')
    plt.xlabel('Scales')
    plt.ylabel('Energy/Entropy')
    plt.savefig('E:/Programming/EEG/DEAP Project/Scale Select/User'+str(i)+'.png')
    plt.close()

plt.plot(averageEER / 32,'*')
plt.title('Average EER over all EEG channels')
plt.xlabel('Scales')
plt.ylabel('Energy/Entropy')
plt.savefig('E:/Programming/EEG/DEAP Project/Scale Select/All_Users.png')
plt.close()