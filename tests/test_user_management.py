from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from user_management.models import CustomUser
from acl.models import UserRole, Role
from django.core.cache import cache
from unittest.mock import patch
from django.utils import timezone

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
        # just create a new Role so that it can be tested.
        # before updating lets create a new role
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["VIEW_ROLE", "CREATE_DEPARTMENT", "VIEW_USER_LIST"]
        }
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")
        response_created = self.client.post(url, valid_payload, format='json')
        self.role_id = response_created.data['id']


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
            "country": "India",
            "role_id": self.role_id
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        # getting the role info:
        url = reverse('user_details', kwargs={'pk': response.data['id']})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['role_data']), 1)
        self.assertEqual(response.data['role_data'][0]['id'], data['role_id'])
        self.assertEqual(response.data['role_data'][0]['role_name'], "Admin")
        # print(response.data)

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

    def test_user_register_with_invalid_role_id(self):
        url = reverse('register')
        data = {
            "first_name": "testing1",
            "last_name": "test",
            "phone_number": "9110161780",
            "email": "rakesh.raushan@cozentus.com",
            "organisation_name": "Cozentus",
            "timezone": "UTC",
            "country": "India",
            "role_id": "Invalid-role-id"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertIn("error", response.data)

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


class UserLoginTestCase(BaseTestCase):
    def test_login_with_valid_credentials(self):
        # Arrange
        url = reverse('user_login')
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
        url = reverse('user_login')

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

        url = reverse('user_login')  # Replace with a real endpoint that requires authentication
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token_format(self):
        # Arrange
        invalid_token = "invalid-token-format"
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {invalid_token}')

        url = reverse('user_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserListTestCase(BaseTestCase):
    def test_get_user_list(self):
        response = self.client.post(reverse("user_list"), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['count'], 1)


class UserDetailApiTest(BaseTestCase):

    def setUp(self):
        super().setUp()

        # Creating test users
        self.user1 = CustomUser.objects.create(
            email="user1@example.com",
            first_name="John",
            last_name="Doe",
            is_active=True,
            is_delete=False,
            created_by=self.user.id
        )
        self.user2 = CustomUser.objects.create(
            email="user2@example.com",
            first_name="Jane",
            last_name="Smith",
            is_active=True,
            is_delete=False,
            created_by=self.user.id
        )

    def test_get_user_detail(self):
        # Test for retrieving a specific user's details
        url = reverse('user_details', kwargs={'pk': self.user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user1.id)
        self.assertEqual(response.data['first_name'], self.user1.first_name)
        self.assertEqual(response.data['last_name'], self.user1.last_name)

    def test_user_detail_not_found(self):
        # Test for a non-existent user
        url = reverse('user_details', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserJsonDataAPITest(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.url = reverse('user_details_json')

        # Creating test users
        self.user1 = CustomUser.objects.create(
            email="user1@example.com",
            first_name="John",
            last_name="Doe",
            is_active=True,
            is_delete=False,
            created_by=self.user.id
        )
        self.user2 = CustomUser.objects.create(
            email="user2@example.com",
            first_name="Jane",
            last_name="Smith",
            is_active=True,
            is_delete=False,
            created_by=self.user.id
        )

    def test_get_user_json_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)


class UserFilterApiTest(BaseTestCase):

    def setUp(self):
        super().setUp()

        # Creating test users
        self.user1 = CustomUser.objects.create(
            email="user1@example.com",
            first_name="John",
            last_name="Doe",
            is_active=True,
            is_delete=False,
            created_by=self.user.id
        )
        self.user2 = CustomUser.objects.create(
            email="user2@example.com",
            first_name="Jane",
            last_name="Smith",
            is_active=True,
            is_delete=False,
            created_by=self.user.id
        )

    def test_filter_users_by_email(self):
        # Test filtering users by email
        url = reverse('user_list')
        data = {
            'email': 'user1',
            'page_size': 10,
            'page': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], self.user1.email)

    def test_pagination(self):
        # Test pagination functionality
        url = reverse('user_list')
        data = {
            'page_size': 1,  # Only one user per page
            'page': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        # Request the next page
        data['page'] = 2
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_and_sort(self):
        # Test filtering by email and sorting by first_name
        url = reverse('user_list')
        data = {
            'order_by': 'first_name',
            'order_type': 'asc',
            'page_size': 10,
            'page': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_page_and_page_size(self):
        # Test invalid page and page_size
        url = reverse('user_list')
        data = {
            'page': -1,
            'page_size': 0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('page and page size should be positive integer', response.data['message'])


class UserOtpVerifyApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="password123")
        self.url = reverse('password_otp_verify')

    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    def test_otp_verify_success(self, mock_cache_set, mock_cache_get):
        mock_cache_get.return_value = 123456
        data = {
            "email": self.user.email,
            "otp": 123456
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], "Otp verify successfully")

    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    def test_otp_verify_invalid_otp(self, mock_cache_set, mock_cache_get):
        mock_cache_get.return_value = 123456
        data = {
            "email": self.user.email,
            "otp": 654321
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn('status', response.json())
        # self.assertEqual(response.json()['status'], "failure")
        self.assertIn('message', response.json())
        # self.assertEqual(response.json()['message'], "Invalid OTP")

    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    def test_otp_verify_invalid_email(self, mock_cache_set, mock_cache_get):
        mock_cache_get.return_value = None
        data = {
            "email": "invaliduser@example.com",
            "otp": 123456
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn('status', response.json())
        # self.assertEqual(response.json()['status'], "failure")
        self.assertIn('message', response.json())
        # self.assertEqual(response.json()['message'], "Invalid OTP")

    def test_otp_verify_missing_fields(self):
        data = {
            "email": self.user.email
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('otp', response.json())
        self.assertEqual(response.json()['otp'][0], "This field is required.")


class UserPasswordResetTestCase(APITestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.old_password = "old_password123"
        self.new_password = "new_password123"
        self.user = User.objects.create_user(email=self.email, password=self.old_password)
        self.reset_password_url = reverse('user_password_reset')
        # Simulate OTP verification in cache
        cache.set(f'{self.email}_verify', True, 120)  # Simulating OTP verification is done

    def test_password_reset_success(self):
        # Arrange
        data = {
            'email': self.email,
            'password': 'newpassword123'
        }

        # Act
        response = self.client.post(self.reset_password_url, data, format='json')

        # Print response for debugging
        print("Response content:", response.content)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_password_reset_invalid_otp(self):
        # Simulate expired or invalid OTP
        cache.delete(f'{self.email}_verify')

        data = {
            "email": self.email,
            "password": self.new_password
        }

        response = self.client.post(self.reset_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], "Password change time expired please retry new otp")

    def test_password_reset_password_validation_error(self):
        # Assuming '123' is a password that fails validation
        data = {
            "email": self.email,
            "password": "123"
        }

        response = self.client.post(self.reset_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertTrue('This password is too short.' in response.json()['message'])

    def test_password_reset_missing_fields(self):
        # Missing password field
        data = {
            "email": self.email
        }

        response = self.client.post(self.reset_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())


class UserUpdateApiTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user = CustomUser.objects.create(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            phone_number='+1234567890',
            organisation_name='Test Org',
            timezone='UTC',
            country='Country',
            is_active=True,
            created_by=1,
            created_on=timezone.now(),
        )
        self.role = Role.objects.create(role_name='Test Role')
        self.user_role = UserRole.objects.create(user=self.user, role=self.role, created_by='testuser@example.com')

        self.valid_payload = {
            'first_name': 'Updated',
            'last_name': 'User',
            'phone_number': '+10987654321',
            'email': 'updateduser@example.com',
            'organisation_name': 'Updated Org',
            'timezone': 'UTC',
            'country': 'Updated Country',
            'role_id': self.role.id,
            'is_active': True
        }
        self.invalid_payload = {
            'first_name': '',
            'last_name': '',
            'phone_number': 'invalid_phone',
            'email': 'invalid_email',
            'role_id': 'invalid_role_id'
        }
        self.patch_payload = {
            'first_name': 'Updated',
            'last_name': 'User',
            'phone_number': '+10987654321',
            'email': 'updateduser@example.com',
            'organisation_name': 'Updated Org'

        }

    def test_retrieve_user(self):
        response = self.client.get(reverse('user_detail_update', kwargs={'id': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.first_name)

    def test_update_user_valid(self):
        response = self.client.put(reverse('user_detail_update', kwargs={'id': self.user.id}), data=self.valid_payload,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.phone_number, '+10987654321')

    def test_update_user_invalid(self):
        response = self.client.put(reverse('user_detail_update', kwargs={'id': self.user.id}),
                                   data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, '')
        self.assertNotEqual(self.user.phone_number, 'invalid_phone')

    def test_partial_update_user(self):
        response = self.client.patch(reverse('user_detail_update', kwargs={'id': self.user.id}),
                                     data=self.patch_payload,
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        response = self.client.delete(reverse('user_detail_update', kwargs={'id': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_delete)


class UserFilterAPITestCase(BaseTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password',
            first_name='Test',
            last_name='User',
            organisation_name='TestOrg',
            phone_number='1234567890'
        )
        self.url = reverse('user_list')  # Ensure the URL name matches

    def test_user_filter_success(self):
        # Sample payload for testing
        payload = {
            "page_size": 10,
            "page": 1

        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_user_filter_invalid_page_size(self):
        payload = {
            "page_size": -10,  # Invalid page size
            "page": 1
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "page and page size should be positive integer")

    def test_user_filter_no_results(self):
        payload = {
            "page_size": 10,
            "page": 1,
            "email": "nonexistentuser@example.com"
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)


class UserStatusApiViewTest(BaseTestCase):

    def setUp(self):
        # Create a superuser to use for authentication
        self.superuser = User.objects.create_superuser(
            email='superuser@example.com',
            password='superpassword'
        )

        # Create a normal user to be used in tests
        self.user = User.objects.create_user(
            email='user@example.com',
            password='userpassword',
            is_active=False,
            is_delete=False
        )

        self.client.force_authenticate(user=self.superuser)

    def test_activate_user(self):
        """
        Ensure we can activate a user.
        """
        url = reverse('user_status', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, data={'is_active': True}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_deactivate_user(self):
        """
        Ensure we can deactivate a user.
        """
        self.user.is_active = True
        self.user.save()

        url = reverse('user_status', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, data={'is_active': False}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_cannot_modify_self(self):
        """
        Ensure a user cannot modify their own status.
        """
        url = reverse('user_status', kwargs={'pk': self.superuser.pk})
        response = self.client.patch(url, data={'is_active': False}, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.superuser.refresh_from_db()
        self.assertTrue(self.superuser.is_active)
        # self.assertIn("You can't perform this operation with yourself", response.data['msg'])

    def test_user_not_found(self):
        """
        Ensure proper error response if user not found.
        """
        url = reverse('user_status', kwargs={'pk': 999})
        response = self.client.patch(url, data={'is_active': False}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# adding the remaining test cases which api end point may not be in use.
