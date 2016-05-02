SnapSudoku
===================

*Take a picture of a Sudoku and have SnapSudoku solve it for you!*


----------
 TODO:
---------
 - [ ] Improve algorithm to get better Sudoku Grid extraction, make it `more robust against blurs` .
 - [ ] Improve `empty cell detection`. Only a basic logic is used right now. 

Prerequisites:
-------------

- Python 2.7 but __not__ Python 3
    - Download from [here](https://www.python.org/downloads/)

- OpenCV
    - `sudo apt-get install python-opencv` (preferred)
    - Install OpenCV from [here](http://opencv.org/downloads.html) 

- Numpy (1.11.0)
    - `pip install numpy` (preferred)
    - You can build it from source [here](https://github.com/numpy/numpy)

How to use: 
----------
    git clone https://github.com/prajwalkr/SnapSudoku.git
    cd SnapSudoku
    python sudoku.py <path-to-input-image>


Working:
-------
> Here's a Sudoku image from a smartphone:

![Input Sudoku Image](https://lh3.googleusercontent.com/-rGpsVTsqkYU/VwysnNV6U4I/AAAAAAAAG00/1XVCxhPkVzMTugwy53PUTVu76JtywthyQCLcB/s1000/test1.jpg "Input image")![](blob:https%3A//drive.google.com/7556d1d6-752d-4e86-b913-8373d50ebe41) 
</br>

> The current code gives out the following output to the Terminal:

![Final result](https://lh3.googleusercontent.com/-PLL7mtKdT68/VxzRU-D1mxI/AAAAAAAAH4s/v2lvYd_mQes3J3ta0PwQ_W2gwxhrVS_VQCLcB/s500/Final+Result.png "Final Result")

Algorithm
-------------

 > 1. Basic image preprocessing - **Thresholding**.
 > 2. Crop out approx. Sudoku puzzle (Largest contour)
 > 3. Get the grid square vertices: *(a better way of doing this is required!)* </br>
   3.1. Get the **largest contour** of the image.</br>
   3.2. Get the largest **bounding rectangle** within the contour.</br>
   3.3. Compute the grid corners. 
> 4. Do a **Warp perspective** on the sudoku image
> 5. We will extract cells from this, by slicing the sudoku grid evenly.
> 6. Digit isolation in cell is done through a series of steps: </br>
    6.1. Extract the **largest connected component** in the image, giving more *priority to the center pixels*. </br>
    6.2. Removing all major noise in the cell. 
> 7.  Predict Digits using a Neural Network. 

> The only 3rd party libraries required are  *OpenCV, Numpy*. The Neural Network created was trained with around 250 digits. The constants used in the training phase, the training data-set is in this repository itself. 

Here are some illustrations of the different stages:
-------

> After Preprocessing:

![After Preprocessing](https://lh3.googleusercontent.com/-hTPN4mSDNiY/Vwy8UgTcxNI/AAAAAAAAG1c/e67gE9TSAKQrcd-ADHmAgOtuMDQPhyCrgCLcB/s500/After+Preprocessing.png "After Preprocessing")

> Final processed Sudoku Grid

![enter image description here](https://lh3.googleusercontent.com/-AcbLo77wYH0/VxtPrbXcAYI/AAAAAAAAH0E/OmEzl2Hn9JkjQTxfdAVTn7ZeN3q3rsutgCLcB/s500/Sudoku+Grid.png "Sudoku Grid Image")

> Here are a few digits after processing the cells:

![Digit 3](https://lh3.googleusercontent.com/-2zxwex6LYnk/VxtQEQH6fDI/AAAAAAAAH0Q/nFmrwIlm7HYV7O2qZEoICQDKF8fcoFKmQCLcB/s100/three.png "Three")![Digit 8](https://lh3.googleusercontent.com/-oPRnuu7XXxc/VwzHKJjnpyI/AAAAAAAAG2o/11FlxwHkkygGEHgoY4NQLZroq-fH6b5MACLcB/s100/eight.png "eight.png") 

> Here's a typical empty cell:

![empty cell](https://lh3.googleusercontent.com/-p2bhyuRWptI/VwzHVYrtABI/AAAAAAAAG2w/C_vKYzb75sQ8gcPdf0aaHCjB6dM02du8wCLcB/s100/emptycell.png "emptycell.png")

>  Predicted Grid:

![Prediction](https://lh3.googleusercontent.com/-bmiUuMHZtYw/VxtQ8SezWLI/AAAAAAAAH0s/VV8HvATwHEAfhtKJqT6nK-fh0A28E52gwCLcB/s500/Digits.png "Digits")

> Solved Grid:

![Solved Grid](https://lh3.googleusercontent.com/-zWnlGKCz9xs/VxzSmieN5EI/AAAAAAAAH48/DR6t33TSfhgDVe7ew3n0YRKAUJB45rKWACLcB/s500/Solved+Grid.png "Solved Grid")
----------
Contributors
------------------
[cclauss](https://github.com/cclauss) <br/>
[lakshmanaram](https://github.com/lakshmanaram)

I'll be very happy to get new ideas to improve the accuracy and make the application better. Feel free to give a pull request! :smile:



