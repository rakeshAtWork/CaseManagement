from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model

from configuration.models import Configuration
from acl.models import MasterModule

User = get_user_model()

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

        # Setup MasterModule for valid tests
        self.master_module = MasterModule.objects.create(module_id=1, name="Test Module")

class ConfigurationCreateApiTest(BaseTestCase):
    def test_create_configuration_success(self):
        url = reverse('configuration_list_create')
        data = {
            "user_preference_setting": [
                {
                    "label": "Test Label",
                    "key": "test_key",
                    "is_disabled": False,
                    "width": 100,
                    "is_sortable": True,
                    "is_filterable": True,
                    "filter_type": "text",
                    "is_selected": True,
                    "module_id": self.master_module.module_id,
                    "user_id": self.user.id
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['label'], 'Test Label')
        self.assertEqual(Configuration.objects.count(), 1)

    def test_create_configuration_missing_module_id(self):
        url = reverse('configuration_list_create')
        data = {
            "user_preference_setting": [
                {
                    "label": "Test Label",
                    "key": "test_key",
                    "is_disabled": False,
                    "width": 100,
                    "is_sortable": True,
                    "is_filterable": True,
                    "filter_type": "text",
                    "is_selected": True,
                    "user_id": self.user.id
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())

    def test_create_configuration_invalid_module_id(self):
        url = reverse('configuration_list_create')
        data = {
            "user_preference_setting": [
                {
                    "label": "Test Label",
                    "key": "test_key",
                    "is_disabled": False,
                    "width": 100,
                    "is_sortable": True,
                    "is_filterable": True,
                    "filter_type": "text",
                    "is_selected": True,
                    "module_id": 999,  # Invalid module ID
                    "user_id": self.user.id
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())

    def test_create_configuration_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        url = reverse('configuration_list_create')
        data = {
            "user_preference_setting": [
                {
                    "label": "Test Label",
                    "key": "test_key",
                    "is_disabled": False,
                    "width": 100,
                    "is_sortable": True,
                    "is_filterable": True,
                    "filter_type": "text",
                    "is_selected": True,
                    "module_id": self.master_module.module_id,
                    "user_id": self.user.id
                }
            ]
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ConfigurationListApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        Configuration.objects.create(
            label="Test Label 1",
            key="test_key_1",
            is_disabled=False,
            width=100,
            is_sortable=True,
            is_filterable=True,
            filter_type="text",
            is_selected=True,
            module_id=self.master_module.module_id,
            user_id=self.user.id
        )
        Configuration.objects.create(
            label="Test Label 2",
            key="test_key_2",
            is_disabled=False,
            width=200,
            is_sortable=False,
            is_filterable=False,
            filter_type="number",
            is_selected=False,
            module_id=self.master_module.module_id,
            user_id=self.user.id
        )

    def test_list_configurations_success(self):
        url = reverse('configuration_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Directly check the length of the list
        self.assertEqual(len(response.data), 2)

    def test_list_configurations_with_filter(self):
        url = reverse('configuration_list')  # Ensure this is your correct URL for listing
        response = self.client.get(url, {'filter_param': 'some_value'},
                                   format='json')  # Adjust filter_param accordingly

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Correctly check the length of the list
        self.assertEqual(len(response.data), 2)

    def test_list_configurations_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        url = reverse('configuration_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ConfigurationModifyApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.configuration = Configuration.objects.create(
            label="Initial Label",
            key="initial_key",
            is_disabled=False,
            width=100,
            is_sortable=True,
            is_filterable=True,
            filter_type="text",
            is_selected=True,
            module_id=self.master_module.module_id,
            user_id=self.user.id
        )

    def test_retrieve_configuration_success(self):
        url = reverse('configuration_detail', kwargs={'pk': self.configuration.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'Initial Label')

    def test_update_configuration_success(self):
        url = reverse('configuration_detail', kwargs={'pk': self.configuration.id})
        data = {
            "label": "Updated Label"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'Updated Label')
        self.configuration.refresh_from_db()
        self.assertEqual(self.configuration.label, 'Updated Label')

    def test_delete_configuration_success(self):
        url = reverse('configuration_detail', kwargs={'pk': self.configuration.id})
        response = self.client.delete(url)

        print(f"Status Code: {response.status_code}")  # Should be 204
        print(f"Response Content: {response.content}")  # Should be empty

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Debugging: Fetch the configuration instance again
        configuration = Configuration.objects.filter(id=self.configuration.id).first()
        if configuration:
            print(f"Configuration exists with ID: {configuration.id}")
            print(f"Configuration is_deleted flag: {getattr(configuration, 'is_deleted', 'Not applicable')}")

    def test_delete_configuration_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        url = reverse('configuration_detail', kwargs={'pk': self.configuration.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_non_existent_configuration(self):
        url = reverse('configuration_detail', kwargs={'pk': 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
