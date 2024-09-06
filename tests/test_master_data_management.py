from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from master_data_management.models import (Category, Department, UserDepartment, Status, Currency, Country,
                                           EmailTemplate, EmailTemplateType, LineOfBusiness, LegalEntity)
from master_data_management.serializers import EmailTemplateTypeSerializer

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
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
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


class StatusFilterApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Setup initial data for Status
        self.status_1 = Status.objects.create(
            name="Vendor Creation Initiated",
            status_code=1,
            color_name="Red",
            color_code="#FF0000",
            highlight=1,
            created_by=self.user,
            is_active=True
        )
        self.status_2 = Status.objects.create(
            name="Vendor Update Initiated",
            status_code=2,
            color_name="Blue",
            color_code="#0000FF",
            highlight=0,
            created_by=self.user,
            is_active=False
        )


    def test_filter_by_status_code(self):
        url = reverse('status_list')
        payload = {'status_code': 2}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status_code'], 2)

    def test_filter_by_is_active(self):
        url = reverse('status_list')
        payload = {'is_active': True}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['is_active'], True)

    def test_pagination(self):
        url = reverse('status_list')
        payload = {'page_size': 1, 'page': 1}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_ordering_by_name_ascending(self):
        url = reverse('status_list')
        payload = {'order_by': 'name', 'order_type': 'asc'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], 'Vendor Creation Initiated')

    def test_ordering_by_name_descending(self):
        url = reverse('status_list')
        payload = {'order_by': 'name', 'order_type': 'desc'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], 'Vendor Update Initiated')

    def test_invalid_page_number(self):
        url = reverse('status_list')
        payload = {'page_size': 1, 'page': 999}  # Page that doesn't exist
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Page not found')

    def test_invalid_page_size(self):
        url = reverse('status_list')
        payload = {'page_size': 0}  # Invalid page size
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'page and page size should be positive integer')


