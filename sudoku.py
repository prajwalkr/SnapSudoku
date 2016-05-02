#!/usr/bin/env python
# coding: utf-8

import os
import pickle
import sys

import numpy as np

from scripts.sudokuExtractor import Extractor
from scripts.train import NeuralNetwork
from scripts.sudoku_str import SudokuStr


def create_net(rel_path):
    with open(os.getcwd() + rel_path) as in_file:
        sizes, biases, wts = pickle.load(in_file)
    return NeuralNetwork(customValues=(sizes, biases, wts))


def get_cells(image_path):  # yields 9 * 9 = 81 cells
    net = create_net(rel_path='/networks/net')
    for row in Extractor(os.path.abspath(image_path)).cells:
        for cell in row:
            x = net.feedforward(np.reshape(cell, (784, 1)))
            x[0] = 0
            digit = np.argmax(x)
            yield str(digit) if list(x[digit])[0] / sum(x) > 0.8 else '.'


def snap_sudoku(image_path):
    grid = ''.join(cell for cell in get_cells(image_path))
    s = SudokuStr(grid)
    try:
        print('\nSolving...\n\n{}'.format(s.solve()))
    except ValueError:
        print('No solution found.  Please rescan the puzzle.')


if __name__ == '__main__':
    try:
        snap_sudoku(image_path=sys.argv[1])
    except IndexError:
        fmt = 'usage: {} image_path'
        print(fmt.format(__file__.split('/')[-1]))
