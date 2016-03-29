from os import path

from scripts.sudokuExtractor import Extractor


def getImagePath():
    image_path = path.abspath('train/image1.jpg')
    return image_path


def main():
    image_path = getImagePath()
    cells = Extractor(image_path).cells

main()
