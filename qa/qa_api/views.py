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
from qa_api.models import Question, FenixEduAPIUser, Answear, Course
#View sets
from rest_framework import viewsets
#Serializers
from qa_api.serializers import UserSerializer, QuestionSerializer, AnswearSerializer, CourseSerializer
#REST framework
from rest_framework.decorators import api_view, permission_classes, link, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import APIException
from rest_framework import status
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
		# Current user
		# Validate course
		obj.user = self.request.user
		course = self.request.POST['course']
		api = fenix.FenixAPISingleton()
		fenix_user = FenixEduAPIUser.objects.get(user=obj.user)
		courses = api.get_person_courses(user=fenix_user.get_fenix_api_user())
		enrolments = courses['enrolments']
		teaching = courses['teaching']

		for enrol in enrolments:
			if course == enrol['id']:
				obj.course = course
				return True

		for teach in teaching:
			if course == teach['id']:
				obj.course = course
				return True
		raise APIException('Invalid course')

	@action(methods=['GET', 'POST'])
	def answears(self, request, pk=None):
		if request.method == 'GET':
			return self.get_answears(request, pk)
		elif request.method == 'POST':
			return self.post_answear(request, pk)

	def get_answears(self, request, pk=None):
		question = self.get_object()
		answears = question.answears.all()
		serializer = AnswearSerializer(answears, many=True)
		return Response(serializer.data)

	def post_answear(self, request, pk=None):
		question = self.get_object()
		serializer = AnswearSerializer(data=request.DATA)
		if serializer.is_valid():
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Courses
class UserViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

# Specific methods
# Get the authentication url
@api_view(['GET'])
@permission_classes((AllowAny, ))
def authentication_url(request):
	api = fenix.FenixAPISingleton()
	authentication_url = api.get_authentication_url()
	return Response({"authentication_url" : authentication_url})

# Set code: After getting the code now it's time to request an access token
@api_view(['POST'])
@permission_classes((AllowAny, ))
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
	
	return Response({'access_token' : fenix_api_user.access_token,
		'refresh_token' : fenix_api_user.refresh_token})

# get token: Get an access token using a refresh token
"""@persmission_classes((AllowAny, ))
def get_token(request):
	refresh_token = request.GET['refresh_token']

	try:
		fenix_api_user = FenixEduAPIUser.objects.get(refresh_token=refresh_token)
		api = FenixAPISingleton()
	except:
"""

@api_view(['GET'])
def get_person_courses(request):
	api = fenix.FenixAPISingleton()
	fenix_user = FenixEduAPIUser.objects.get(user=request.user)
	fenix_api_user = fenix_user.get_fenix_api_user()
	courses = api.get_person_courses(user=fenix_api_user)
	person_courses = []

	# Add the courses to DB if they don't exists already
	enrolments = courses['enrolments']
	teaching = courses['teaching']

	for enrol in enrolments:
		course, created = Course.objects.get_or_create(fenix_id=enrol['id'], name=enrol['name'])
		if created:
			course.save()
		person_courses.append(course)

	for teach in teaching:
		course, created = Course.objects.get_or_create(fenix_id=teach['id'], name=teach['name'])
		if created:
			course.save()
		person_courses.append(course)

	db_courses = person_courses
	serializer = CourseSerializer(db_courses, many=True)
	return Response(serializer.data)
