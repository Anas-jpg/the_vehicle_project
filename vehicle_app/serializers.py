from rest_framework import serializers
from .models import Brand, Car

from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password',
                                      style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


def validate_car_name(value):
    if 'test' in value.lower():
        raise serializers.ValidationError("Car name cannot contain the word 'test'.")
    return value


class BrandNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['page_id', 'page_name']


def validate_year(value):
    if value < 1886 or value > 2100:
        raise serializers.ValidationError("Year must be between 1886 and 2100.")
    return value


class CarSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(
        slug_field='page_name',
        queryset=Brand.objects.all()
    )

    class Meta:
        model = Car
        fields = ['id', 'name', 'model', 'year', 'brand']
        validators = [validate_car_name]

    def validate(self, data):
        if data['model'] == data['brand'].page_name:
            raise serializers.ValidationError("Model name and Brand name cannot be the same.")
        return data


class MakeSerializer(serializers.Serializer):
    make = serializers.CharField()

    def validate_make(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Make must be at least 2 characters long.")
        return value


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['page_id', 'page_name', 'url']
