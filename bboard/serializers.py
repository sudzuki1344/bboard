from rest_framework import serializers

from .models import Rubric, Bb

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'name')
