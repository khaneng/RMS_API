from .models import Profile,Restaurant,Dish
from rest_framework import serializers
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# User serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'
class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = '__all__'
        # exclude = ('password', )

# class ItemSerializer(serializers.ModelSerializer):
#     # category = CategorySerializer(many=True, read_only=True)
#     category_name = serializers.CharField(source='category.name', required = False)
#     sub_category_name = serializers.CharField(source='sub_category.name', required = False)
#     class Meta:
#         model = Items
#         fields = ['name','category','category_id','sub_category','category_name','sub_category_name']