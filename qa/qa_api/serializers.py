
from django.contrib.auth.models import User
from qa_api.models import Course, Question, Answear
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')

class CourseSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Course
		fields = ('id', 'fenix_id', 'name')

class AnswearSerializer(serializers.HyperlinkedModelSerializer):
	user = serializers.Field(source='user.username')
	class Meta:
		model = Answear
		fields = ('user', 'text')

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
	user = serializers.Field(source='user.username')
	answears = AnswearSerializer(many=True)
	class Meta:
		model = Question
		fields = ('id', 'user', 'text', 'course', 'answears')


