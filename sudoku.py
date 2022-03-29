#!/usr/bin/env python
# coding: utf-8

import os
import pickle
import sys

import numpy as np

from scripts.sudokuExtractor import Extractor
from scripts.train import NeuralNetwork
from scripts.sudoku_str import SudokuStr

from flask import Flask, request, render_template

app = Flask(__name__)


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
        print('Solving...')
        return s.solve()
    except ValueError:
        return 'No solution found. Please rescan the puzzle and try again.'


@app.route('/', methods=['GET', 'POST'])
def solve():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', result='No file')
        input_file = request.files['file']
        if input_file.filename == '':
            return render_template('index.html', result='No file selected. Please try again.')
        input_file.save(os.path.join(app.root_path, 'static/images/input.jpg'))
        solution = snap_sudoku('static/images/input.jpg')
        return render_template('index.html', result=solution)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
