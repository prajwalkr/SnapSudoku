from rest_framework import serializers

from models import SudokuImage


class SudokuImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SudokuImage
        fields = ('image',)
