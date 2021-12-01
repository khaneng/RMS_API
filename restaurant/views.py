from django.shortcuts import render
# from django.contrib.gis.utils import GeoIP
from .serializers import ProfileSerializer, UserSerializer, RestaurantSerializer, DishSerializer
from .models import Profile,Restaurant,Dish
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from requests import get
import requests
from rest_framework.renderers import JSONRenderer
from math import radians, cos, sin, asin, sqrt



def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		print('x_forwarded_for')
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META['HTTP_X_REAL_IP']
	return ip

#Register API
class RegisterApi(generics.GenericAPIView):
	serializer_class = UserSerializer
	def post(self, request, *args,  **kwargs):
		
		ip = get('https://api.ipify.org').content.decode('utf8')
		request.data['password'] = make_password(request.data['password'])
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		
		try:
			user = serializer.save()
		except Exception as e:
			raise e
		
		
		response = requests.get("https://geolocation-db.com/json/"+ip).json()
		print(response)
		profile = Profile(user = user,current_location_lat =response.get('latitude'),current_location_lng=response.get('longitude'))
		profile.save()
		return Response({
			
			"message": "User Created Successfully.  Now perform Login to get your token",
		})

class CreateSubadminApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		
		if request.user.is_superuser:
			user_id = request.data.get('user_id')
			Profile.objects.filter(user=user_id).update(is_subadmin = True)
			
		else:
			return Response({
			
			"message": "Only admin can create sub_admin",
		})
		return Response({
			
			"message": "Subadmin Created.",
		})


class CreateRestaurantApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = RestaurantSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		print("in CreateRestaurantApi")
		profile = Profile.objects.filter(user=request.user).first()
		is_subadmin = None
		if profile:
			is_subadmin = getattr(profile, 'is_subadmin')
		
		if request.user.is_superuser or is_subadmin:
			request.data['created_by'] = request.user.id
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			
			try:
				restaurant = serializer.save()
			except Exception as e:
				raise e
			

		else:
			return Response({
			
			"message": "Only admin or sub_admin can create Restaurant",
		})
		return Response({
			
			"message": "Restaurant Created.",
			"restaurant_id": restaurant.id,
			"restaurant_name": restaurant.name
		})



class CreateDishApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = DishSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		profile = Profile.objects.filter(user=request.user).first()
		is_subadmin = None
		if profile:
			is_subadmin = getattr(profile, 'is_subadmin')
		
		if request.user.is_superuser or is_subadmin:
			request.data['created_by'] = request.user.id
			request.data['restaurant'] = [request.data['restaurant_id']]
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			
			try:
				dish = serializer.save()
			except Exception as e:
				raise e
			

		else:
			return Response({
			
			"message": "Only admin or sub_admin can create dish",
		})
		return Response({
			
			"message": "Dish Created.",
			"dish_id": dish.id,
			"dish_name": dish.name
		})



class GetRestaurantApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = RestaurantSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		restaurant = Restaurant.objects.all()
		serializer = self.get_serializer(restaurant, many=True)
		print(serializer.data)
				
		return Response({
			"restaurant": serializer.data,
		})

class GetDishApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = DishSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		dish = Dish.objects.filter(restaurant = request.data['restaurant_id'])
		serializer = self.get_serializer(dish, many=True)
		print(serializer.data)
				
		return Response({
			"dish": serializer.data,
		})



class GetSubadminApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = ProfileSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		print('in GetSubadminApi')
		profile = Profile.objects.filter(is_subadmin = True)
		serializer = self.get_serializer(profile, many=True)
		print(serializer.data)
				
		return Response({
			"sub_admins": serializer.data,
		})

class RestaurantDistanceApi(generics.GenericAPIView):
	permissions_classes = (permissions.IsAuthenticated,)
	serializer_class = RestaurantSerializer
	# authentication_classes = (TokenAuthentication,)
	
	def post(self, request, *args,  **kwargs):
		restaurant = Restaurant.objects.filter(id = request.data['restaurant_id']).first()
		profile = Profile.objects.filter(user = request.user.id).first()
		user_lat = profile.current_location_lat
		user_lng = profile.current_location_lng
		serializer = self.get_serializer(restaurant)
		serializer_data = serializer.data.copy()
		serializer_data['distance'] = self.distance(restaurant.restaurant_lat,user_lat,restaurant.restaurant_lng,user_lng)
		return Response({
			"restaurant": serializer_data,
		})

	def distance(self,lat1, lat2, lon1, lon2): 
		print("in distance")
		# The math module contains a function named
		# radians which converts from degrees to radians.
		lon1 = radians(lon1)
		lon2 = radians(lon2)
		lat1 = radians(lat1)
		lat2 = radians(lat2)
		  
		# Haversine formula
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	 
		c = 2 * asin(sqrt(a))
		
		# Radius of earth in kilometers. Use 3956 for miles
		r = 6371
		  
		# calculate the result
		return(c * r)


