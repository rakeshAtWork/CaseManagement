from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your tests here.
class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        username = "test@gmail.com"
        password = "test@123"
        self.user = User.objects.create_superuser(username, password)
        jwt_fetch_data = {
            'email': username,
            'password': password
        }

        url = reverse('token_obtain_pair')
        response = self.client.post(url, jwt_fetch_data, format='json')
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.json()
        )

        self.access_token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


