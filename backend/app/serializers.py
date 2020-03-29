from rest_framework import serializers
from .models import Student, Result, ResType

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

class ResTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResType
        fields = '__all__'