import os
import pickle as pck
import numpy as np
from pprint import pprint
import sys

from scripts.sudokuExtractor import Extractor
from scripts.train import NeuralNetwork


class Sudoku(object):

    def __init__(self, name):
        image_path = self.getImagePath(name)
        cells = Extractor(image_path).cells
        neuralnetpath = os.getcwd() + '/networks/net'
        sizes, biases, wts = pck.load(open(neuralnetpath, 'r'))
        net = NeuralNetwork(customValues=(sizes, biases, wts))
        self.res = [[None for _ in range(9)] for _ in range(9)]
        
        for i, row in enumerate(cells):
            for j, cell in enumerate(row):
                vector = np.reshape(cell, (784, 1))
                x = net.feedforward(vector)
                x[0] = 0
                s = sum(x)
                if list(x[np.argmax(x)])[0] / s > 0.8:
                    self.res[i][j] = str(np.argmax(x))
                else:
                    self.res[i][j] = ' '

        pprint(self.res)

    def getImagePath(self, name):
        return os.path.abspath(name)

Sudoku(sys.argv[1])
