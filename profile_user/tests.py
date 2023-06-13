from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class ProfileAPITestCase(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.user = User.objects.create_user(username='dulal', password='Dulal@123')
        self.client.force_authenticate(user=self.user)

        image_path = '/home/user/Desktop/sat/profile3.jpeg'
        with open(image_path, 'rb') as f:
            image_data = f.read()

        self.image = SimpleUploadedFile(name=os.path.basename(image_path),content=image_data,content_type='image/jpeg')

    def test_create_profile(self):

        data = {
            'user': self.user.id,
            'name': 'dulal',
            'email': 'dulal@gmail.com',
            'bio': 'I am doing an internship in careers360',
            'profile_picture': self.image
        }

        response = self.client.post(reverse('profile'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().user, self.user)
        self.assertEqual(Profile.objects.get().name, 'dulal')

    def test_update_profile(self):

        profile = Profile.objects.create(user=self.user, name='dulal', email='dulal@gmail.com')
        updated_data = {

            'name': 'Dulal',
            'email': 'dulal@example.com',
            'bio': 'Iam doing internship in careers360(gurugram)',
            'profile_picture': self.image 
        }
        response = self.client.patch('/profile/', updated_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.name, 'Dulal')
        self.assertEqual(profile.email, 'dulal@example.com')
        self.assertEqual(profile.bio, 'Iam doing internship in careers360(gurugram)')

    def test_unauthenticated_access(self):

        self.client.logout() 
        response = self.client.post('/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.patch('/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)