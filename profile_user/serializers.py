from rest_framework import serializers
from .models import Profile, User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'bio', 'profile_picture']

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','phone_number', 'password','confirm_password']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('confirm_password')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields=['email','password']