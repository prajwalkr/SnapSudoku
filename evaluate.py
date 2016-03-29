import pickle as pck
import numpy as np
from pprint import pprint

from train import NeuralNetwork

net = pck.load(open('net','r'))
res = [[None for _ in range(9)] for _ in range(9)]
cells = pck.load(open('save','r'))
for i,row in enumerate(cells):
	for j,cell in enumerate(row):
		vector = np.reshape(cell, (784,1))
		x = net.feedforward(vector)
		res[i][j] = np.argmax(x),list(x[np.argmax(x)])[0]

pprint(res)