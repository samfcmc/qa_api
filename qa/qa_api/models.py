"""
-------------------
Models file
-------------------
"""

"""
Imports
"""
# Models
from django.db import models
from django.contrib.auth.models import User

# Fenix API SDK
import fenix

class Course(models.Model):
	fenix_id = models.CharField(max_length=200)
	name = models.CharField(max_length=200)

class Answear(models.Model):
	user = models.ForeignKey(User)
	text = models.CharField(max_length=500000)

class Question(models.Model):
	user = models.ForeignKey(User)
	answears = models.ManyToManyField(Answear)
	course = models.CharField(max_length=200)
	text = models.CharField(max_length=10000)

class TopAnswear(models.Model):
	question = models.ForeignKey(Question)
	answear = models.ForeignKey(Answear)

# Models for authentication
class FenixEduAPIUser(models.Model):
	user = models.ForeignKey(User)
	code = models.CharField(max_length=255)
	access_token = models.CharField(max_length=255, unique=True)
	refresh_token = models.CharField(max_length=255)
	token_expires = models.IntegerField(default=0)

	def get_fenix_api_user(self):
		user = fenix.User(username=self.user.username, code=self.code, 
				access_token=self.access_token, refresh_token=self.refresh_token, 
				token_expires=self.token_expires)
		return user

