"""
-------------
Views file
-------------
"""

"""
Imports
"""

#Models
from django.contrib.auth.models import User
from qa_api.models import Question
#View sets
from rest_framework import viewsets
#Serializers
from qa_api.serializers import UserSerializer, QuestionSerializer, AnswearSerializer, CourseSerializer
#Decorators
from rest_framework.decorators import api_view
#Responses
from rest_framework.response import Response
#Fenix SDK
import fenix

"""
Classes
"""
# View sets
# Users TODO: Delete this or give this just to admin
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

# Questions
class QuestionViewSet(viewsets.ModelViewSet):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

# Specific methods
# Get the authentication url
@api_view(['GET'])
def authentication_url(request):
	api = fenix.FenixAPISingleton()
	authentication_url = api.get_authentication_url()
	return Response({"authentication_url" : authentication_url})

