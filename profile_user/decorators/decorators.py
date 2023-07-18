from rest_framework import permissions
from django.conf import settings


class ApiKeyPermission(permissions.BasePermission):


	def has_permission(self, request, view):
		api_key = request.META.get('HTTP_X_API_KEY', "")
		print('api_key',api_key)
		print('==>>>>',settings.WEB_API_KEY)
		
		if api_key and api_key == settings.WEB_API_KEY:
			return True
		else:
			return False

	@property
	def message(self):
		response_dict = {}
		response_dict['status'] = 'error'
		response_dict['message'] = 'Invalid Key'
		return response_dict