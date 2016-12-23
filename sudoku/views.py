from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from serializers import SudokuImageSerializer

from PIL import Image
import numpy as np

from snapsudoku import snap_sudoku


def index(request):
    return HttpResponse("Hello, world!")


@api_view(['POST'])
def solve(request):
    serializer = SudokuImageSerializer(data=request.data)
    if serializer.is_valid():
        im = Image.open(request.data['image'].file)
        color_img = np.asarray(im)
        snap_sudoku(color_img)
        return HttpResponse("{}")
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
