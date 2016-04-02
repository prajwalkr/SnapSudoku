from os import path
import pickle as pck
import numpy as np
from pprint import pprint
import sys

from scripts.sudokuExtractor import Extractor

def getImagePath(name):
    image_path = path.abspath('test/' + name)
    return image_path

def main(name):
    image_path = getImagePath(name)
    cells = Extractor(image_path).cells
    net = pck.load(open('net', 'r'))
    res = [[None for _ in range(9)] for _ in range(9)]
    for i, row in enumerate(cells):
        for j, cell in enumerate(row):
            vector = np.reshape(cell, (784, 1))
            x = net.feedforward(vector)
            x[0] = 0
            s = sum(x)
            if list(x[np.argmax(x)])[0] / s > 0.8:
                res[i][j] = str(np.argmax(x))
            else:
                res[i][j] = ' '

    pprint(res)

main(sys.argv[1])
