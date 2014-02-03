from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
	fenix_id = models.CharField(max_length=200)
	name = models.CharField(max_length=200)

class Answear(models.Model):
	user = models.ForeignKey(User)
	text = models.CharField(max_length=500000)

class Question(models.Model):
	user = models.ForeignKey(User)
	answears = models.ManyToManyField(Answear)
	course = models.ForeignKey(Course)
	text = models.CharField(max_length=10000)

class TopAnswear(models.Model):
	question = models.ForeignKey(Question)
	answear = models.ForeignKey(Answear)

