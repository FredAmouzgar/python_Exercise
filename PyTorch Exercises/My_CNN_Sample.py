# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import torch
from torch import nn
import torch.nn.functional as F

class ConvNet(nn.Module):
    def __init__(self, input_shape=(1,3,28,28)):
        super(ConvNet, self).__init__()
        self.cnn = nn.Sequential(nn.Conv2d(in_channels=3, out_channels=128, kernel_size=3, padding=1),
                                 nn.ReLU(),
                                 nn.MaxPool2d(2),
                                 nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),
                                 nn.ReLU(),
                                 nn.MaxPool2d(2))
        cs = self._calculate_cnn_output_shape(input_shape=input_shape)
        cnn_flattened_size = cs[1] * cs[2] * cs[3]
        self.dense = nn.Sequential(nn.Linear(cnn_flattened_size, 128),
                                   nn.ReLU(),
                                   nn.Linear(128, 10))
    
    def forward(self, x):
        x = self.cnn(x)
        x = x.view(x.shape[0], -1)
        return F.log_softmax(self.dense(x), dim=-1)
    
    def _calculate_cnn_output_shape(self, input_shape=(10, 3, 28, 28)):
        data = torch.rand(input_shape)
        return list(self.cnn(data).size())
        
        
    
if __name__ == "__main__":
    
    net = ConvNet()
    imgs = torch.rand(10, 3, 28, 28)
    with torch.no_grad():
        print(net(imgs))
        