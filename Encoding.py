import pandas as pd

for user in range(4):
    f = pd.read_csv('E:/Programming/EEG/DEAP Project/labels_' + str(user) + '.csv')
    fout_labels_class = open('E:/Programming/EEG/DEAP Project/labels_class_' + str(user) + '.csv','w')
    for val in f['Label_' + str(user)]:
        if float(val) > 4.5:
            fout_labels_class.write(str(1) + "\n")
        else:
            fout_labels_class.write(str(0) + "\n")
    print('E:/Programming/EEG/DEAP Project/labels_class_' + str(user) + '.csv')
    fout_labels_class.close()
