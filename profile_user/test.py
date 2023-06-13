from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Profile
from django.urls import reverse


class ProfileAPITestCase(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.user = User.objects.create_user(username='dulal', password='Dulal@123')
        self.client.force_authenticate(user=self.user)

    def test_create_profile(self):

        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'dulal',
            'email': 'dulal@gmail.com',
            'bio': 'I am doing an internship in careers360',
            'profile_picture': None
        }

        response = self.client.post(reverse('profile'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().user, self.user)
        self.assertEqual(Profile.objects.get().name, 'dulal')

    def test_update_profile(self):

        self.client.force_authenticate(user=self.user)
        profile = Profile.objects.create(user=self.user, name='dulal', email='dulal@gmail.com')
        updated_data = {

            'name': 'Dulal',
            'email': 'dulal@example.com',
            'bio': 'Iam doing internship in careers360(gurugram)',
            'profile_picture': None 
        }
        response = self.client.patch('/profile/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.name, 'Dulal')
        self.assertEqual(profile.email, 'dulal@example.com')
        self.assertEqual(profile.bio, 'Iam doing internship in careers360(gurugram)')