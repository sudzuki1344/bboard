from rest_framework import serializers

from .models import Rubric, Bb


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        # fields = '__all__'
        fields = ('id', 'name')
