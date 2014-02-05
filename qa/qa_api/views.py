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
from qa_api.models import Question, FenixEduAPIUser
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
	serializer_class = QuestionSerializer
	model = Question
	def get_queryset(self):
		queryset = Question.objects.all()
		return queryset

	def pre_save(self, obj):
		obj.user = self.request.user

# Specific methods
# Get the authentication url
@api_view(['GET'])
def authentication_url(request):
	api = fenix.FenixAPISingleton()
	authentication_url = api.get_authentication_url()
	return Response({"authentication_url" : authentication_url})

# Set code: After getting the code now it's time to request an access token
@api_view(['POST'])
def set_code(request):
	code = request.GET.get('code')
	fenix_user = fenix.User()
	api = fenix.FenixAPISingleton()
	api.set_code(code=code, user=fenix_user)
	person = api.get_person(fenix_user)

	username = person['username']
	# Check if the user already exists
	try:
		user = User.objects.get(username=username)
		fenix_api_user = FenixEduAPIUser.objects.get(user=user)
		fenix_api_user.access_token = fenix_user.access_token
		fenix_api_user.refresh_token = fenix_user.refresh_token
		fenix_api_user.code = fenix_user.code
		fenix_api_user.token_expires = fenix_user.token_expires

		user.save()
		fenix_api_user.save()
	except User.DoesNotExist:
		# User is not in the database yet
		name = person['name']
		name_split = name.split()
		first_name = name_split[0]
		last_name = name_split[len(name_split) - 1]
		# Doing this because authentication is made throught Fenix API and not django
		password = 'anything'
		user = User.objects.create(username=username, password=password,
				first_name=first_name, last_name=last_name)

		fenix_api_user = FenixEduAPIUser.objects.create(user=user, access_token=fenix_user.access_token,
				refresh_token=fenix_user.refresh_token, token_expires=fenix_user.token_expires,
				code=fenix_user.code)

		user.save()
		fenix_api_user.save()
	
	return Response({'access_token' : fenix_api_user.access_token})
