from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model

from master_data_management.models import Category, Department, UserDepartment, Status, Currency, Country
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
        self.assertEqual(response.data['message'], "No Category matches the given query.")

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

    def test_create_status_missing_fields(self):
        data = {
            "name": "In Progress"
            # Missing other required fields
        }
        response = self.client.post(self.status_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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