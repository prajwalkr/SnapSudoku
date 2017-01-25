# SnapSudoku

Take a picture of an unsolved Sudoku and have SnapSudoku solve it for you! This repository also consists of an Android application which harnesses an API endpoint created using [Django REST Framework](http://www.django-rest-framework.org/).

## How to use

```
$ git clone https://github.com/ymittal/SnapSudoku.git
$ cd SnapSudoku
$ pip install -r requirements.txt
$ python sudoku/snapsudoku.py <path>
```

You can read the directions to test the Android application [**here**](https://github.com/ymittal/SnapSudoku/blob/master/android/README.md).

### Algorithm

 - Basic image preprocessing - **Thresholding**
 - Crop out approx. Sudoku puzzle (largest contour)
 - Get the grid square verticles (*need for improvement*)
    - Get the largest contour of the image
    - Get the largest bounding rectangle within the contour
    - Compute the grid corners
- Do a **warp perspective** on the Sudoku
- Extract cells by slicing the grid evenly
- Isolate cells as follows
    - Extract the largest connected component, giving more priority to the center pixels
    - Remove all major noise in a cell
- Predict digits using a Neural Network

The Neural Network created was trained with around 250 digits. The [constants](https://github.com/ymittal/SnapSudoku/blob/master/sudoku/networks/net) used in the training phase and the [training dataset](https://github.com/ymittal/SnapSudoku/tree/master/sudoku/train) can be found in the repository itself.

### Working

Here's a Sudoku image from a smartphone:

![](https://lh3.googleusercontent.com/-rGpsVTsqkYU/VwysnNV6U4I/AAAAAAAAG00/1XVCxhPkVzMTugwy53PUTVu76JtywthyQCLcB/s1000/test1.jpg "Input image")

The current code produces the following output:

![](https://lh3.googleusercontent.com/-PLL7mtKdT68/VxzRU-D1mxI/AAAAAAAAH4s/v2lvYd_mQes3J3ta0PwQ_W2gwxhrVS_VQCLcB/s500/Final+Result.png "Final Result")

**Note:** For a detailed step-by-step demo, check out [**this**](https://github.com/ymittal/SnapSudoku/blob/master/demo/README.md).

## TODO

- [ ] Improve algorithm to get better Sudoku grid extraction and make it more robust against blurs.
- [ ] Improve empty cell detection. Only a basic logic is being used right now. 

### Contributors

* [prajwalkr](https://github.com/prajwalkr) **Prajwal Renukanand**
* [cclauss](https://github.com/cclauss)
* [lakshmanaram](https://github.com/lakshmanaram)
* [ymittal](https://github.com/ymittal) **Yash Mittal**

We are happy to get new ideas to make the application more accurate. Feel free to submit a pull request or open an issue. :smile:
