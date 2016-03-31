import pickle as pck
import numpy as np
from pprint import pprint

from train import NeuralNetwork

net = pck.load(open('net', 'r'))
res = [[None for _ in range(9)] for _ in range(9)]
cells = pck.load(open('save', 'r'))
for i, row in enumerate(cells):
    for j, cell in enumerate(row):
        vector = np.reshape(cell, (784, 1))
        x = net.feedforward(vector)
        x[0] = 0
        s = sum(x)
        if list(x[np.argmax(x)])[0] / s > 0.6:
            res[i][j] = str(np.argmax(x))
        else:
            res[i][j] = ' '

pprint(res)
