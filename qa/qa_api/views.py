from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import viewsets
from qa_api.serializers import UserSerializer, QuestionSerializer, AnswearSerializer, CourseSerializer
from qa_api.models import Question

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class QuestionViewSet(viewsets.ModelViewSet):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

