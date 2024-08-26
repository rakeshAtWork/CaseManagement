from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model

from master_data_management.models import Category, Department, UserDepartment, Status, Currency, Country, \
    EmailTemplate, FileType, BusinessUnit, Application, Client
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
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")
        response_created = self.client.post(url, valid_payload, format='json')
        self.role_id = response_created.data['id']


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


class CategoryFilterApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        Category.objects.create(name="Test Category 1", created_by=self.user)
        Category.objects.create(name="Test Category 2", created_by=self.user)
        Category.objects.create(name="Another Category", created_by=self.user)

    def test_filter_category_success(self):
        url = reverse('category_list')
        data = {
            "category_name": "Test"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn("Test Category 1", [category['name'] for category in response.data['results']])
        self.assertIn("Test Category 2", [category['name'] for category in response.data['results']])

    def test_pagination(self):
        url = reverse('category_list')
        data = {
            "page_size": 1,
            "page": 1
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['count'], 3)

    def test_invalid_page_and_page_size(self):
        url = reverse('category_list')
        data = {
            "page_size": -1,
            "page": -1
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "page and page size should be positive integer")

    def test_non_existent_category_name(self):
        url = reverse('category_list')
        data = {
            "category_name": "NonExistentCategory"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_unauthenticated_request(self):
        self.client.credentials()  # Remove authentication
        url = reverse('category_list')
        data = {
            "category_name": "Test"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryUpdateApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name="Initial Category", created_by=self.user)

    def test_update_category_success(self):
        url = reverse('category_update', kwargs={'pk': self.category.id})
        data = {
            "name": "Updated Category"
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Category')
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_update_category_missing_name(self):
        url = reverse('category_update', kwargs={'pk': self.category.id})
        data = {
            "name": ""
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error'])

    def test_update_category_long_name(self):
        url = reverse('category_update', kwargs={'pk': self.category.id})
        data = {
            "name": "A" * 151  # Assuming the max_length is 150
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error'])

    def test_update_category_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        url = reverse('category_update', kwargs={'pk': self.category.id})
        data = {
            "name": "Updated Category"
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_category_success(self):
        url = reverse('category_update', kwargs={'pk': self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())

    def test_delete_category_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        url = reverse('category_update', kwargs={'pk': self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_non_existent_category(self):
        url = reverse('category_update', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DepartmentCreateApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a category to use as department_type
        # self.category = Category.objects.create(
        #     name="IT",
        # )
        self.create_url = reverse('department_create')

    def test_create_department_success(self):
        data = {
            "department_name": "Engineering",
            "department_code": "ENG001"
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['department_name'], "Engineering")
        self.assertEqual(response.data['department_code'], "ENG001")

    def test_create_department_invalid_data(self):
        data = {
            "department_name": "",  # Invalid name
            "department_code": "ENG001",
            # "department_type": self.category.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('department_name', response.data['error'])

    def test_create_department_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "department_name": "Engineering",
            "department_code": "ENG001",
            # "department_type": self.category.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DepartmentFilterApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create categories to use for department_type
        # self.category1 = Category.objects.create(name="HR")
        # self.category2 = Category.objects.create(name="IT")

        # Create departments to test filtering
        self.department1 = Department.objects.create(
            department_name="Human Resources",
            department_code="HR001",
            # department_type=self.category1,
            created_by=self.user
        )
        self.department2 = Department.objects.create(
            department_name="Information Technology",
            department_code="IT001",
            # department_type=self.category2,
            created_by=self.user
        )

        self.filter_url = reverse('department_list')

    def test_filter_department_success(self):
        data = {
            # without any payload
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Two departments should be returned
        # print(response.data)

    def test_filter_department_invalid_page(self):
        data = {
            "name": "Human",
            "order_by": "name",
            "order_type": "asc",
            "page_size": 1,
            "page": -1  # Invalid page number
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "page and page size should be positive integer")

    def test_filter_department_no_results(self):
        data = {
            "name": "Nonexistent",
            "order_by": "name",
            "order_type": "asc",
            "page_size": 10,
            "page": 1
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_filter_department_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "department_name": "Human",
            "order_by": "department_name",
            "order_type": "asc",
            "page_size": 10,
            "page": 1
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_department_is_active(self):
        # for active
        data = {
            "is_active": True
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        # for inactive
        data = {
            "is_active": False
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


class DepartmentUpdateApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create categories to use for department_type
        # self.category = Category.objects.create(name="HR")

        # Create a department to test update and delete
        self.department = Department.objects.create(
            department_name="Human Resources",
            department_code="HR001",
            # department_type=self.category,
            created_by=self.user
        )

        self.update_url = reverse('department_update', args=[self.department.id])

    def test_update_department_success(self):
        data = {
            "department_name": "HR & Admin",
            "department_code": "HR002",
            # "department_type": self.category.id
        }
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.department_name, "HR & Admin")
        self.assertEqual(self.department.department_code, "HR002")

    def test_update_department_partial_success(self):
        data = {
            "department_name": "Admin"
        }
        response = self.client.patch(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.department_name, "Admin")

    def test_update_department_invalid_id(self):
        invalid_url = reverse('department_update', args=[999])
        data = {
            "department_name": "Admin"
        }
        response = self.client.put(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_department_success(self):
        response = self.client.delete(self.update_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Department.objects.filter(id=self.department.id).exists())

    def test_delete_department_invalid_id(self):
        invalid_url = reverse('department_update', args=[999])
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_department_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "department_name": "HR & Admin"
        }
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_department_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.delete(self.update_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDepartmentApiTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Creating test users and departments
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='password',
            first_name='John',
            last_name='Doe'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='password',
            first_name='Jane',
            last_name='Smith'
        )
        # self.category1 = Category.objects.create(name="HR")
        # self.category2 = Category.objects.create(name="IT")

        self.department1 = Department.objects.create(
            department_name='HR',
            department_code='HR01',
            # department_type=self.category1
        )
        self.department2 = Department.objects.create(
            department_name='Finance',
            department_code='FIN01',
            # department_type=self.category2
        )

        self.user_department1 = UserDepartment.objects.create(
            user=self.user1,
            department=self.department1,
            created_by=self.user1
        )
        self.user_department2 = UserDepartment.objects.create(
            user=self.user2,
            department=self.department2,
            created_by=self.user2
        )

    def test_get_user_department_list(self):
        url = reverse('department_user')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_department_id(self):
        url = reverse('department_user')
        response = self.client.get(url, {'department_id': self.department1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_user_id(self):
        url = reverse('department_user')
        response = self.client.get(url, {'user_id': self.user2.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_department(self):
        url = reverse('department_user')
        data = {
            'user': self.user1.id,
            'department': self.department2.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserDepartment.objects.count(), 3)  # One more department created

    def test_invalid_create_user_department(self):
        url = reverse('department_user')
        data = {
            'user': self.user1.id,  # Missing department
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('department', response.data['error'])


class StatusApiTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.status_data = {
            "name": "Open",
            "status_code": 5,
            "color_code": "#FFFFFF",
            "highlight": 1

        }
        self.status = Status.objects.create(**self.status_data)
        self.status_create_url = reverse('status_create')
        self.status_update_url = reverse('status_update', kwargs={'pk': self.status.id})
        self.status_list_url = reverse('status_list')

    def test_create_status(self):
        data = {
            "name": "Closed",
            "status_code": 5,
            "color_code": "#000000",
            "highlight": 1
        }
        response = self.client.post(self.status_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Closed')
        self.assertEqual(Status.objects.count(), 2)

    def test_update_status(self):
        data = {
            "name": "In Progress",
            "status_code": 10,
            "color_code": "#FF5733",
            "highlight": 1
        }
        response = self.client.put(self.status_update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "In Progress")
        self.assertEqual(self.status.status_code, 10)

    def test_partial_update_status(self):
        data = {
            "name": "On Hold"
        }
        response = self.client.patch(self.status_update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "On Hold")

    def test_delete_status(self):
        response = self.client.delete(self.status_update_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Status.objects.count(), 0)

    def test_list_status(self):
        response = self.client.post(self.status_list_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


# TestCase for Country
class CountryApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url_create = reverse('country_create')
        self.valid_data = {
            "country_name": "India",
            "country_code": "IN",
            "description": "Country in South Asia",
            "is_active": True
        }

    def test_country_create_success(self):
        response = self.client.post(self.url_create, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['country_name'], self.valid_data['country_name'])

    def test_country_create_with_existing_name(self):
        # First create a country
        response = self.client.post(self.url_create, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try creating the same country again
        response = self.client.post(self.url_create, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'country with country_name country name already exists.')

    def test_country_create_with_missing_country_name(self):
        invalid_data = self.valid_data.copy()
        del invalid_data['country_name']  # Remove country_name from the data

        response = self.client.post(self.url_create, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertIn('country_name', response.json()['error'])

    def test_country_create_with_invalid_country_code(self):
        invalid_data = self.valid_data.copy()
        invalid_data['country_code'] = ''  # Empty country code

        response = self.client.post(self.url_create, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertIn('country_code', response.json()['error'])

    # def test_country_create_with_invalid_user(self):
    #     # Simulate an unauthorized user by not providing the token
    #     self.client.credentials()  # Remove the token
    #     response = self.client.post(self.url_create, self.valid_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertIn('detail', response.json())
    #     self.assertEqual(response.json()['message'], 'Authentication credentials were not provided.')

    def test_country_update(self):
        update_data = {
            "country_name": "Updated Country",
            "updated_by": self.user.id
        }
        response = self.client.patch(self.country_modify_url, update_data, format='json')
        print(response.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.country.refresh_from_db()
        self.assertEqual(self.country.country_name, "Updated Country")

    def test_country_filter(self):
        filter_data = {
            "country_name": "Test",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(self.country_filter_url, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['country_name'], "Test Country")


class CountryFilterApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        Country.objects.create(country_name="Test Country 1", created_by=self.user.id)
        Country.objects.create(country_name="Test Country 2", created_by=self.user.id)
        Country.objects.create(country_name="Another Country", created_by=self.user.id)

    def test_filter_country_success(self):
        url = reverse('country_filter')
        data = {
            "country_name": "Test"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn("Test Country 1", [country['country_name'] for country in response.data['results']])
        self.assertIn("Test Country 2", [country['country_name'] for country in response.data['results']])

    def test_pagination(self):
        url = reverse('country_filter')
        data = {
            "page_size": 1,
            "page": 1
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['count'], 3)

    def test_invalid_page_and_page_size(self):
        url = reverse('country_filter')
        data = {
            "page_size": -1,
            "page": -1
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "page and page size should be positive integers")

    def test_non_existent_country_name(self):
        url = reverse('country_filter')
        data = {
            "country_name": "NonExistentCountry"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_unauthenticated_request(self):
        self.client.credentials()  # Remove authentication
        url = reverse('country_filter')
        data = {
            "country_name": "Test"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CountryUpdateApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.country = Country.objects.create(country_name="Initial Country", created_by=self.user.id)

    def test_update_country_success(self):
        url = reverse('country_detail', kwargs={'pk': self.country.id})
        data = {
            "country_name": "Updated Country Name",
            "country_code": "NEWCODE",
            "description": "Updated description"
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['country_name'], 'Updated Country Name')
        self.assertEqual(response.data['country_code'], 'NEWCODE')
        self.country.refresh_from_db()
        self.assertEqual(self.country.country_name, 'Updated Country Name')
        self.assertEqual(self.country.country_code, 'NEWCODE')

    def test_update_country_missing_name(self):
        url = reverse('country_detail', kwargs={'pk': self.country.id})
        data = {
            "country_name": ""
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('country_name', response.data['error'])

    def test_update_country_duplicate_name(self):
        # Create another country with a different name
        Country.objects.create(country_name="Another Country", created_by=self.user.id)

        url = reverse('country_detail', kwargs={'pk': self.country.id})
        data = {
            "country_name": "Another Country"
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('country_name', response.data['error'])

    # def test_update_country_unauthenticated(self):
    #     self.client.credentials()  # Remove authentication
    #     url = reverse('country_detail', kwargs={'pk': self.country.id})
    #     data = {
    #         "country_name": "Updated Country"
    #     }
    #
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_country_success(self):
        url = reverse('country_detail', kwargs={'pk': self.country.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the object is marked as deleted
        self.assertTrue(Country.objects.filter(id=self.country.id, is_delete=True).exists())
        self.assertFalse(Country.objects.filter(id=self.country.id, is_delete=False).exists())

    # def test_delete_non_existent_country(self):
    #     url = reverse('country_detail', kwargs={'pk': 999})
    #
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data['message'], "No Country matches the given query.")


# TestCase for Currency
class CurrencyApiTestCase(BaseTestCase):
    def setUp(self):
        self.currency_create_url = reverse('currency_create')
        self.currency_modify_url = reverse('currency_detail', args=[1])
        self.currency_filter_url = reverse('currency_filter')

        self.currency_data = {
            "currency_name": "Test Currency",
            "currency_code": "TCU",
            "created_by": 1
        }

        self.currency = Currency.objects.create(**self.currency_data)

    def test_currency_create(self):
        response = self.client.post(self.currency_create_url, self.currency_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Currency.objects.count(), 2)

    def test_currency_update(self):
        update_data = {
            "currency_name": "Updated Currency",
            "updated_by": 1
        }
        response = self.client.patch(self.currency_modify_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.currency.refresh_from_db()
        self.assertEqual(self.currency.currency_name, "Updated Currency")

    def test_currency_delete(self):
        response = self.client.delete(self.currency_modify_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.currency.refresh_from_db()
        self.assertFalse(self.currency.is_active)

    def test_currency_filter(self):
        filter_data = {"currency_name": "Test"}
        response = self.client.post(self.currency_filter_url, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class EmailTemplateListCreateApiTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('email_template_list_create')

    def test_list_email_templates(self):
        # Create a few email templates
        EmailTemplate.objects.create(
            template_type='ACCOUNT_ACTIVE',
            subject='Account Activated',
            email_to='##user_email##',
            message='Welcome!##user_name##'
        )
        EmailTemplate.objects.create(
            template_type='WELCOME',
            subject='Welcome!',
            email_to='##user_email##',
            message='Hello ##user_name##!'
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['template_type'], 'ACCOUNT_ACTIVE')
        self.assertEqual(response.data[1]['template_type'], 'WELCOME')

    def test_create_email_template(self):
        payload = {
            'template_type': 'RESET_PASSWORD',
            'subject': 'Password Reset Request',
            'email_to': '##user_email##',
            'message': 'Use this link to reset your password: ##reset_link##, User name is ##user_name##',
            'signature': 'Support Team'
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)
        self.assertEqual(EmailTemplate.objects.count(), 1)
        self.assertEqual(EmailTemplate.objects.get().template_type, 'RESET_PASSWORD')
        self.assertEqual(EmailTemplate.objects.get().subject, 'Password Reset Request')

    def test_create_email_template_without_shortcode_in_email_to(self):
        payload = {
            'template_type': 'STATUS_UPDATE',
            'subject': 'Status Update',
            'email_to': 'invalidemail@example.com',  # No shortcode
            'message': 'Your status has been updated.',
            'signature': 'Support Team'
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print(response.data)
        self.assertIn('email_to', response.data['error'])
        self.assertEqual('The email_to field must contain at least one valid shortcode.', response.data['message'])

    def test_create_email_template_with_invalid_cc(self):
        payload = {
            'template_type': 'TICKET_UPDATE',
            'subject': 'Ticket Update',
            'email_to': '##user_email##',
            'cc': 'invalidemail@example.com',  # No shortcode in cc
            'message': 'Your ticket has been updated.',
            'signature': 'Support Team'
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print(response.data)
        self.assertIn('cc', response.data['error'])
        self.assertEqual('The cc field must contain at least one valid shortcode.', response.data['message'])

    def test_create_email_template_with_invalid_bcc(self):
        payload = {
            'template_type': 'TICKET_UPDATE',
            'subject': 'Ticket Update',
            'email_to': '##user_email##',
            'bcc': 'invalidemail@example.com',  # No shortcode in bcc
            'message': 'Your ticket has been updated.',
            'signature': 'Support Team'
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print(response.data)
        self.assertIn('bcc', response.data['error'])
        self.assertEqual('The bcc field must contain at least one valid shortcode.', response.data['message'])

    def test_create_duplicate_email_template_type(self):
        # Create an initial template
        EmailTemplate.objects.create(
            template_type='WELCOME',
            subject='Welcome Email',
            email_to='##user_email##',
            message='Welcome to the platform!'
        )

        # Attempt to create a duplicate template type
        payload = {
            'template_type': 'WELCOME',
            'subject': 'Another Welcome Email',
            'email_to': '##user_email##',
            'message': 'Welcome again!',
            'signature': 'Support Team'
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print(response.data)
        self.assertIn('template_type', response.data['error'])
        self.assertEqual('email template with template_type template type already exists.', response.data['message'])


class EmailTemplateRetrieveUpdateDestroyApiTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create an email template that can be used for testing
        self.email_template = EmailTemplate.objects.create(
            template_type='WELCOME',
            subject='Welcome Email',
            email_to='##user_email##',
            cc='##creator_email##',
            bcc='##follower_email##',
            message='Welcome to the platform! ##user_email##',
            signature='Support Team',
            created_by=self.user
        )
        self.url = reverse('email_template_detail', kwargs={'pk': self.email_template.pk})

    def test_retrieve_email_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['template_type'], 'WELCOME')
        self.assertEqual(response.data['subject'], 'Welcome Email')

    def test_update_email_template(self):
        payload = {
            'template_type': 'WELCOME',
            'email_to': '##user_email##',
            'subject': 'Updated Welcome Email',
            'message': 'Welcome to our updated platform! ##user_email##',
            'cc': '##queue_manager_email##',  # Valid shortcodes in list format
            'bcc': '##assigned_to_email##',  # Valid shortcodes in list format
            'signature': 'The Support Team'
        }

        response = self.client.put(self.url, payload, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.email_template.refresh_from_db()
        self.assertEqual(self.email_template.subject, 'Updated Welcome Email')
        self.assertEqual(self.email_template.message, 'Welcome to our updated platform! ##user_email##')
        self.assertEqual(self.email_template.updated_by, self.user)
        self.assertAlmostEqual(self.email_template.updated_on, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_partial_update_email_template(self):
        payload = {
            'subject': 'Partially Updated Subject',
        }

        response = self.client.patch(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.email_template.refresh_from_db()
        self.assertEqual(self.email_template.subject, 'Partially Updated Subject')
        self.assertEqual(self.email_template.updated_by, self.user)
        self.assertAlmostEqual(self.email_template.updated_on, timezone.now(), delta=timezone.timedelta(seconds=1))

    def test_delete_email_template(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(EmailTemplate.objects.filter(pk=self.email_template.pk).exists())

    def test_update_email_template_invalid_shortcodes(self):
        payload = {
            'subject': 'Invalid Shortcodes Test',
            'cc': ['invalidemail@example.com'],  # Invalid shortcode
        }

        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cc', response.data['error'])

    def test_update_email_template_with_duplicate_template_type(self):
        # Create another template with a different type
        EmailTemplate.objects.create(
            template_type='RESET_PASSWORD',
            subject='Reset Password',
            email_to='##user_email##',
            message='Please reset your password using the following link.',
            created_by=self.user
        )

        # Try to update the existing template to have the same template_type as the new one
        payload = {
            'template_type': 'RESET_PASSWORD',
        }

        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.data)
        self.assertIn('template_type', response.data['error'])
        self.assertEqual('email template with template_type template type already exists.', response.data['message'])


class EmailTemplateFilterApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create EmailTemplate instances
        self.template1 = EmailTemplate.objects.create(
            template_type='WELCOME',
            subject='Welcome to Our Service',
            email_to='user1@example.com',
            cc='cc1@example.com',
            bcc='bcc1@example.com',
            message='Hello ##user_name##, welcome!',
            signature='Best Regards'
        )

        self.template2 = EmailTemplate.objects.create(
            template_type='RESET_PASSWORD',
            subject='Reset Your Password',
            email_to='user2@example.com',
            cc='cc2@example.com',
            bcc='bcc2@example.com',
            message='Hello ##user_name##, reset your password here.',
            signature='Support Team'
        )

        self.url = reverse('email_template_list_filter')

    def test_filter_email_templates(self):
        # Test filtering email templates by template type
        data = {
            'template_type': 'WELCOME',
            'order_by': 'subject',
            'order_type': 'asc',
            'page': 1,
            'page_size': 10
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['template_type'], 'WELCOME')

    def test_pagination(self):
        # Test pagination with more than one page
        data = {
            'page': 1,
            'page_size': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 1)

    def test_invalid_page(self):
        # Test with invalid page number
        data = {
            'page': 3,  # More than available pages
            'page_size': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Page not found')

    def test_empty_filter(self):
        # Test with empty filter (should return all)
        data = {
            'page': 1,
            'page_size': 10
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)


class FileTypeCreateApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()  # Calls the BaseTestCase setup for authentication
        self.url = reverse('file_type')

        # Prepare valid payload for file type creation
        self.valid_payload = {
            "status": True,
            "file_type": "Document",
            "file_extension": "PDF",
            "max_file_size": 1024,
            "file_description": "PDF documents"
        }

    def test_create_file_type_valid(self):
        """
        Test creating a file type with valid data.
        """
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FileType.objects.count(), 1)
        file_type = FileType.objects.get()
        self.assertEqual(file_type.file_type, self.valid_payload['file_type'])
        # self.assertEqual(file_type.file_extension, self.valid_payload['file_extension'].lower())
        # self.assertEqual(file_type.max_file_size, self.valid_payload['max_file_size'])

    def test_create_file_type_duplicate_extension(self):
        """
        Test creating a file type with a duplicate file extension.
        """
        # Create the first FileType instance
        self.client.post(self.url, self.valid_payload, format='json')

        # Attempt to create another with the same file extension
        duplicate_payload = self.valid_payload.copy()
        response = self.client.post(self.url, duplicate_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FileType.objects.count(), 1)
        # self.assertIn("File extension name should be unique", response.data['non_field_errors'])

    def test_create_file_type_invalid_extension(self):
        """
        Test creating a file type with an invalid file extension containing special characters.
        """
        invalid_payload = self.valid_payload.copy()
        invalid_payload['file_extension'] = "PDF*"

        response = self.client.post(self.url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(FileType.objects.count(), 0)
        # self.assertIn("File extension should not contain any special characters", response.data['file_extension'])

    def test_create_file_type_missing_required_fields(self):
        """
        Test creating a file type with missing required fields.
        """
        invalid_payload = self.valid_payload.copy()
        del invalid_payload['file_type']  # Remove required field

        response = self.client.post(self.url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(FileType.objects.count(), 0)
        # self.assertIn("This field is required.", response.data['file_type'])


class FileTypeModifyApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()  # Calls the BaseTestCase setup for authentication

        # Create an initial FileType instance for testing modify operations
        self.file_type_instance = FileType.objects.create(
            status=True,
            file_type="Document",
            file_extension="PDF",
            max_file_size=1024,
            file_description="PDF documents",
            created_by=self.user.id
        )
        self.url = reverse('file_type_modify', kwargs={'pk': self.file_type_instance.id})

    def test_retrieve_file_type(self):
        """
        Test retrieving a file type by ID.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_type'], self.file_type_instance.file_type)
        self.assertEqual(response.data['file_extension'], self.file_type_instance.file_extension)

    def test_update_file_type(self):
        """
        Test updating a file type with new data.
        """
        update_payload = {
            "status": False,
            "file_type": "Updated Document",
            "file_extension": "DOCX",
            "max_file_size": 2048,
            "file_description": "Updated description"
        }

        response = self.client.put(self.url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.file_type_instance.refresh_from_db()
        self.assertEqual(self.file_type_instance.file_type, update_payload['file_type'])
        # self.assertEqual(self.file_type_instance.file_extension, update_payload['file_extension'].lower())
        # self.assertEqual(self.file_type_instance.max_file_size, update_payload['max_file_size'])

    def test_partial_update_file_type(self):
        """
        Test partially updating a file type.
        """
        partial_update_payload = {
            "file_description": "Partially updated description"
        }

        response = self.client.patch(self.url, partial_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.file_type_instance.refresh_from_db()
        self.assertEqual(self.file_type_instance.file_description, partial_update_payload['file_description'])

    def test_delete_file_type(self):
        """
        Test deleting a file type.
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FileType.objects.filter(id=self.file_type_instance.id).exists())

    def test_update_file_type_invalid_extension(self):
        """
        Test updating a file type with an invalid file extension containing special characters.
        """
        invalid_update_payload = {
            "file_extension": "DOCX*"
        }

        response = self.client.put(self.url, invalid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn("File extension should not contain any special characters", response.data['file_extension'])

    def test_update_file_type_duplicate_extension(self):
        """
        Test updating a file type to a duplicate file extension.
        """
        # Create another FileType instance with the same file_extension
        FileType.objects.create(
            status=True,
            file_type="Another Document",
            file_extension="DOCX",
            max_file_size=512,
            file_description="Another document",
            created_by=self.user.id
        )

        # Attempt to update the original file type to the same file_extension
        duplicate_extension_payload = {
            "file_extension": "DOCX"
        }

        response = self.client.put(self.url, duplicate_extension_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn("File extension name should be unique", response.data['non_field_errors'])


class FileTypeFilterApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()  # Calls the BaseTestCase setup for authentication

        # Create multiple FileType instances for testing
        self.file_types = [
            FileType.objects.create(
                status=True,
                file_type="Document1",
                file_extension="PDF",
                max_file_size=1024,
                file_description="Description1",
                created_by=self.user.id
            ),
            FileType.objects.create(
                status=False,
                file_type="Document2",
                file_extension="DOCX",
                max_file_size=2048,
                file_description="Description2",
                created_by=self.user.id
            ),
            FileType.objects.create(
                status=True,
                file_type="Document3",
                file_extension="XLSX",
                max_file_size=3072,
                file_description="Description3",
                created_by=self.user.id
            )
        ]
        self.url = reverse('file_type_filter')

    def test_filter_file_type_by_status(self):
        """
        Test filtering file types by status.
        """
        filter_payload = {
            "status": True
        }

        response = self.client.post(self.url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertTrue(all(item['status'] == True for item in response.data['results']))

    def test_filter_file_type_by_file_type(self):
        """
        Test filtering file types by file_type.
        """
        filter_payload = {
            "file_type": "Document1"
        }

        response = self.client.post(self.url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['file_type'], "Document1")

    def test_pagination(self):
        """
        Test pagination of file types.
        """
        filter_payload = {
            "page": 1,
            "page_size": 2
        }

        response = self.client.post(self.url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], len(self.file_types))

    def test_order_by_file_type(self):
        """
        Test ordering file types by file_type.
        """
        filter_payload = {
            "order_by": "file_type",
            "order_type": "asc"
        }

        response = self.client.post(self.url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        file_types = [ft['file_type'] for ft in results]
        self.assertEqual(file_types, sorted(file_types))

    def test_order_by_file_type_desc(self):
        """
        Test ordering file types by file_type in descending order.
        """
        filter_payload = {
            "order_by": "file_type",
            "order_type": "desc"
        }

        response = self.client.post(self.url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        file_types = [ft['file_type'] for ft in results]
        self.assertEqual(file_types, sorted(file_types, reverse=True))

    def test_invalid_page_and_page_size(self):
        """
        Test handling of invalid page and page_size values.
        """
        filter_payload = {
            "page": -1,
            "page_size": 0
        }

        response = self.client.post(self.url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "page and page size should be positive integer")

    def test_page_not_found(self):
        """
        Test handling of page number that exceeds available pages.
        """
        filter_payload = {
            "page": 9999,
            "page_size": 2
        }

        response = self.client.post(self.url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Page not found")

    def test_invalid_export_option(self):
        """
        Test handling of invalid export option.
        """
        filter_payload = {
            "export": "invalid_option"
        }

        response = self.client.post(self.url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn("Invalid export option", response.data.get('message', ''))


# Test cases for Business Unit
class BusinessUnitApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.create_url = reverse('business_unit')

    def test_create_business_unit_valid(self):
        data = {
            "client_id": "Client1",
            "code": "Code1",
            "name": "Business Unit 1",
            "contact_name": "John Doe",
            "contact_email": "john.doe@example.com",
            "contact_number": "1234567890"
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BusinessUnit.objects.count(), 1)
        self.assertEqual(BusinessUnit.objects.get().name, "Business Unit 1")

    def test_create_business_unit_invalid(self):
        data = {
            "client_id": "Client1",
            "code": "Code1",
            "name": "",
            "contact_name": "John Doe",
            "contact_email": "john.doe@example.com",
            "contact_number": "1234567890"
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BusinessUnitModifyApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.business_unit = BusinessUnit.objects.create(
            client_id="Client1",
            code="Code1",
            name="Business Unit 1",
            contact_name="John Doe",
            contact_email="john.doe@example.com",
            contact_number="1234567890",
            created_by=self.user.id
        )
        self.modify_url = reverse('business_unit_modify', args=[self.business_unit.id])

    def test_get_business_unit(self):
        response = self.client.get(self.modify_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Business Unit 1")

    def test_update_business_unit(self):
        # Update with valid email format
        data = {
            "code": "UpdatedCode",
            "name": "Updated Business Unit",
            "contact_name": "Updated Contact Name",
            "contact_number": "0987654321"
        }
        response = self.client.put(self.modify_url, data, format='json')

        # Print debugging output if the response status is not OK
        if response.status_code != status.HTTP_200_OK:
            print("Response Status Code:", response.status_code)
            print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.business_unit.refresh_from_db()
        self.assertEqual(self.business_unit.name, "Updated Business Unit")

    def test_delete_business_unit(self):
        response = self.client.delete(self.modify_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BusinessUnit.objects.filter(id=self.business_unit.id).exists())


class BusinessUnitFilterApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.business_unit1 = BusinessUnit.objects.create(
            client_id="Client1",
            code="Code1",
            name="Business Unit 1",
            contact_name="John Doe",
            contact_email="john.doe@example.com",
            contact_number="1234567890",
            created_by=self.user.id
        )
        self.business_unit2 = BusinessUnit.objects.create(
            client_id="Client2",
            code="Code2",
            name="Business Unit 2",
            contact_name="Jane Doe",
            contact_email="jane.doe@example.com",
            contact_number="0987654321",
            created_by=self.user.id
        )
        self.filter_url = reverse('business_unit_filter')

    def test_filter_business_units(self):
        data = {
            "name": "Business Unit 1",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], "Business Unit 1")

    def test_filter_business_units_invalid_page(self):
        data = {
            "page": -1,
            "page_size": 10
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ApplicationApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('application')

    def test_create_application_success(self):
        """
        Test successful creation of an Application instance.
        """
        payload = {
            "status": True,
            "code": "APP123",
            "name": "Test Application",
            "contact_name": "John Doe",
            "contact_email": "john.doe@example.com",
            "contact_number": "1234567890"
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.get().name, "Test Application")
        self.assertEqual(Application.objects.get().created_by, self.user.id)

    def test_create_application_missing_fields(self):
        """
        Test creating an Application instance with missing required fields.
        """
        payload = {
            "status": True
            # Missing 'code', 'name', 'contact_name', 'contact_email', 'contact_number'
        }

        response = self.client.post(self.url, payload, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # look this
        # self.assertIn('code', response.data)
        # self.assertIn('name', response.data)
        # self.assertIn('contact_name', response.data)
        # self.assertIn('contact_email', response.data)
        # self.assertIn('contact_number', response.data)

    def test_create_application_invalid_email(self):
        """
        Test creating an Application instance with an invalid email address.
        """
        payload = {
            "status": True,
            "code": "APP123",
            "name": "Test Application",
            "contact_name": "John Doe",
            "contact_email": "invalid-email",
            "contact_number": "1234567890"
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('contact_email', response.data['error'])

    def test_create_application_without_authentication(self):
        """
        Test creating an Application instance without authentication.
        """
        self.client.credentials()  # Remove authentication
        payload = {
            "status": True,
            "code": "APP123",
            "name": "Test Application",
            "contact_name": "John Doe",
            "contact_email": "john.doe@example.com",
            "contact_number": "1234567890"
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_application_with_invalid_data(self):
        """
        Test creating an Application instance with invalid data.
        """
        payload = {
            "status": "not_a_boolean",  # Invalid data type
            "code": "APP123",
            "name": "Test Application",
            "contact_name": "John Doe",
            "contact_email": "john.doe@example.com",
            "contact_number": "1234567890"
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data['error'])


class ApplicationModifyApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Create an application instance for testing
        self.application = Application.objects.create(
            status=True,
            code="APP123",
            name="Test Application",
            contact_name="John Doe",
            contact_email="john.doe@example.com",
            contact_number="1234567890",
            created_by=1
        )
        self.url = reverse('application_modify', kwargs={'pk': self.application.id})

    def test_retrieve_application(self):
        """
        Test retrieving an Application instance.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Application")
        self.assertEqual(response.data['contact_email'], "john.doe@example.com")

    def test_update_application(self):
        """
        Test updating an Application instance.
        """
        payload = {
            "status": False,
            "code": "APP456",
            "name": "Updated Application",
            "contact_name": "Jane Doe",
            "contact_email": "jane.doe@example.com",
            "contact_number": "0987654321"
        }

        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.name, "Updated Application")
        self.assertEqual(self.application.contact_email, "jane.doe@example.com")
        # self.assertEqual(self.application.updated_by, self.user.id)

    def test_partial_update_application(self):
        """
        Test partially updating an Application instance.
        """
        payload = {
            "contact_name": "Jane Doe"
        }

        response = self.client.patch(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.contact_name, "Jane Doe")

    def test_delete_application(self):
        """
        Test deleting an Application instance.
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Application.objects.filter(id=self.application.id).exists())

    def test_retrieve_application_without_authentication(self):
        """
        Test retrieving an Application instance without authentication.
        """
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ApplicationFilterApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Create application instances for testing
        self.app1 = Application.objects.create(
            status=True,
            code="APP123",
            name="Test Application 1",
            contact_name="John Doe",
            contact_email="john.doe@example.com",
            contact_number="1234567890",
            created_by=self.user.id
        )
        self.app2 = Application.objects.create(
            status=False,
            code="APP456",
            name="Test Application 2",
            contact_name="Jane Doe",
            contact_email="jane.doe@example.com",
            contact_number="0987654321",
            created_by=self.user.id
        )
        self.url = reverse('application_filter')

    def test_filter_by_status(self):
        """
        Test filtering applications by status.
        """
        payload = {
            "status": True,
            "order_by": "created_on",
            "order_type": "desc"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['code'], "APP123")

    def test_filter_by_name(self):
        """
        Test filtering applications by name.
        """
        payload = {
            "name": "Test Application 2",
            "order_by": "created_on",
            "order_type": "desc"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['code'], "APP456")

    def test_filter_by_date_range(self):
        """
        Test filtering applications by created_on date range.
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        payload = {
            "created_on": f"{start_date.isoformat()}Z",
            "order_by": "created_on",
            "order_type": "desc"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertGreaterEqual(len(response.data['results']), 2)

    def test_pagination(self):
        """
        Test pagination for application filtering.
        """
        payload = {
            "order_by": "created_on",
            "order_type": "desc",
            "page": 1,
            "page_size": 1
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data['results']), 1)

    def test_invalid_filter(self):
        """
        Test handling of invalid filter input.
        """
        payload = {
            "status": "invalid_status",
            "order_by": "created_on",
            "order_type": "desc"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_field(self):
        """
        Test handling of missing required fields.
        """
        payload = {
            "order_by": "created_on"
            # Missing required fields like 'status', 'name', etc.
        }
        response = self.client.post(self.url, payload, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # look into this.

    def test_no_results_found(self):
        """
        Test filtering with criteria that return no results.
        """
        payload = {
            "name": "Nonexistent Application",
            "order_by": "created_on",
            "order_type": "desc"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_retrieve_without_authentication(self):
        """
        Test retrieval of filtered applications without authentication.
        """
        self.client.credentials()  # Remove authentication
        payload = {
            "status": True,
            "order_by": "created_on",
            "order_type": "desc"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_with_invalid_token(self):
        """
        Test retrieval with an invalid token.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        payload = {
            "status": True,
            "order_by": "created_on",
            "order_type": "desc"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ClientApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Set up any additional data needed for the tests
        self.client_create_url = reverse('client')
        self.valid_payload = {
            "status": True,
            "code": "CL001",
            "name": "Test Client",
            "contact_name": "John Doe",
            "contact_email": "johndoe@example.com",
            "contact_number": "1234567890"
        }
        self.invalid_payload = {
            "status": True,
            "code": "",
            "name": "Test Client",
            "contact_name": "John Doe",
            "contact_email": "invalid-email",
            "contact_number": "123"
        }

    def test_create_client_with_valid_payload(self):
        """
        Ensure that a client can be created successfully with valid data.
        """
        response = self.client.post(self.client_create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Client.objects.filter(name="Test Client").exists())

    def test_create_client_with_invalid_payload(self):
        """
        Ensure that a client creation fails with invalid data.
        """
        response = self.client.post(self.client_create_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Client.objects.filter(contact_email="invalid-email").exists())

    def test_create_client_missing_required_fields(self):
        """
        Ensure that the client creation fails if required fields are missing.
        """
        missing_field_payload = {
            "status": True,
            "code": "CL001",
            "name": "",  # Missing name field
            "contact_name": "John Doe",
            "contact_email": "johndoe@example.com",
            "contact_number": "1234567890"
        }
        response = self.client.post(self.client_create_url, missing_field_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn('name', response.data)

    def test_create_client_with_existing_code(self):
        """
        Ensure that a client creation fails if the code is not unique.
        """
        Client.objects.create(
            status=True,
            code="CL001",
            name="Existing Client",
            contact_name="Jane Doe",
            contact_email="janedoe@example.com",
            contact_number="0987654321",
            created_by=self.user.id
        )
        response = self.client.post(self.client_create_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertIn('code', response.data)


class ClientModifyApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a client to work with
        self.client_instance = Client.objects.create(
            status=True,
            code="CL001",
            name="Initial Client",
            contact_name="Jane Doe",
            contact_email="janedoe@example.com",
            contact_number="1234567890",
            created_by=self.user.id
        )
        self.client_modify_url = reverse('client_modify', kwargs={'pk': str(self.client_instance.id)})

        self.valid_update_payload = {
            "status": False,
            "code": "CL002",
            "name": "Updated Client",
            "contact_name": "John Smith",
            "contact_email": "johnsmith@example.com",
            "contact_number": "0987654321"
        }

        self.invalid_update_payload = {
            "status": False,
            "code": "",
            "name": "Updated Client",
            "contact_name": "John Smith",
            "contact_email": "invalid-email",
            "contact_number": "0987654321"
        }

    def test_retrieve_client(self):
        """
        Ensure that a client can be retrieved successfully.
        """
        response = self.client.get(self.client_modify_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.client_instance.name)

    def test_update_client_with_valid_payload(self):
        """
        Ensure that a client can be updated successfully with valid data.
        """
        response = self.client.put(self.client_modify_url, self.valid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_instance.refresh_from_db()
        self.assertEqual(self.client_instance.name, "Updated Client")
        self.assertEqual(self.client_instance.code, "CL002")

    def test_update_client_with_invalid_payload(self):
        """
        Ensure that updating a client fails with invalid data.
        """
        response = self.client.put(self.client_modify_url, self.invalid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client_instance.refresh_from_db()
        self.assertNotEqual(self.client_instance.contact_email, "invalid-email")

    def test_partial_update_client(self):
        """
        Ensure that a client can be partially updated successfully.
        """
        partial_update_payload = {
            "contact_name": "New Contact Name"
        }
        response = self.client.patch(self.client_modify_url, partial_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_instance.refresh_from_db()
        self.assertEqual(self.client_instance.contact_name, "New Contact Name")

    def test_delete_client(self):
        """
        Ensure that a client can be deleted successfully.
        """
        response = self.client.delete(self.client_modify_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(id=self.client_instance.id).exists())


class ClientFilterApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Creating some client data to filter
        Client.objects.create(
            status=True, code="C001", name="Client A", contact_name="Alice",
            contact_email="alice@example.com", contact_number="1234567890",
            created_by=self.user.id, updated_by=self.user.id
        )
        Client.objects.create(
            status=False, code="C002", name="Client B", contact_name="Bob",
            contact_email="bob@example.com", contact_number="0987654321",
            created_by=self.user.id, updated_by=self.user.id
        )

    def test_client_filter_by_name(self):
        """
        Test filtering clients by name.
        """
        url = reverse('client_filter')
        filter_payload = {
            "name": "Client A",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Client A")

    def test_client_filter_by_status(self):
        """
        Test filtering clients by status.
        """
        url = reverse('client_filter')
        filter_payload = {
            "status": True,
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], True)

    def test_client_filter_invalid_page(self):
        """
        Test filtering with an invalid page number.
        """
        url = reverse('client_filter')
        filter_payload = {
            "page": 3,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Page not found")

    def test_client_filter_with_ordering(self):
        """
        Test filtering with ordering by name ascending.
        """
        url = reverse('client_filter')
        filter_payload = {
            "order_by": "name",
            "order_type": "asc",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], "Client A")
        self.assertEqual(response.data['results'][1]['name'], "Client B")
