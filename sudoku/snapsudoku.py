#!/usr/bin/env python
# coding: utf-8

import os
import pickle
import sys

import cv2
import numpy as np

from scripts.sudokuExtractor import Extractor
from scripts.train import NeuralNetwork
from scripts.sudoku_str import SudokuStr


def create_net(rel_path):
    print (os.getcwd())
    with open(os.getcwd() + rel_path) as in_file:
        sizes, biases, wts = pickle.load(in_file)
    return NeuralNetwork(customValues=(sizes, biases, wts))


def get_cells(color_img):
    net = create_net(rel_path='\sudoku\\networks\\net')
    for row in Extractor(color_img).cells:
        for cell in row:
            x = net.feedforward(np.reshape(cell, (784, 1)))
            x[0] = 0
            digit = np.argmax(x)
            yield str(digit) if list(x[digit])[0] / sum(x) > 0.8 else '.'


def load_image(image_path):
    color_img = cv2.imread(os.path.abspath(image_path))
    if color_img is None:
        raise IOError('Image not loaded')
    print ('Image loaded.')
    return color_img


def snap_sudoku(color_img):
    grid = ''.join(cell for cell in get_cells(color_img))
    s = SudokuStr(grid)
    try:
        print('\nSolving...\n\n{}'.format(s.solve()))
    except ValueError:
        print('No solution found.  Please rescan the puzzle.')

if __name__ == '__main__':
    try:
        color_img = load_image(image_path=sys.argv[1])
        snap_sudoku(color_img=color_img)
    except IndexError:
        fmt = 'usage: {} image_path'
        print(fmt.format(__file__.split('/')[-1]))
