"""
Authentication classes file
"""

"""
Imports
"""
# Models
from django.contrib.auth.models import User
from qa_api.models import FenixEduAPIUser

# Django authentication
from rest_framework import authentication
from rest_framework import exceptions

class CustomAuthentication(authentication.BaseAuthentication):
	def authenticate(self, request):
		# Receive the access token from the request
		access_token = request.GET.get('access_token')

		# Check if the access_token parameter is in the request
		if not access_token:
			# If not, authentication fails
			return None
		try:
			# Use that token to check if the user have requested an access token before
			fenix_api_user = FenixEduAPIUser.objects.get(access_token = access_token)
			
			# If a user exists with that token
			# Get the user object
			user = fenix_api_user.user
			# Authentication with success
			return (user, True)
		
		# Invalid token
		except FenixEduAPIUser.DoesNotExist:
			# Authentication fails
			raise exceptions.AuthenticationFailed('Invalid token')
