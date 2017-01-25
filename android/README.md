# SnapSudoku Android

An Android application to solve an unsolved sudoku by taking its picture

## Getting Started

* Before testing on an emulator, run the Django server as follows. You can access `localhost` at `http://10.0.2.2:8000/` on an Android emulator.
  
  ```
  $ python manage.py runserver
  ```
  **Note:** You need to turn on camera settings for your emulator.

* If you deployed the Django app, add the URL to the list of `ALLOWED_HOSTS` in [`settings.py`](https://github.com/ymittal/SnapSudoku/blob/master/django_project/settings.py). Additionally, modify the `baseUrl` of `Retrofit.Builder()` in the Java code.

## Authors

Please feel free to reach out to [Yash Mitta](yashmittal2009@gmail.com) if you have questions regarding the Android codebase.
