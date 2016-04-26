#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import os
import pickle
import sys
from pprint import pprint

import numpy as np

from scripts.sudokuExtractor import Extractor
from scripts.train import NeuralNetwork


class Sudoku(object):
    def __init__(self, name):
        image_path = self.getImagePath(name)
        cells = Extractor(image_path).cells
        neural_net_path = os.path.join(os.getcwd(), 'networks', 'net')
        with open(neural_net_path, 'r') as in_file:
            sizes, biases, wts = pickle.load(in_file)
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

    @staticmethod
    def getImagePath(name):
        return os.path.abspath(name)

Sudoku(sys.argv[1])
