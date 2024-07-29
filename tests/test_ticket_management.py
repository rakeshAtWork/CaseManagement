from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from ticket_management.models import Category

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


class CategoryCreateApiTest(BaseTestCase):
    def test_create_category_success(self):
        url = reverse('category_create')
        data = {
            "name": "Test Category"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Category')
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Test Category')
        self.assertEqual(Category.objects.get().created_by, self.user)

    def test_create_category_missing_name(self):
        url = reverse('category_create')
        data = {
            # Missing "name"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json()["error"])

    #
    def test_create_category_long_name(self):
        url = reverse('category_create')
        data = {
            "name": "A" * 151  # Assuming the max_length is 150
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.json()['error'])

    #
    def test_create_category_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        url = reverse('category_create')
        data = {
            "name": "Test Category"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #
    # def test_create_category_no_permission(self):
    #     # Assuming you have a permissions system and a user without permission
    #     self.client.credentials()  # Remove current credentials
    #     normal_user = User.objects.create_user('normal_user@gmail.com', 'normal@123')
    #     jwt_fetch_data = {
    #         'email': 'normal_user@gmail.com',
    #         'password': 'normal@123'
    #     }
    #
    #     url = reverse('token_obtain_pair')
    #     response = self.client.post(url, jwt_fetch_data, format='json')
    #     self.assertEqual(
    #         response.status_code, status.HTTP_200_OK, response.json()
    #     )
    #
    #     access_token = response.json()['access']
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    #
    #     url = reverse('category_create')
    #     data = {
    #         "name": "Test Category"
    #     }
    #
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
