#!/usr/bin/env bash

docker build -t snap_sudoku .
docker run -it --rm --name snap_sudoku snap_sudoku
