from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User) #, related_name = '%(class)s_uprofile'
	is_subadmin = models.BooleanField(default=False)
	current_location_lat = models.FloatField()
	current_location_lng = models.FloatField()
	

	def __str__(self):
		return self.user.username

class Restaurant(models.Model):
	created_by = models.ForeignKey(User,related_name = 'restaurant_created_by') 	
	name = models.CharField(max_length = 200)
	restaurant_lat = models.FloatField()
	restaurant_lng = models.FloatField()
	
	

	def __str__(self):
		return self.name


class Dish(models.Model):
	created_by = models.ForeignKey(User,related_name = 'dish_created_by') 
	name = models.CharField(max_length = 200)
	restaurant = models.ManyToManyField(Restaurant)

	def __str__(self):
		return self.name