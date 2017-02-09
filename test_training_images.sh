#!/bin/bash

I=1
while [ $I -le 10 ]; do
    printf "\nimage${I}.jpg...\n"
    python ./sudoku.py train/image${I}.jpg
    let I+=1
done
