SnapSudoku
===================

*Take a picture of a Sudoku and have SnapSudoku solve it for you!*


----------
 #### <i class="icon-pencil"></i> TODO:

 - Add `code to solve` the Sudoku from the predicted output grid.
 - Improve algorithm to get better Sudoku Grid extraction, make it `more robust against blurs` .
 - Improve `empty cell detection`. Only a basic logic is used right now. 
 - Improve accuracy by checking and removing same digits predicted in the same row/column. 

> How to use: 

    python sudoku.py <path-to-input-image>

> Here's a Sudoku image from a smartphone:

![Input Sudoku Image](https://lh3.googleusercontent.com/-rGpsVTsqkYU/VwysnNV6U4I/AAAAAAAAG00/1XVCxhPkVzMTugwy53PUTVu76JtywthyQCLcB/s1000/test1.jpg "test1.jpg")![](blob:https%3A//drive.google.com/7556d1d6-752d-4e86-b913-8373d50ebe41) 

</br>
> The current code gives out the following output to the Terminal:

![Final set of predicted digits](https://lh3.googleusercontent.com/-fiDbDkl_K0c/VwytWw8EmUI/AAAAAAAAG1A/_zl5CLKBsuw1M9YnvVZsYM0goyX__5PdgCLcB/s1000/Final+Set+of+Digits.png "Final Set of Digits.png")
Algorithm
-------------

 > 1. Basic image preprocessing - **Thresholding**.
 > 2. Crop out approx. Sudoku puzzle (Largest contour)
 > 3. Get the grid square vertices: *(a better way of doing this is required!)*
   3.1. Get the **largest contour** of the image.
   3.2. Get the largest **bounding rectangle** within the contour.
   3.3. Compute the grid corners. 
> 4. Do a **Warp perspective** on the sudoku image
> 5. We will extract cells from this, by slicing the sudoku grid evenly.
> 6. Digit isolation in cell is done through a series of steps:
    6.1. Extract the **largest connected component** in the image, giving more *priority to the center pixels*.
    6.2. Removing all major noise in the cell. 
> 7.  Predict Digits using a Neural Network. 

> The only 3rd party library required is  *OpenCV*. The Neural Network created was trained with around 250 digits. The constants used in the training phase, the training data-set is in this repository itself. 

Here are some images through the process:
-------

> After Preprocessing:

![After Preprocessing](https://lh3.googleusercontent.com/-hTPN4mSDNiY/Vwy8UgTcxNI/AAAAAAAAG1c/e67gE9TSAKQrcd-ADHmAgOtuMDQPhyCrgCLcB/s500/After+Preprocessing.png "After Preprocessing.png")

> Final processed Sudoku Grid

![Final processed Sudoku Grid](https://lh3.googleusercontent.com/--Fg-hdourGA/Vwy85uIDTVI/AAAAAAAAG1o/Qxk9ZTHf1JQmyzmkNrLPJmO0EQ3ea5DoQCLcB/s500/Final+Sudoku+Grid.png "Final Sudoku Grid.png")

> Here are a few digits after processing the cells:

![Digit 3](https://lh3.googleusercontent.com/-FUS-oLg9IFg/VwzG4TkmbkI/AAAAAAAAG2Y/Itp5IgR-RQEolR83GAjf0pTZxd-1jgWGQCLcB/s100/three.png "three.png")![Digit 5](https://lh3.googleusercontent.com/-3M9WyxA40lw/VwzG-pJTKHI/AAAAAAAAG2g/Dnh0sk7MQ18rHvpUQM-bT3RvjR1T1HTyACLcB/s100/five.png "five.png")![Digit 8](https://lh3.googleusercontent.com/-oPRnuu7XXxc/VwzHKJjnpyI/AAAAAAAAG2o/11FlxwHkkygGEHgoY4NQLZroq-fH6b5MACLcB/s100/eight.png "eight.png") 

> Here's a typical empty cell:

![empty cell](https://lh3.googleusercontent.com/-p2bhyuRWptI/VwzHVYrtABI/AAAAAAAAG2w/C_vKYzb75sQ8gcPdf0aaHCjB6dM02du8wCLcB/s100/emptycell.png "emptycell.png")

>  Predicted Grid:

 ![Prediction](https://lh3.googleusercontent.com/-oMYqzsvb5WM/VwzHoe7OB4I/AAAAAAAAG28/kWf8acj3NtkDrrMJP_rlIzFELxlO1JBKACLcB/s400/Digits.png "Digits.png")
----------
Contributions
------------------
I'll be very happy to get new ideas to improve the accuracy and make the application better. Feel free to give a pull request! 

---------
License
---------
![enter image description here](https://cloud.githubusercontent.com/assets/7397433/9025904/67008062-3936-11e5-8803-e5b164a0dfc0.png)




