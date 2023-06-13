from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated

class UserProfileAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):

        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response("Profile does not exist.", status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
