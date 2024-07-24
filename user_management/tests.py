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


class UserRegisterTestCase(BaseTestCase):

    def test_user_register_success(self):
        url = reverse('register')
        data = {
            "first_name": "testing1",
            "last_name": "test",
            "phone_number": "9110161780",
            "email": "rakesh.raushan@cozentus.com",
            "organisation_name": "Cozentus",
            "timezone": "UTC",
            "country": "India"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])

    def test_user_register_invalid_email(self):
        url = reverse('register')
        data = {
            "first_name": "testing1",
            "last_name": "test",
            "phone_number": "9110161780",
            "email": "invalid-email",
            "organisation_name": "Cozentus",
            "timezone": "UTC",
            "country": "India"
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response_data)

    def test_user_register_duplicate_email(self):
        url = reverse('register')
        data1 = {
            "first_name": "testing1",
            "last_name": "test",
            "phone_number": "9110161780",
            "email": "duplicate@cozentus.com",
            "organisation_name": "Cozentus",
            "timezone": "UTC",
            "country": "India"
        }
        self.client.post(url, data1, format='json')

        # Attempt to register the same email again
        data2 = {
            "first_name": "testing2",
            "last_name": "test2",
            "phone_number": "9110161790",
            "email": "duplicate@cozentus.com",
            "organisation_name": "AnotherOrg",
            "timezone": "UTC",
            "country": "India"
        }
        response = self.client.post(url, data2, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response_data)

    def test_user_register_invalid_phone_number(self):
        url = reverse('register')
        data = {
            "first_name": "testing1",
            "last_name": "test",
            "phone_number": "invalid-phone",
            "email": "rakesh.raushan@cozentus.com",
            "organisation_name": "Cozentus",
            "timezone": "UTC",
            "country": "India"
        }
        response = self.client.post(url, data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response_data['error'])


# class UserRegisterTestCase(BaseTestCase):
#     def test_user_register(self):
#         url = reverse('register')
#         data = {
#             "first_name": "testing1",
#             "last_name": "test",
#             "phone_number": "9110161780",
#             "email": "abhilipsa@cozentus.com",
#             "organisation_name": "Cozentus",
#             "timezone": "UTC",
#             "country": "India"
#         }
#         response = self.client.post(url, data, format='json')
#         print("*****", response)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserLoginTestCase(BaseTestCase):
    def test_login_with_valid_credentials(self):
        # Arrange
        url = reverse('user-login')
        data = {
            'email': "test@gmail.com",
            'password': "test@123"
        }
        # Act
        response = self.client.post(url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response_data)
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Login successfully")

    def test_login_with_invalid_credentials(self):
        # Arrange
        url = reverse('user-login')

        # Invalid email
        data = {'email': "wrong@gmail.com", 'password': "test@123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Invalid password
        data = {'email': "test@gmail.com", 'password': "wrong@123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Empty fields
        data = {'email': "", 'password': ""}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expired_token(self):
        # This test needs a real expired token for a realistic test.
        # You may need to generate one or mock the token expiry logic.
        expired_token = "expired-token"  # Replace with a real expired token for the test
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')

        url = reverse('user-login')  # Replace with a real endpoint that requires authentication
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_invalid_token_format(self):
    #     # Arrange
    #     invalid_token = "invalid-token-format"
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {invalid_token}')
    #
    #     url = reverse('user-protected-endpoint')  # Replace with a real endpoint that requires authentication
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_login_response_structure(self):
    #     # Arrange
    #     url = reverse('user-login')
    #     data = {
    #         'email': "test@gmail.com",
    #         'password': "test@123"
    #     }
    #     # Act
    #     response = self.client.post(url, data, format='json')
    #     response_data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsInstance(response_data, dict)
    #     self.assertIn("access", response_data)
    #     self.assertIn("message", response_data)
    #     self.assertIsInstance(response_data["access"], str)
    #     self.assertEqual(response_data["message"], "Login successfully")
    #
    # def test_login_rate_limiting(self):
    #     # Arrange
    #     url = reverse('user-login')
    #     data = {
    #         'email': "test@gmail.com",
    #         'password': "test@123"
    #     }
    #     for _ in range(10):  # Adjust number as needed to exceed rate limits
    #         response = self.client.post(url, data, format='json')
    #         if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
    #             break
    #     self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
