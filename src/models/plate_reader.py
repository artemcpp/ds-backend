import os
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms as T
from torchvision.models import resnet18, alexnet, vgg16, googlenet
from torchvision.transforms.functional import to_tensor
from PIL import Image, UnidentifiedImageError

import warnings

DEVICE=torch.device('cpu')

MEAN = np.array([0.485, 0.456, 0.406])
STD = np.array([0.229, 0.224, 0.225])
N_LETTERS=22

index_letter_map = {0: '9', 1: 'н', 2: 'а', 3: 'к', 4: 'м', 5: '5', 6: 'е', 7: '3', 8: 'т', 9: 'х', 10: 'о', 11: '8', 12: '0', 13: 'у', 14: '4', 15: 'р', 16: '7', 17: '2', 18: '1', 19: 'с', 20: 'в', 21: '6'}


class InvalidImage(Exception):
    pass


class PlateReader(nn.Module):
    def __init__(self, ):
        super(PlateReader, self).__init__()
        self.resnet = nn.Sequential(*(list(resnet18().children())[:-2]))
        self.cnn = nn.Conv1d(in_channels=512, kernel_size=3, padding=1, out_channels=N_LETTERS)
        self.relu = nn.ReLU()

    @staticmethod
    def load_from_file(path: str) -> 'PlateReader':
        model = PlateReader()
        model.to(DEVICE)
        model.load_state_dict(torch.load(path))

        model.eval()
        return model

    def forward(self, x):
        x = self.resnet(x)
        x = x.mean(axis=2)
        x = self.cnn(x)
        return x

    def read_text(self, image: bytes) -> str:
        transform = T.Compose([
            T.PILToTensor()
        ])
        
        image = Image.open(image)
        image = transform(image)

        image = image.repeat(3, 1, 1)
        norm = T.Normalize(MEAN, STD)
        image = norm(image.float() / 255.)
        image = image.to(DEVICE)
        with torch.no_grad():
            val_preds = self.forward(image.unsqueeze(0))
            y_pred = torch.argmax(val_preds, dim=1)
            res = ''.join([index_letter_map[j] for j in y_pred.cpu()[0].numpy()])

        return res
