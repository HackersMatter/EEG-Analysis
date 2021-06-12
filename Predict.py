import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
import torch.nn.functional as F

from sklearn.metrics import accuracy_score

class cnn_classifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv11 = nn.Conv3d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.conv12 = nn.Conv3d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.pool1 = nn.MaxPool3d(kernel_size=2, padding=(0,0,1))
        
        self.conv21 = nn.Conv3d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.conv22 = nn.Conv3d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.pool2 = nn.MaxPool3d(kernel_size=2, padding=(0,0,1))
        
        self.conv31 = nn.Conv3d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.conv32 = nn.Conv3d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1)
        self.pool3 = nn.MaxPool3d(kernel_size=2, padding=0)
        

        self.fc_layer = nn.Linear(128*4*4*1, 2)
        
        self.dropout_layer = nn.Dropout(p=0.5)

    def forward(self, xb):
        h1 = self.conv11(xb)
        h1 = self.conv12(h1)
        h1 = self.dropout_layer(h1)
        h1 = self.pool1(h1)
        h1 = F.relu(h1)

        h2 = self.conv21(h1)
        h2 = self.conv22(h2)
        h2 = self.pool2(h2)
        h2 = F.relu(h2) 

        h3 = self.conv31(h2)
        h3 = self.conv32(h3)
        h3 = self.pool3(h3)
        h3 = F.relu(h3) 
        
        flatten = h3.view(-1, 128*4*4*1)
        out = self.fc_layer(flatten)
        return out


def predict(model, x_test, device):
    print('Predicting.....')
    model.eval()
    y_pred = model(x_test.view(-1, 1, 32, 32, 3).to(device))
    #acc = y_pred.argmax(1).eq(y_test.to(device)).float().mean().cpu().numpy()
    #print('test acc: %f'%(acc*100))
    return int(torch.mode(y_pred.argmax(1)).values)

def loadmodel():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    modelv = cnn_classifier()
    modelv.load_state_dict(torch.load('./CNN_model_valence.pth', map_location=device))

    modela = cnn_classifier()
    modela.load_state_dict(torch.load('./CNN_model_arousal.pth', map_location=device))

    return (modelv,modela,device)