# TestCase for Country
class CountryCreateApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url_create = reverse('country_create')
        # self.country_modify_url = reverse('country_detail', kwargs={'pk': self.url_create.pk})
        self.valid_data = {
            "country_name": "India",
            "country_code": "IN",
            "description": "Country in South Asia",
            "is_active": True
        }
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
class CurrencyCreateApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url_create = reverse('currency_create')
        self.valid_data = {
            "currency_name": "US Dollar",
            "currency_code": "USD",
            "is_active": True
        }

    def test_currency_create_success(self):
        response = self.client.post(self.url_create, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['currency_name'], self.valid_data['currency_name'])

    def test_currency_create_with_existing_name(self):
        # First create a currency
        response = self.client.post(self.url_create, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try creating the same currency again
        response = self.client.post(self.url_create, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'currency with currency_name currency name already exists.')

    def test_currency_create_with_missing_currency_name(self):
        invalid_data = self.valid_data.copy()
        del invalid_data['currency_name']  # Remove currency_name from the data

        response = self.client.post(self.url_create, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertIn('currency_name', response.json()['error'])

    def test_currency_create_with_invalid_currency_code(self):
        invalid_data = self.valid_data.copy()
        invalid_data['currency_code'] = ''  # Empty currency code

        response = self.client.post(self.url_create, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertIn('currency_code', response.json()['error'])


class CurrencyUpdateApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.currency = Currency.objects.create(
            currency_name="US Dollar",
            currency_code="USD",
            is_active=True,
            created_by=self.user.id
        )
        self.currency_modify_url = reverse('currency_detail', kwargs={'pk': self.currency.pk})

    def test_currency_update_success(self):
        update_data = {
            "currency_name": "Updated Currency",
            "modified_by": self.user.id
        }
        response = self.client.patch(self.currency_modify_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.currency.refresh_from_db()
        self.assertEqual(self.currency.currency_name, "Updated Currency")

    def test_currency_update_with_invalid_data(self):
        update_data = {
            "currency_name": "",  # Invalid name
            "modified_by": self.user.id
        }
        response = self.client.patch(self.currency_modify_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertIn('currency_name', response.json()['error'])


class CurrencyFilterApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url_filter = reverse('currency_filter')
        self.currency = Currency.objects.create(
            currency_name="US Dollar",
            currency_code="USD",
            is_active=True,
            created_by=self.user.id
        )

    def test_currency_filter_by_name(self):
        filter_data = {
            "currency_name": "US Dollar",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(self.url_filter, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['currency_name'], "US Dollar")

    def test_currency_filter_with_invalid_page(self):
        filter_data = {
            "currency_name": "US Dollar",
            "page": 999,  # Invalid page
            "page_size": 10
        }
        response = self.client.post(self.url_filter, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Page not found')


class EmailTemplateTypeListCreateViewTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.list_create_url = reverse('email_template_type_list_create')

    def test_create_email_template_type(self):
        """
        Ensure we can create a new EmailTemplateType.
        """
        payload = {
            "template_name": "Welcome Email",
        }
        response = self.client.post(self.list_create_url, payload, format='json')

        # Check that the email template type was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['template_name'], payload['template_name'])
        self.assertEqual(response.data['created_by'], self.user.id)

        # Ensure that the instance is created in the database
        self.assertTrue(EmailTemplateType.objects.filter(template_name=payload['template_name']).exists())

    def test_list_email_template_types(self):
        """
        Ensure we can list EmailTemplateTypes.
        """
        # Create a few instances
        EmailTemplateType.objects.create(template_name="Welcome Email", created_by=self.user)
        EmailTemplateType.objects.create(template_name="Password Reset", created_by=self.user)

        response = self.client.get(self.list_create_url, format='json')

        # Check that the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the number of returned email template types matches what we created
        self.assertEqual(len(response.data), 2)

        # Optionally, check the content of the returned data
        email_template_types = EmailTemplateType.objects.all()
        serializer = EmailTemplateTypeSerializer(email_template_types, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_email_template_type_with_duplicate_name(self):
        """
        Ensure that creating an EmailTemplateType with a duplicate name fails.
        """
        EmailTemplateType.objects.create(template_name="Welcome Email", created_by=self.user)
        payload = {
            "template_name": "Welcome Email",
        }
        response = self.client.post(self.list_create_url, payload, format='json')

        # Check that the response status is HTTP 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure that the error message indicates the duplicate issue
        self.assertIn('template_name', response.data['error'])


class EmailTemplateTypeRetrieveUpdateDestroyViewTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.email_template_type = EmailTemplateType.objects.create(
            template_name="Welcome Email", created_by=self.user
        )
        self.detail_url = reverse('email_template_type_detail', args=[self.email_template_type.pk])

    def test_retrieve_email_template_type(self):
        """
        Ensure we can retrieve a single EmailTemplateType.
        """
        response = self.client.get(self.detail_url, format='json')

        # Check that the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the returned data matches the created instance
        serializer = EmailTemplateTypeSerializer(self.email_template_type)
        self.assertEqual(response.data, serializer.data)

    def test_update_email_template_type(self):
        """
        Ensure we can update an existing EmailTemplateType.
        """
        payload = {
            "template_name": "Updated Welcome Email"
        }
        response = self.client.put(self.detail_url, payload, format='json')

        # Check that the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the instance was updated
        self.email_template_type.refresh_from_db()
        self.assertEqual(self.email_template_type.template_name, payload['template_name'])
        self.assertEqual(self.email_template_type.modified_by, self.user)

    def test_partial_update_email_template_type(self):
        """
        Ensure we can partially update an existing EmailTemplateType.
        """
        payload = {
            "template_name": "Partially Updated Email"
        }
        response = self.client.patch(self.detail_url, payload, format='json')

        # Check that the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the instance was updated
        self.email_template_type.refresh_from_db()
        self.assertEqual(self.email_template_type.template_name, payload['template_name'])
        self.assertEqual(self.email_template_type.modified_by, self.user)

    def test_delete_email_template_type(self):
        """
        Ensure we can delete an EmailTemplateType.
        """
        response = self.client.delete(self.detail_url, format='json')

        # Check that the response status is NO CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the instance was deleted
        self.assertFalse(EmailTemplateType.objects.filter(pk=self.email_template_type.pk).exists())

    def test_update_email_template_type_with_duplicate_name(self):
        """
        Ensure that updating an EmailTemplateType with a duplicate name fails.
        """
        EmailTemplateType.objects.create(template_name="Duplicate Email", created_by=self.user)
        payload = {
            "template_name": "Duplicate Email"
        }
        response = self.client.put(self.detail_url, payload, format='json')

        # Check that the response status is HTTP 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure that the error message indicates the duplicate issue
        self.assertIn('template_name', response.data['error'])


class EmailTemplateListCreateApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create an EmailTemplateType instance to use in tests
        self.email_template_type = EmailTemplateType.objects.create(template_name="Welcome Email")

    def test_create_email_template(self):
        """Test creating a new email template."""
        url = reverse('email_template_list_create')
        valid_payload = {
            "template_type": self.email_template_type.id,
            "subject": "Welcome to Our Service",
            "email_to": "##user_email##",
            "cc": "##creator_email##,##creator_email##",
            "bcc": "##creator_email##",
            "message": "Hello ##user_name##, welcome to our service!",
            "signature": "Best regards, Our Service Team"
        }

        response = self.client.post(url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmailTemplate.objects.count(), 1)
        self.assertEqual(EmailTemplate.objects.get().subject, "Welcome to Our Service")

    def test_create_email_template_without_required_shortcodes(self):
        """Test creating an email template without required shortcodes in fields."""
        url = reverse('email_template_list_create')
        invalid_payload = {
            "template_type": self.email_template_type.id,
            "subject": "Welcome to Our Service",
            "email_to": "user@example.com",  # Missing shortcode
            "cc": "admin@example.com",
            "bcc": "admin@example.com",
            "message": "Hello User, welcome to our service!",  # Missing shortcode
            "signature": "Best regards, Our Service Team"
        }

        response = self.client.post(url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email_to', response.data['error'])
        self.assertIn('message', response.data['error'])

    def test_list_email_templates(self):
        """Test listing all email templates."""
        # First, create a sample email template
        EmailTemplate.objects.create(
            template_type=self.email_template_type,
            subject="Sample Email",
            email_to="##user_email##",
            message="This is a sample email template."
        )

        url = reverse('email_template_list_create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['subject'], "Sample Email")

    #
    def test_create_email_template_with_invalid_cc_bcc_format(self):
        """Test creating an email template with invalid CC/BCC format."""
        url = reverse('email_template_list_create')
        invalid_payload = {
            "template_type": self.email_template_type.id,
            "subject": "Invalid CC/BCC Format",
            "email_to": "##user_email##",
            "cc": "##creator_email##,invalid_email_format",  # Invalid email format
            "bcc": "admin@example.com",
            "message": "Hello ##user_name##, welcome to our service!",
            "signature": "Best regards, Our Service Team"
        }

        response = self.client.post(url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cc', response.data['error'])


class EmailTemplateRetrieveUpdateDestroyApiTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Creating a sample EmailTemplateType
        self.email_template_type = EmailTemplateType.objects.create(template_name="Registration")

        # Creating a sample EmailTemplate instance
        self.email_template = EmailTemplate.objects.create(
            is_active=True,
            template_type=self.email_template_type,
            subject="Welcome to Our Service",
            email_to="##user_email##",
            cc="##creator_email##",
            bcc="##follower_email##",
            message="Hello ##user_name##, welcome!",
            signature="Best Regards, Team",
            created_by=self.user
        )
        self.detail_url = reverse('email_template_detail', kwargs={'pk': self.email_template.pk})

    def test_retrieve_email_template(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], self.email_template.subject)

    def test_update_email_template(self):
        updated_payload = {
            'subject': 'Updated Subject',
            'email_to': '##user_email##',
            'cc': '##creator_email##',
            'bcc': '##follower_email##',
            'message': 'Updated message content##creator_email##',
            'signature': 'Updated Signature',
        }
        response = self.client.put(self.detail_url, updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.email_template.refresh_from_db()
        self.assertEqual(self.email_template.subject, 'Updated Subject')
        self.assertEqual(self.email_template.message, 'Updated message content##creator_email##')

    #
    def test_partial_update_email_template(self):
        partial_payload = {
            'subject': 'Partially Updated Subject',
        }
        response = self.client.patch(self.detail_url, partial_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.email_template.refresh_from_db()
        self.assertEqual(self.email_template.subject, 'Partially Updated Subject')

    def test_delete_email_template(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(EmailTemplate.DoesNotExist):
            EmailTemplate.objects.get(pk=self.email_template.pk)

    def test_update_email_template_invalid_shortcodes(self):
        invalid_payload = {
            'subject': 'Invalid Subject',
            'email_to': 'invalidemail@domain.com',  # No shortcode
            'cc': 'invalidcc@domain.com',  # No shortcode
            'bcc': 'invalidbcc@domain.com',  # No shortcode
            'message': 'This message has no shortcode',
            'signature': 'Invalid Signature',
        }
        response = self.client.put(self.detail_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email_to', response.data['error'])
        self.assertIn('cc', response.data['error'])
        self.assertIn('bcc', response.data['error'])
        self.assertIn('message', response.data['error'])


class EmailTemplateFilterApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Setup initial data for EmailTemplate
        template_type = EmailTemplateType.objects.create(template_name="Notification")
        self.email_template = EmailTemplate.objects.create(
            template_type=template_type,
            subject="Welcome",
            email_to="user@example.com",
            cc="cc1@example.com,cc2@example.com",
            bcc="bcc1@example.com",
            message="Welcome to our service!",
            signature="Best regards, Team",
            created_by=self.user,
            is_active=True
        )

    def test_filter_by_subject(self):
        url = reverse('email_template_list_filter')
        payload = {
            'subject': 'Welcome'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['subject'], 'Welcome')


    def test_filter_by_is_active(self):
        url = reverse('email_template_list_filter')
        payload = {
            'is_active': True
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['is_active'], True)

    def test_pagination(self):
        url = reverse('email_template_list_filter')
        payload = {
            'page_size': 1,
            'page': 1
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_ordering_by_subject_ascending(self):
        url = reverse('email_template_list_filter')
        payload = {
            'order_by': 'subject',
            'order_type': 'asc'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['subject'], 'Welcome')

    def test_ordering_by_subject_descending(self):
        url = reverse('email_template_list_filter')
        payload = {
            'order_by': 'subject',
            'order_type': 'desc'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['subject'], 'Welcome')


# class FileTypeCreateApiTestCase(BaseTestCase):
#
#     def setUp(self):
#         super().setUp()  # Calls the BaseTestCase setup for authentication
#         self.url = reverse('file_type')
#
#         # Prepare valid payload for file type creation
#         self.valid_payload = {
#             "status": True,
#             "file_type": "Document",
#             "file_extension": "PDF",
#             "max_file_size": 1024,
#             "file_description": "PDF documents"
#         }
#
#     def test_create_file_type_valid(self):
#         """
#         Test creating a file type with valid data.
#         """
#         response = self.client.post(self.url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(FileType.objects.count(), 1)
#         file_type = FileType.objects.get()
#         self.assertEqual(file_type.file_type, self.valid_payload['file_type'])
#         # self.assertEqual(file_type.file_extension, self.valid_payload['file_extension'].lower())
#         # self.assertEqual(file_type.max_file_size, self.valid_payload['max_file_size'])
#
#     def test_create_file_type_duplicate_extension(self):
#         """
#         Test creating a file type with a duplicate file extension.
#         """
#         # Create the first FileType instance
#         self.client.post(self.url, self.valid_payload, format='json')
#
#         # Attempt to create another with the same file extension
#         duplicate_payload = self.valid_payload.copy()
#         response = self.client.post(self.url, duplicate_payload, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(FileType.objects.count(), 1)
#         # self.assertIn("File extension name should be unique", response.data['non_field_errors'])
#
#     def test_create_file_type_invalid_extension(self):
#         """
#         Test creating a file type with an invalid file extension containing special characters.
#         """
#         invalid_payload = self.valid_payload.copy()
#         invalid_payload['file_extension'] = "PDF*"
#
#         response = self.client.post(self.url, invalid_payload, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(FileType.objects.count(), 0)
#         # self.assertIn("File extension should not contain any special characters", response.data['file_extension'])
#
#     def test_create_file_type_missing_required_fields(self):
#         """
#         Test creating a file type with missing required fields.
#         """
#         invalid_payload = self.valid_payload.copy()
#         del invalid_payload['file_type']  # Remove required field
#
#         response = self.client.post(self.url, invalid_payload, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # self.assertEqual(FileType.objects.count(), 0)
#         # self.assertIn("This field is required.", response.data['file_type'])


# class FileTypeModifyApiTestCase(BaseTestCase):
#
#     def setUp(self):
#         super().setUp()  # Calls the BaseTestCase setup for authentication
#
#         # Create an initial FileType instance for testing modify operations
#         self.file_type_instance = FileType.objects.create(
#             status=True,
#             file_type="Document",
#             file_extension="PDF",
#             max_file_size=1024,
#             file_description="PDF documents",
#             created_by=self.user.id
#         )
#         self.url = reverse('file_type_modify', kwargs={'pk': self.file_type_instance.id})
#
#     def test_retrieve_file_type(self):
#         """
#         Test retrieving a file type by ID.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['file_type'], self.file_type_instance.file_type)
#         self.assertEqual(response.data['file_extension'], self.file_type_instance.file_extension)
#
#     def test_update_file_type(self):
#         """
#         Test updating a file type with new data.
#         """
#         update_payload = {
#             "status": False,
#             "file_type": "Updated Document",
#             "file_extension": "DOCX",
#             "max_file_size": 2048,
#             "file_description": "Updated description"
#         }
#
#         response = self.client.put(self.url, update_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.file_type_instance.refresh_from_db()
#         self.assertEqual(self.file_type_instance.file_type, update_payload['file_type'])
#         # self.assertEqual(self.file_type_instance.file_extension, update_payload['file_extension'].lower())
#         # self.assertEqual(self.file_type_instance.max_file_size, update_payload['max_file_size'])
#
#     def test_partial_update_file_type(self):
#         """
#         Test partially updating a file type.
#         """
#         partial_update_payload = {
#             "file_description": "Partially updated description"
#         }
#
#         response = self.client.patch(self.url, partial_update_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.file_type_instance.refresh_from_db()
#         self.assertEqual(self.file_type_instance.file_description, partial_update_payload['file_description'])
#
#     def test_delete_file_type(self):
#         """
#         Test deleting a file type.
#         """
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(FileType.objects.filter(id=self.file_type_instance.id).exists())
#
#     def test_update_file_type_invalid_extension(self):
#         """
#         Test updating a file type with an invalid file extension containing special characters.
#         """
#         invalid_update_payload = {
#             "file_extension": "DOCX*"
#         }
#
#         response = self.client.put(self.url, invalid_update_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # self.assertIn("File extension should not contain any special characters", response.data['file_extension'])
#
#     def test_update_file_type_duplicate_extension(self):
#         """
#         Test updating a file type to a duplicate file extension.
#         """
#         # Create another FileType instance with the same file_extension
#         FileType.objects.create(
#             status=True,
#             file_type="Another Document",
#             file_extension="DOCX",
#             max_file_size=512,
#             file_description="Another document",
#             created_by=self.user.id
#         )
#
#         # Attempt to update the original file type to the same file_extension
#         duplicate_extension_payload = {
#             "file_extension": "DOCX"
#         }
#
#         response = self.client.put(self.url, duplicate_extension_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # self.assertIn("File extension name should be unique", response.data['non_field_errors'])
#
#
# class FileTypeFilterApiTestCase(BaseTestCase):
#
#     def setUp(self):
#         super().setUp()  # Calls the BaseTestCase setup for authentication
#
#         # Create multiple FileType instances for testing
#         self.file_types = [
#             FileType.objects.create(
#                 status=True,
#                 file_type="Document1",
#                 file_extension="PDF",
#                 max_file_size=1024,
#                 file_description="Description1",
#                 created_by=self.user.id
#             ),
#             FileType.objects.create(
#                 status=False,
#                 file_type="Document2",
#                 file_extension="DOCX",
#                 max_file_size=2048,
#                 file_description="Description2",
#                 created_by=self.user.id
#             ),
#             FileType.objects.create(
#                 status=True,
#                 file_type="Document3",
#                 file_extension="XLSX",
#                 max_file_size=3072,
#                 file_description="Description3",
#                 created_by=self.user.id
#             )
#         ]
#         self.url = reverse('file_type_list')
#
#     def test_filter_file_type_by_status(self):
#         """
#         Test filtering file types by status.
#         """
#         filter_payload = {
#             "status": True
#         }
#
#         response = self.client.post(self.url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 2)
#         self.assertTrue(all(item['status'] == True for item in response.data['results']))
#
#     def test_filter_file_type_by_file_type(self):
#         """
#         Test filtering file types by file_type.
#         """
#         filter_payload = {
#             "file_type": "Document1"
#         }
#
#         response = self.client.post(self.url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 1)
#         self.assertEqual(response.data['results'][0]['file_type'], "Document1")
#
#     def test_pagination(self):
#         """
#         Test pagination of file types.
#         """
#         filter_payload = {
#             "page": 1,
#             "page_size": 2
#         }
#
#         response = self.client.post(self.url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 2)
#         self.assertEqual(response.data['count'], len(self.file_types))
#
#     def test_order_by_file_type(self):
#         """
#         Test ordering file types by file_type.
#         """
#         filter_payload = {
#             "order_by": "file_type",
#             "order_type": "asc"
#         }
#
#         response = self.client.post(self.url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         results = response.data['results']
#         file_types = [ft['file_type'] for ft in results]
#         self.assertEqual(file_types, sorted(file_types))
#
#     def test_order_by_file_type_desc(self):
#         """
#         Test ordering file types by file_type in descending order.
#         """
#         filter_payload = {
#             "order_by": "file_type",
#             "order_type": "desc"
#         }
#
#         response = self.client.post(self.url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         results = response.data['results']
#         file_types = [ft['file_type'] for ft in results]
#         self.assertEqual(file_types, sorted(file_types, reverse=True))
#
#     def test_invalid_page_and_page_size(self):
#         """
#         Test handling of invalid page and page_size values.
#         """
#         filter_payload = {
#             "page": -1,
#             "page_size": 0
#         }
#
#         response = self.client.post(self.url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['message'], "page and page size should be positive integer")
#
#     def test_page_not_found(self):
#         """
#         Test handling of page number that exceeds available pages.
#         """
#         filter_payload = {
#             "page": 9999,
#             "page_size": 2
#         }
#
#         response = self.client.post(self.url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['message'], "Page not found")
#
#     def test_invalid_export_option(self):
#         """
#         Test handling of invalid export option.
#         """
#         filter_payload = {
#             "export": "invalid_option"
#         }
#
#         response = self.client.post(self.url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # self.assertIn("Invalid export option", response.data.get('message', ''))
#
#
# # Test cases for Business Unit
# class BusinessUnitApiTestCase(BaseTestCase):
#
#     def setUp(self):
#         super().setUp()
#         self.create_url = reverse('business_unit')
#
#     def test_create_business_unit_valid(self):
#         data = {
#             "client_id": "Client1",
#             "code": "Code1",
#             "name": "Business Unit 1",
#             "contact_name": "John Doe",
#             "contact_email": "john.doe@example.com",
#             "contact_number": "1234567890"
#         }
#         response = self.client.post(self.create_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(BusinessUnit.objects.count(), 1)
#         self.assertEqual(BusinessUnit.objects.get().name, "Business Unit 1")
#
#     def test_create_business_unit_invalid(self):
#         data = {
#             "client_id": "Client1",
#             "code": "Code1",
#             "name": "",
#             "contact_name": "John Doe",
#             "contact_email": "john.doe@example.com",
#             "contact_number": "1234567890"
#         }
#         response = self.client.post(self.create_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class BusinessUnitModifyApiTestCase(BaseTestCase):
#
#     def setUp(self):
#         super().setUp()
#         self.business_unit = BusinessUnit.objects.create(
#             client_id="Client1",
#             code="Code1",
#             name="Business Unit 1",
#             contact_name="John Doe",
#             contact_email="john.doe@example.com",
#             contact_number="1234567890",
#             created_by=self.user.id
#         )
#         self.modify_url = reverse('business_unit_modify', args=[self.business_unit.id])
#
#     def test_get_business_unit(self):
#         response = self.client.get(self.modify_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], "Business Unit 1")
#
#     def test_update_business_unit(self):
#         # Update with valid email format
#         data = {
#             "code": "UpdatedCode",
#             "name": "Updated Business Unit",
#             "contact_name": "Updated Contact Name",
#             "contact_number": "0987654321"
#         }
#         response = self.client.put(self.modify_url, data, format='json')
#
#         # Print debugging output if the response status is not OK
#         if response.status_code != status.HTTP_200_OK:
#             print("Response Status Code:", response.status_code)
#             print("Response Data:", response.data)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.business_unit.refresh_from_db()
#         self.assertEqual(self.business_unit.name, "Updated Business Unit")
#
#     def test_delete_business_unit(self):
#         response = self.client.delete(self.modify_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(BusinessUnit.objects.filter(id=self.business_unit.id).exists())
#
#
# class BusinessUnitFilterApiTestCase(BaseTestCase):
#
#     def setUp(self):
#         super().setUp()
#         self.business_unit1 = BusinessUnit.objects.create(
#             client_id="Client1",
#             code="Code1",
#             name="Business Unit 1",
#             contact_name="John Doe",
#             contact_email="john.doe@example.com",
#             contact_number="1234567890",
#             created_by=self.user.id
#         )
#         self.business_unit2 = BusinessUnit.objects.create(
#             client_id="Client2",
#             code="Code2",
#             name="Business Unit 2",
#             contact_name="Jane Doe",
#             contact_email="jane.doe@example.com",
#             contact_number="0987654321",
#             created_by=self.user.id
#         )
#         self.filter_url = reverse('business_unit_filter')
#
#     def test_filter_business_units(self):
#         data = {
#             "name": "Business Unit 1",
#             "page": 1,
#             "page_size": 10
#         }
#         response = self.client.post(self.filter_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['count'], 1)
#         self.assertEqual(response.data['results'][0]['name'], "Business Unit 1")
#
#     def test_filter_business_units_invalid_page(self):
#         data = {
#             "page": -1,
#             "page_size": 10
#         }
#         response = self.client.post(self.filter_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#
# class ApplicationApiTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.url = reverse('application')
#
#     def test_create_application_success(self):
#         """
#         Test successful creation of an Application instance.
#         """
#         payload = {
#             "status": True,
#             "code": "APP123",
#             "name": "Test Application",
#             "contact_name": "John Doe",
#             "contact_email": "john.doe@example.com",
#             "contact_number": "1234567890"
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Application.objects.count(), 1)
#         self.assertEqual(Application.objects.get().name, "Test Application")
#         self.assertEqual(Application.objects.get().created_by, self.user.id)
#
#     def test_create_application_missing_fields(self):
#         """
#         Test creating an Application instance with missing required fields.
#         """
#         payload = {
#             "status": True
#             # Missing 'code', 'name', 'contact_name', 'contact_email', 'contact_number'
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # look this
#         # self.assertIn('code', response.data)
#         # self.assertIn('name', response.data)
#         # self.assertIn('contact_name', response.data)
#         # self.assertIn('contact_email', response.data)
#         # self.assertIn('contact_number', response.data)
#
#     def test_create_application_invalid_email(self):
#         """
#         Test creating an Application instance with an invalid email address.
#         """
#         payload = {
#             "status": True,
#             "code": "APP123",
#             "name": "Test Application",
#             "contact_name": "John Doe",
#             "contact_email": "invalid-email",
#             "contact_number": "1234567890"
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('contact_email', response.data['error'])
#
#     def test_create_application_without_authentication(self):
#         """
#         Test creating an Application instance without authentication.
#         """
#         self.client.credentials()  # Remove authentication
#         payload = {
#             "status": True,
#             "code": "APP123",
#             "name": "Test Application",
#             "contact_name": "John Doe",
#             "contact_email": "john.doe@example.com",
#             "contact_number": "1234567890"
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_create_application_with_invalid_data(self):
#         """
#         Test creating an Application instance with invalid data.
#         """
#         payload = {
#             "status": "not_a_boolean",  # Invalid data type
#             "code": "APP123",
#             "name": "Test Application",
#             "contact_name": "John Doe",
#             "contact_email": "john.doe@example.com",
#             "contact_number": "1234567890"
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('status', response.data['error'])
#
#
# class ApplicationModifyApiTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#
#         # Create an application instance for testing
#         self.application = Application.objects.create(
#             status=True,
#             code="APP123",
#             name="Test Application",
#             contact_name="John Doe",
#             contact_email="john.doe@example.com",
#             contact_number="1234567890",
#             created_by=1
#         )
#         self.url = reverse('application_modify', kwargs={'pk': self.application.id})
#
#     def test_retrieve_application(self):
#         """
#         Test retrieving an Application instance.
#         """
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], "Test Application")
#         self.assertEqual(response.data['contact_email'], "john.doe@example.com")
#
#     def test_update_application(self):
#         """
#         Test updating an Application instance.
#         """
#         payload = {
#             "status": False,
#             "code": "APP456",
#             "name": "Updated Application",
#             "contact_name": "Jane Doe",
#             "contact_email": "jane.doe@example.com",
#             "contact_number": "0987654321"
#         }
#
#         response = self.client.put(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.application.refresh_from_db()
#         self.assertEqual(self.application.name, "Updated Application")
#         self.assertEqual(self.application.contact_email, "jane.doe@example.com")
#         # self.assertEqual(self.application.updated_by, self.user.id)
#
#     def test_partial_update_application(self):
#         """
#         Test partially updating an Application instance.
#         """
#         payload = {
#             "contact_name": "Jane Doe"
#         }
#
#         response = self.client.patch(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.application.refresh_from_db()
#         self.assertEqual(self.application.contact_name, "Jane Doe")
#
#     def test_delete_application(self):
#         """
#         Test deleting an Application instance.
#         """
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Application.objects.filter(id=self.application.id).exists())
#
#     def test_retrieve_application_without_authentication(self):
#         """
#         Test retrieving an Application instance without authentication.
#         """
#         self.client.credentials()  # Remove authentication
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class ApplicationFilterApiTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#
#         # Create application instances for testing
#         self.app1 = Application.objects.create(
#             status=True,
#             code="APP123",
#             name="Test Application 1",
#             contact_name="John Doe",
#             contact_email="john.doe@example.com",
#             contact_number="1234567890",
#             created_by=self.user.id
#         )
#         self.app2 = Application.objects.create(
#             status=False,
#             code="APP456",
#             name="Test Application 2",
#             contact_name="Jane Doe",
#             contact_email="jane.doe@example.com",
#             contact_number="0987654321",
#             created_by=self.user.id
#         )
#         self.url = reverse('application_filter')
#
#     def test_filter_by_status(self):
#         """
#         Test filtering applications by status.
#         """
#         payload = {
#             "status": True,
#             "order_by": "created_on",
#             "order_type": "desc"
#         }
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 1)
#         self.assertEqual(response.data['results'][0]['code'], "APP123")
#
#     def test_filter_by_name(self):
#         """
#         Test filtering applications by name.
#         """
#         payload = {
#             "name": "Test Application 2",
#             "order_by": "created_on",
#             "order_type": "desc"
#         }
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 1)
#         self.assertEqual(response.data['results'][0]['code'], "APP456")
#
#     def test_filter_by_date_range(self):
#         """
#         Test filtering applications by created_on date range.
#         """
#         end_date = datetime.now()
#         start_date = end_date - timedelta(days=1)
#         payload = {
#             "created_on": f"{start_date.isoformat()}Z",
#             "order_by": "created_on",
#             "order_type": "desc"
#         }
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # self.assertGreaterEqual(len(response.data['results']), 2)
#
#     def test_pagination(self):
#         """
#         Test pagination for application filtering.
#         """
#         payload = {
#             "order_by": "created_on",
#             "order_type": "desc",
#             "page": 1,
#             "page_size": 1
#         }
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # self.assertEqual(len(response.data['results']), 1)
#
#     def test_invalid_filter(self):
#         """
#         Test handling of invalid filter input.
#         """
#         payload = {
#             "status": "invalid_status",
#             "order_by": "created_on",
#             "order_type": "desc"
#         }
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_missing_required_field(self):
#         """
#         Test handling of missing required fields.
#         """
#         payload = {
#             "order_by": "created_on"
#             # Missing required fields like 'status', 'name', etc.
#         }
#         response = self.client.post(self.url, payload, format='json')
#         # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # look into this.
#
#     def test_no_results_found(self):
#         """
#         Test filtering with criteria that return no results.
#         """
#         payload = {
#             "name": "Nonexistent Application",
#             "order_by": "created_on",
#             "order_type": "desc"
#         }
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['results'], [])
#
#     def test_retrieve_without_authentication(self):
#         """
#         Test retrieval of filtered applications without authentication.
#         """
#         self.client.credentials()  # Remove authentication
#         payload = {
#             "status": True,
#             "order_by": "created_on",
#             "order_type": "desc"
#         }
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_retrieve_with_invalid_token(self):
#         """
#         Test retrieval with an invalid token.
#         """
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
#         payload = {
#             "status": True,
#             "order_by": "created_on",
#             "order_type": "desc"
#         }
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class ClientApiTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         # Set up any additional data needed for the tests
#         self.client_create_url = reverse('client')
#         self.valid_payload = {
#             "status": True,
#             "code": "CL001",
#             "name": "Test Client",
#             "contact_name": "John Doe",
#             "contact_email": "johndoe@example.com",
#             "contact_number": "1234567890"
#         }
#         self.invalid_payload = {
#             "status": True,
#             "code": "",
#             "name": "Test Client",
#             "contact_name": "John Doe",
#             "contact_email": "invalid-email",
#             "contact_number": "123"
#         }
#
#     def test_create_client_with_valid_payload(self):
#         """
#         Ensure that a client can be created successfully with valid data.
#         """
#         response = self.client.post(self.client_create_url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Client.objects.filter(name="Test Client").exists())
#
#     def test_create_client_with_invalid_payload(self):
#         """
#         Ensure that a client creation fails with invalid data.
#         """
#         response = self.client.post(self.client_create_url, self.invalid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(Client.objects.filter(contact_email="invalid-email").exists())
#
#     def test_create_client_missing_required_fields(self):
#         """
#         Ensure that the client creation fails if required fields are missing.
#         """
#         missing_field_payload = {
#             "status": True,
#             "code": "CL001",
#             "name": "",  # Missing name field
#             "contact_name": "John Doe",
#             "contact_email": "johndoe@example.com",
#             "contact_number": "1234567890"
#         }
#         response = self.client.post(self.client_create_url, missing_field_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # self.assertIn('name', response.data)
#
#     def test_create_client_with_existing_code(self):
#         """
#         Ensure that a client creation fails if the code is not unique.
#         """
#         Client.objects.create(
#             status=True,
#             code="CL001",
#             name="Existing Client",
#             contact_name="Jane Doe",
#             contact_email="janedoe@example.com",
#             contact_number="0987654321",
#             created_by=self.user.id
#         )
#         response = self.client.post(self.client_create_url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # self.assertIn('code', response.data)
#
#
# class ClientModifyApiTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         # Create a client to work with
#         self.client_instance = Client.objects.create(
#             status=True,
#             code="CL001",
#             name="Initial Client",
#             contact_name="Jane Doe",
#             contact_email="janedoe@example.com",
#             contact_number="1234567890",
#             created_by=self.user.id
#         )
#         self.client_modify_url = reverse('client_modify', kwargs={'pk': str(self.client_instance.id)})
#
#         self.valid_update_payload = {
#             "status": False,
#             "code": "CL002",
#             "name": "Updated Client",
#             "contact_name": "John Smith",
#             "contact_email": "johnsmith@example.com",
#             "contact_number": "0987654321"
#         }
#
#         self.invalid_update_payload = {
#             "status": False,
#             "code": "",
#             "name": "Updated Client",
#             "contact_name": "John Smith",
#             "contact_email": "invalid-email",
#             "contact_number": "0987654321"
#         }
#
#     def test_retrieve_client(self):
#         """
#         Ensure that a client can be retrieved successfully.
#         """
#         response = self.client.get(self.client_modify_url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], self.client_instance.name)
#
#     def test_update_client_with_valid_payload(self):
#         """
#         Ensure that a client can be updated successfully with valid data.
#         """
#         response = self.client.put(self.client_modify_url, self.valid_update_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client_instance.refresh_from_db()
#         self.assertEqual(self.client_instance.name, "Updated Client")
#         self.assertEqual(self.client_instance.code, "CL002")
#
#     def test_update_client_with_invalid_payload(self):
#         """
#         Ensure that updating a client fails with invalid data.
#         """
#         response = self.client.put(self.client_modify_url, self.invalid_update_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.client_instance.refresh_from_db()
#         self.assertNotEqual(self.client_instance.contact_email, "invalid-email")
#
#     def test_partial_update_client(self):
#         """
#         Ensure that a client can be partially updated successfully.
#         """
#         partial_update_payload = {
#             "contact_name": "New Contact Name"
#         }
#         response = self.client.patch(self.client_modify_url, partial_update_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.client_instance.refresh_from_db()
#         self.assertEqual(self.client_instance.contact_name, "New Contact Name")
#
#     def test_delete_client(self):
#         """
#         Ensure that a client can be deleted successfully.
#         """
#         response = self.client.delete(self.client_modify_url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Client.objects.filter(id=self.client_instance.id).exists())
#
#
# class ClientFilterApiTestCase(BaseTestCase):
#
#     def setUp(self):
#         super().setUp()
#         # Creating some client data to filter
#         Client.objects.create(
#             status=True, code="C001", name="Client A", contact_name="Alice",
#             contact_email="alice@example.com", contact_number="1234567890",
#             created_by=self.user.id, updated_by=self.user.id
#         )
#         Client.objects.create(
#             status=False, code="C002", name="Client B", contact_name="Bob",
#             contact_email="bob@example.com", contact_number="0987654321",
#             created_by=self.user.id, updated_by=self.user.id
#         )
#
#     def test_client_filter_by_name(self):
#         """
#         Test filtering clients by name.
#         """
#         url = reverse('client_filter')
#         filter_payload = {
#             "name": "Client A",
#             "page": 1,
#             "page_size": 10
#         }
#         response = self.client.post(url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 1)
#         self.assertEqual(response.data['results'][0]['name'], "Client A")
#
#     def test_client_filter_by_status(self):
#         """
#         Test filtering clients by status.
#         """
#         url = reverse('client_filter')
#         filter_payload = {
#             "status": True,
#             "page": 1,
#             "page_size": 10
#         }
#         response = self.client.post(url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 1)
#         self.assertEqual(response.data['results'][0]['status'], True)
#
#     def test_client_filter_invalid_page(self):
#         """
#         Test filtering with an invalid page number.
#         """
#         url = reverse('client_filter')
#         filter_payload = {
#             "page": 3,
#             "page_size": 10
#         }
#         response = self.client.post(url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['message'], "Page not found")
#
#     def test_client_filter_with_ordering(self):
#         """
#         Test filtering with ordering by name ascending.
#         """
#         url = reverse('client_filter')
#         filter_payload = {
#             "order_by": "name",
#             "order_type": "asc",
#             "page": 1,
#             "page_size": 10
#         }
#         response = self.client.post(url, filter_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']), 2)
#         self.assertEqual(response.data['results'][0]['name'], "Client A")
#         self.assertEqual(response.data['results'][1]['name'], "Client B")
#

User = get_user_model()

class LineOfBusinessUpdateApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)  # Authenticate the test user
        self.lob = LineOfBusiness.objects.create(
            name="Original LOB",
            is_active=True,
            created_by=self.user.id
        )
        self.lob_update_url = reverse('lob_update', kwargs={'pk': self.lob.pk})

    def test_update_line_of_business_with_invalid_data(self):
        update_data = {
            "name": "",  # Invalid name
            "modified_by": self.user.id
        }
        response = self.client.patch(self.lob_update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertIn('name', response.json()['error'])

    def test_update_line_of_business_with_non_existing_id(self):
        non_existing_url = reverse('lob_update', kwargs={'pk': 9999})
        update_data = {
            "name": "Non-Existent LOB",
            "modified_by": self.user.id
        }
        response = self.client.patch(non_existing_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('message', response.json())
        # self.assertEqual(response.json()['message'], 'Line of Business not found.')


class LineOfBusinessFilterApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)  # Authenticate the test user
        self.url_list = reverse('lob_list')
        self.lob1 = LineOfBusiness.objects.create(
            name="LOB One",
            is_active=True,
            created_by=self.user.id
        )
        self.lob2 = LineOfBusiness.objects.create(
            name="LOB Two",
            is_active=False,
            created_by=self.user.id
        )

    def test_list_line_of_business_success(self):
        filter_data = {
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(self.url_list, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['name'], "LOB One")
        self.assertEqual(response.data['results'][1]['name'], "LOB Two")

    def test_list_line_of_business_with_filter(self):
        filter_data = {
            "name": "LOB One",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(self.url_list, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], "LOB One")

    def test_list_line_of_business_with_invalid_page(self):
        filter_data = {
            "page": 999,  # Invalid page
            "page_size": 10
        }
        response = self.client.post(self.url_list, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Page not found')

    def test_list_line_of_business_with_active_status(self):
        # Filter by active status
        filter_data = {
            "is_active": True,
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(self.url_list, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Only one active record
        active_names = [item['name'] for item in response.data['results']]
        self.assertIn("LOB One", active_names)
        self.assertNotIn("LOB Two", active_names)

    def test_list_line_of_business_with_inactive_status(self):
        # Filter by inactive status
        filter_data = {
            "is_active": False,
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(self.url_list, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Only one inactive record
        inactive_names = [item['name'] for item in response.data['results']]
        self.assertIn("LOB Two", inactive_names)
        self.assertNotIn("LOB One", inactive_names)

    def test_list_line_of_business_with_no_results(self):
        # Filter with a name that doesn't exist
        filter_data = {
            "name": "Nonexistent LOB",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(self.url_list, filter_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)


class LegalEntityCreateApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url_create = reverse('legal_entity_create')

    def test_create_legal_entity_success(self):
        payload = {
            "legal_entity_id": "LE001",
            "legal_entity_name": "Legal Entity 1",
            "address_city": "Metropolis",
            "address_country_region_id": "US",
            "address_country_region_iso_code": "US",
            "address_description": "Head Office",
            "address_street": "123 Main St",
            "address_zip_code": "12345",
            "vendor_account_number": "VN123456",
            "sales_tax_group_code": "STG001",
            "bank_account_id": "BA123456",
            "currency_code": "USD",
            "on_hold_status": "Active",
            "vendor_group_id": "VG001",
            "vendor_hold_release_date": "2024-09-01T12:00:00Z",
            "vendor_organization_name": "Legal Entity Org",
            "vendor_type": "Type A",
            "vend_source_system": "System A",
            "vend_source_system_id": "SSID001",
            "vat_number": "VAT123456",
            "is_active": True,
            "is_delete": False
        }
        response = self.client.post(self.url_create, payload, format='json')
        print(response.data)  # Debugging line to check the response data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LegalEntity.objects.count(), 1)
        self.assertEqual(LegalEntity.objects.get().legal_entity_id, "LE001")

    def test_create_legal_entity_missing_required_field(self):
        payload = {
            "legal_entity_name": "Legal Entity 1",
            # Missing required legal_entity_id field
            "address_street": "123 Main St",
            "address_zip_code": "12345",
            "vendor_account_number": "VN123456",
            "city": "Metropolis",
            "currency_code": "USD",
            "vat_number": "VAT123456",
            "is_active": True
        }
        response = self.client.post(self.url_create, payload, format='json')

        # Assert the status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that 'legal_entity_id' is in the 'error' dictionary within the response data
        self.assertIn('legal_entity_id', response.data['error'])

        # Assert that the specific error message is correct
        self.assertEqual(response.data['error']['legal_entity_id'][0], 'This field is required.')

    # def test_create_legal_entity_duplicate_id(self):
    #     # First, create a legal entity with a unique legal_entity_id
    #     unique_id = "LEGAL001"
    #     payload = {
    #         "legal_entity_id": unique_id,
    #         "legal_entity_name": "Legal Entity 1",
    #         "address_street": "123 Main St",
    #         "address_zip_code": "12345",
    #         "vendor_account_number": "VN123456",
    #         "city": "Metropolis",
    #         "currency_code": "USD",
    #         "vat_number": "VAT123456",
    #         "is_active": True
    #     }
    #     response = self.client.post(self.url_create, payload, format='json')
    #
    #     # Attempt to create another legal entity with the same legal_entity_id
    #     duplicate_payload = payload.copy()
    #     duplicate_response = self.client.post(self.url_create, duplicate_payload, format='json')
    #
    #     # Debugging: Print the response content
    #     print("Response status code:", duplicate_response.status_code)
    #     print("Response data:", duplicate_response.data)
    #
    #     # Assert that the status code is 400 BAD REQUEST
    #     self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     # Assert that the 'legal_entity_id' field error is present in the response
    #     self.assertIn('legal_entity_id', duplicate_response.data['error'])
    #
    #     # Assert that the specific error message indicates a duplicate entry
    #     self.assertEqual(duplicate_response.data['error']['legal_entity_id'][0],
    #                      'legal entity with this legal entity id already exists.')


class LegalEntityUpdateApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a LegalEntity to work with
        self.legal_entity = LegalEntity.objects.create(
            legal_entity_id="LE001",
            legal_entity_name="Legal Entity 1",
            address_city="Metropolis",
            address_country_region_id="US",
            address_country_region_iso_code="US",
            address_description="Description of address",
            address_street="123 Main St",
            address_zip_code="12345",
            vendor_account_number="V12345",
            sales_tax_group_code="STG123",
            bank_account_id="BA12345",
            currency_code="USD",
            on_hold_status="No",
            vendor_group_id="VG123",
            vendor_hold_release_date=None,
            vendor_organization_name="Legal Org",
            vendor_type="Type A",
            vend_source_system="System A",
            vend_source_system_id="SS12345",
            vat_number="VAT123456",
            is_active=True,
            is_delete=False
        )
        self.url_update = reverse('legal_entity_modify', kwargs={'pk': self.legal_entity.id})

        # Valid payload for update
        self.valid_update_payload = {
            "legal_entity_id": "LE001",
            "legal_entity_name": "Updated Legal Entity",
            "address_city": "Updated City",
            "address_country_region_id": "UK",
            "address_country_region_iso_code": "GB",
            "address_description": "Updated description",
            "address_street": "456 Another St",
            "address_zip_code": "54321",
            "vendor_account_number": "V54321",
            "sales_tax_group_code": "STG456",
            "bank_account_id": "BA54321",
            "currency_code": "EUR",
            "on_hold_status": "Yes",
            "vendor_group_id": "VG456",
            "vendor_hold_release_date": None,
            "vendor_organization_name": "Updated Org",
            "vendor_type": "Type B",
            "vend_source_system": "System B",
            "vend_source_system_id": "SS54321",
            "vat_number": "VAT654321",
            "is_active": True,
            "is_delete": False
        }

        # Invalid payload for update
        self.invalid_update_payload = {
            "legal_entity_name": "",  # Example of invalid data
            "address_zip_code": "54321"
        }

    def test_retrieve_legal_entity(self):
        """
        Ensure that a LegalEntity can be retrieved successfully.
        """
        response = self.client.get(self.url_update, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['legal_entity_name'], self.legal_entity.legal_entity_name)

    def test_update_legal_entity_with_valid_payload(self):
        """
        Ensure that a legal entity can be updated successfully with valid data.
        """
        response = self.client.put(self.url_update, self.valid_update_payload, format='json')

        # Debugging: Print response details
        print("Response status code:", response.status_code)
        print("Response data:", response.data)

        # Assert that the update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the instance from the database and verify changes
        self.legal_entity.refresh_from_db()
        self.assertEqual(self.legal_entity.legal_entity_name, "Updated Legal Entity")

    def test_update_legal_entity_with_invalid_payload(self):
        """
        Ensure that updating a LegalEntity fails with invalid data.
        """
        response = self.client.put(self.url_update, self.invalid_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify that the entity name was not updated
        self.legal_entity.refresh_from_db()
        self.assertNotEqual(self.legal_entity.legal_entity_name, "")  # Ensure no invalid data update

    def test_partial_update_legal_entity(self):
        """
        Ensure that a LegalEntity can be partially updated successfully.
        """
        partial_update_payload = {
            "legal_entity_name": "Partially Updated Entity"
        }
        response = self.client.patch(self.url_update, partial_update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the instance from the database and verify partial update
        self.legal_entity.refresh_from_db()
        self.assertEqual(self.legal_entity.legal_entity_name, "Partially Updated Entity")

    def test_update_legal_entity_not_found(self):
        """
        Test case for updating a non-existent entity.
        """
        url_invalid = reverse('legal_entity_modify', kwargs={'pk': 999})  # Non-existent ID
        payload = {
            "legal_entity_name": "Non-Existent Entity"
        }
        response = self.client.put(url_invalid, payload, format='json')

        # Assert that the entity was not found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "Not found.")


class LegalEntityFilterApiTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Creating some LegalEntity data to filter
        LegalEntity.objects.create(
            legal_entity_id="LE001",
            legal_entity_name="Legal Entity A",
            address_city="Metropolis",
            address_country_region_id="US",
            address_country_region_iso_code="US",
            address_description="Description A",
            address_street="123 Main St",
            address_zip_code="12345",
            vendor_account_number="V12345",
            sales_tax_group_code="STG123",
            bank_account_id="BA12345",
            currency_code="USD",
            on_hold_status="No",
            vendor_group_id="VG123",
            vendor_hold_release_date=None,
            vendor_organization_name="Legal Org A",
            vendor_type="Type A",
            vend_source_system="System A",
            vend_source_system_id="SS12345",
            vat_number="VAT123456",
            is_active=True,
            is_delete=False
        )
        LegalEntity.objects.create(
            legal_entity_id="LE002",
            legal_entity_name="Legal Entity B",
            address_city="Gotham",
            address_country_region_id="GB",
            address_country_region_iso_code="GB",
            address_description="Description B",
            address_street="456 Another St",
            address_zip_code="54321",
            vendor_account_number="V54321",
            sales_tax_group_code="STG456",
            bank_account_id="BA54321",
            currency_code="EUR",
            on_hold_status="Yes",
            vendor_group_id="VG456",
            vendor_hold_release_date=None,
            vendor_organization_name="Legal Org B",
            vendor_type="Type B",
            vend_source_system="System B",
            vend_source_system_id="SS54321",
            vat_number="VAT654321",
            is_active=False,
            is_delete=False
        )

    def test_legal_entity_filter_by_name(self):
        """
        Test filtering LegalEntities by name.
        """
        url = reverse('legal_entity_filter')
        filter_payload = {
            "legal_entity_name": "Legal Entity A",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['legal_entity_name'], "Legal Entity A")

    def test_legal_entity_filter_by_city(self):
        """
        Test filtering LegalEntities by city.
        """
        url = reverse('legal_entity_filter')
        filter_payload = {
            "address_city": "Gotham",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['address_city'], "Gotham")

    def test_legal_entity_filter_invalid_page(self):
        """
        Test filtering with an invalid page number.
        """
        url = reverse('legal_entity_filter')
        filter_payload = {
            "page": 3,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Page not found")

    def test_legal_entity_filter_with_ordering(self):
        """
        Test filtering with ordering by legal_entity_name ascending.
        """
        url = reverse('legal_entity_filter')
        filter_payload = {
            "order_by": "legal_entity_name",
            "order_type": "asc",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['legal_entity_name'], "Legal Entity A")
        self.assertEqual(response.data['results'][1]['legal_entity_name'], "Legal Entity B")

    def test_legal_entity_filter_by_active_status(self):
        """
        Test filtering LegalEntities by active status.
        """
        url = reverse('legal_entity_filter')
        filter_payload = {
            "is_active": True,
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')

        # Print response details for debugging
        print("Response status code:", response.status_code)
        print("Response data:", response.data)

        # Verify status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the correct number of results
        results = response.data['results']
        print("Filtered results:", results)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['legal_entity_name'], "Legal Entity A")

    def test_legal_entity_filter_by_vat_number(self):
        """
        Test filtering LegalEntities by VAT number.
        """
        url = reverse('legal_entity_filter')
        filter_payload = {
            "vat_number": "VAT654321",
            "page": 1,
            "page_size": 10
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['vat_number'], "VAT654321")
