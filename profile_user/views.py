from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, User
from .serializers import UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .decorators.decorators import ApiKeyPermission
from .decorators.timer import timer

   
class UserRegistrationAPI(APIView):

    permission_classes=(ApiKeyPermission,)

    @timer
    def post(self, request, format=None):

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if User.objects.filter(phone_number=serializer.validated_data['phone_number']).exists():
                return Response({"message": "Phone number already registered"}, status=status.HTTP_302_FOUND)
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPI(APIView):

    permission_classes=(ApiKeyPermission,)
    
    @timer
    def post(self, request, format=None):

        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid():

            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({ 'token': token.key, 'msg': 'Login Successful' },status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status = status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    @timer
    def post(self, request):

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "profile detail entered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @timer
    def patch(self, request):

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response("Profile does not exist.", status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save(user=request.user)
            return Response({"message": "profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
