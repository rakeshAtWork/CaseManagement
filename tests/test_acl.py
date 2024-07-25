from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from acl.models import UserRole, ClientPrivilege, MasterPrivilege

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


class ListPrivilegesTestCase(BaseTestCase):
    def test_privilege_list(self):
        url = reverse('privilege_list')
        # data = {} # getting all the privileges

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Example assertions
        data = response.json()
        self.assertIsInstance(data["results"], list)

    def test_privilege_list_invalid_page(self):
        url = reverse('privilege_list')
        payload = {
            'page': -1,
            'page_size': 10
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'page and page size should be positive integer')

    def test_privilege_list_invalid_page_size(self):
        url = reverse('privilege_list')
        payload = {
            'page': 1,
            'page_size': -10
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'page and page size should be positive integer')

    def test_privilege_list_filter_by_role(self):
        url = reverse('privilege_list')
        payload = {
            'role_id': 1,
            'page': 1,
            'page_size': 10
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertIsInstance(data['results'], list)
        # Add more assertions based on your expected response

    def test_privilege_list_filter_by_privilege_name(self):
        url = reverse('privilege_list')
        payload = {
            'privilege_name': 'CREATE_APPLICATION',
            'page': 1,
            'page_size': 10
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertIsInstance(data['results'], list)


class PopulatePrivilegesTestCase(BaseTestCase):
    def test_populate_privileges(self):
        url = reverse('populate-privileges')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Permissions populated successfully.", response.json()['message'])
        # from .models import Privilege
        # self.assertEqual(Privilege.objects.count(), 35)


class RoleCreateAPITestCase(BaseTestCase):
    valid_payload = {
        "role_name": "Admin",
        "role_description": "Administrator role with full permissions",
        "client_id": 1,
        "privilege_names": ["create_user", "delete_user"]
    }
    invalid_payload = {
        "role_name": "",
        "role_description": "Invalid role without a name",
        "client_id": 1,
        "privilege_names": ["invalid_privilege"]
    }

    def test_create_role_success(self):
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate-privileges')
        self.client.post(privileges_url, {}, format="json")
        response = self.client.post(url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIsInstance(data, dict)
        from acl.models import Role, RolePermission
        self.assertEqual(Role.objects.count(), 1)
        self.assertEqual(RolePermission.objects.count(), 2)

    def test_create_role_WithDuplicateName(self):
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        valid_payload_duplicate = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate-privileges')
        self.client.post(privileges_url, {}, format="json")
        self.client.post(url, valid_payload, format='json')
        response = self.client.post(url, valid_payload_duplicate, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_role_invalid_privilege(self):
        url = reverse("role_create")
        invalid_payload = {
            "role_name": "User",
            "role_description": "User roles with invalid privileges",
            "client_id": 1,
            "privilege_names": ["invalid_privilege"]
        }
        response = self.client.post(url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("please provide valid privilege", response.json()['error'])


class RoleFilterApiTestCase(BaseTestCase):
    def test_role_list_success(self):
        url = reverse('role_list')
        # first create a role
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        self.client.post(url, valid_payload, format='json')

        valid_payload = {}
        response = self.client.post(url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data['results'], list)

    def test_role_list_invalid_page(self):
        url = reverse('role_list')
        invalid_payload_page = {
            "page": -1,
            "page_size": 10
        }
        response = self.client.post(url, invalid_payload_page, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'page and page size should be positive integer')

    def test_role_list_invalid_page_size(self):
        url = reverse('role_list')
        invalid_payload_page_size = {
            "page": 1,
            "page_size": -10
        }
        response = self.client.post(url, invalid_payload_page_size, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'page and page size should be positive integer')

    def test_role_list_filter(self):
        url = reverse('role_list')
        filter_payload = {
            "page": 1,
            "page_size": 10,
            "role_name": "User"
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data['results'], list)

    def test_role_list_order_by(self):
        url = reverse("role_list")
        order_payload = {
            "page": 1,
            "page_size": 10,
            "order_by": "Admin",
            "order_type": "desc"
        }
        response = self.client.post(url, order_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data['results'], list)


class RoleUpdateDeleteApiTestCase(BaseTestCase):
    def test_update_role_success(self):
        # before updating lets create a new role
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate-privileges')
        self.client.post(privileges_url, {}, format="json")
        response_created = self.client.post(url, valid_payload, format='json')

        # now lets update the role
        url_update_role = reverse("role_update", kwargs={'pk': response_created.json()['id']})
        update_data = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST", "DELETE_CUSTOMER"]
        }
        response = self.client.put(url_update_role, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_role_invalid(self):
        # before updating lets create a new role
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate-privileges')
        self.client.post(privileges_url, {}, format="json")
        response_created = self.client.post(url, valid_payload, format='json')

        # now lets update the role
        url_update_role = reverse("role_update", kwargs={'pk': response_created.json()['id']})

        invalid_payload = {
            "role_name": "",
            "role_description": "Role without name",
            "client_id": 1,
            "privilege_names": ["privilege1", "privilege2"]
        }
        response = self.client.put(url_update_role, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_role_success(self):
        # before delete lets create a new role
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate-privileges')
        self.client.post(privileges_url, {}, format="json")
        response_created = self.client.post(url, valid_payload, format='json')
        url_update_role = reverse('role_update', kwargs={'pk': response_created.json()['id']})
        response = self.client.delete(url_update_role, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RolePrivilegesListTestCase(BaseTestCase):
    def test_role_privileges_success(self):
        # first populate privilege and create a Role
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate-privileges')
        self.client.post(privileges_url, {}, format="json")
        self.client.post(url, valid_payload, format='json')
        url_role_privileges = reverse('role_list_privileges')
        response = self.client.get(url_role_privileges, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_role_valid_uuid(self):
        # first populate privilege and create a Role
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate-privileges')
        self.client.post(privileges_url, {}, format="json")
        response_created = self.client.post(url, valid_payload, format='json')
        url_get_single_role = reverse('role_detail_privileges', kwargs={'pk': response_created.json()['id']})
        response = self.client.get(url_get_single_role, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_role_invalid_uuid(self):
        # first populate privilege and create a Role
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate-privileges')
        self.client.post(privileges_url, {}, format="json")
        response_created = self.client.post(url, valid_payload, format='json')
        url_get_single_role = reverse('role_detail_privileges', kwargs={'pk': 'fb12629f-f193-47fr-bdea-84991bd81625'})
        response = self.client.get(url_get_single_role, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


from acl.models import Role
import uuid


class RoleUserCreateAPITestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # populate all the roles and create a User
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION", "VIEW_CLIENT_PERMISSION_LIST"]
        }
        privileges_url = reverse('populate-privileges')
        self.client.post(privileges_url, {}, format="json")
        response_created = self.client.post(url, valid_payload, format='json')
        self.role_id = response_created.json()['id']

    def test_assign_users_to_role_success(self):
        url = reverse('role_user_create')
        payload = {
            "role_id": str(self.role_id),
            "user_ids": [self.user.id]
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn("results", data)
        self.assertEqual(data["results"]["role_id"], str(self.role_id))
        self.assertCountEqual(data["results"]["user_ids"], [self.user.id])

    def test_invalid_role_id(self):
        url = reverse('role_user_create')
        payload = {
            "role_id": "fb12619f-f193-47fd-bdea-84991bd81625",
            "user_ids": [self.user.id]
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Please provide valid user data or role data")

    def test_invalid_user_ids(self):
        url = reverse('role_user_create')
        payload = {
            "role_id": str(self.role_id),
            "user_ids": ["invalid_user_id"]
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.json()["message"], "Please provide valid user data or role data")


class ClientPrivilegeApiTestCase(BaseTestCase):
    def test_create_client_privilege(self):
        url = reverse('client_privilege')
        payload = {
            "privilege": 1,
            "client": "Test Client"
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn("id", data)

    def test_create_client_privilege_missing_privilege(self):
        url = reverse('client_privilege')
        payload = {
            "client": "Test Client"
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("error", data)

    def test_create_client_privilege_missing_client(self):
        url = reverse('client_privilege')
        payload = {
            "privilege": 1
        }

        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("error", data)


class ClientPrivilegeModifyApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client_privilege = ClientPrivilege.objects.create(
            privilege=1,
            client="Test Client",
            created_by=str(self.user.id),
        )
        self.url = reverse('client_privilege_update', args=[self.client_privilege.id])

    def test_retrieve_client_privilege(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], str(self.client_privilege.id))
        self.assertEqual(data["privilege"], self.client_privilege.privilege)
        self.assertEqual(data["client"], self.client_privilege.client)

    def test_update_client_privilege(self):
        payload = {
            "privilege": 2,
            "client": "Updated Client"
        }

        response = self.client.put(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], str(self.client_privilege.id))
        self.assertEqual(data["privilege"], payload["privilege"])
        self.assertEqual(data["client"], payload["client"])
        self.assertEqual(data["modified_by"], self.user.id)

        # Verify the updated data in the database
        self.client_privilege.refresh_from_db()
        self.assertEqual(self.client_privilege.privilege, payload["privilege"])
        self.assertEqual(self.client_privilege.client, payload["client"])
        self.assertEqual(self.client_privilege.modified_by, self.user.id)

    def test_partial_update_client_privilege(self):
        payload = {
            "privilege": 3
        }

        response = self.client.patch(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], str(self.client_privilege.id))
        self.assertEqual(data["privilege"], payload["privilege"])
        self.assertEqual(data["client"], self.client_privilege.client)
        self.assertEqual(data["modified_by"], self.user.id)

        # Verify the updated data in the database
        self.client_privilege.refresh_from_db()
        self.assertEqual(self.client_privilege.privilege, payload["privilege"])
        self.assertEqual(self.client_privilege.client, self.client_privilege.client)
        self.assertEqual(self.client_privilege.modified_by, self.user.id)

    def test_delete_client_privilege(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the object is deleted from the database
        with self.assertRaises(ClientPrivilege.DoesNotExist):
            ClientPrivilege.objects.get(id=self.client_privilege.id)

    def test_invalid_uuid_format(self):
        invalid_uuid_url = reverse('client_privilege_update', args=["291df079-755c-422a-ae89-e956h8b95bf5"])
        response = self.client.get(invalid_uuid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_role_does_not_exist(self):
        non_existent_uuid = uuid.uuid4()
        non_existent_url = reverse('client_privilege_update', args=[non_existent_uuid])
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ClientPrivilegeFilterApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.privilege = MasterPrivilege.objects.create(
            id=1,
            privilege_name="Test Privilege"
        )
        self.client_id = 1

        self.client_privilege = ClientPrivilege.objects.create(
            privilege=self.privilege.id,
            client=self.client_id,
            created_by=str(self.user.id),
        )
        self.url = reverse('client_privilege_filter')

    def test_filter_client_privilege(self):
        payload = {
            "privilege": self.privilege.id,
            "client": self.client_id,
            "page": 1,
            "page_size": 10
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["id"], str(self.client_privilege.id))
        self.assertEqual(data["results"][0]["privilege"]["id"], self.privilege.id)

    def test_invalid_page_size(self):
        payload = {
            "privilege": self.privilege.id,
            "client": self.client_id,
            "page": 1,
            "page_size": 0  # Invalid page size
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "page and page size should be positive integer")

    def test_invalid_page_number(self):
        payload = {
            "privilege": self.privilege.id,
            "client": self.client_id,
            "page": -1,  # Invalid page number
            "page_size": 10
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "page and page size should be positive integer")

    def test_page_not_found(self):
        payload = {
            "privilege": self.privilege.id,
            "client": self.client_id,
            "page": 10,  # Page number beyond available pages
            "page_size": 1
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Page not found")

    def test_order_by_privilege(self):
        payload = {
            "order_by": "privilege",
            "order_type": "desc",
            "page": 1,
            "page_size": 10
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["id"], str(self.client_privilege.id))
        self.assertEqual(data["results"][0]["privilege"]["id"], self.privilege.id)

    def test_invalid_filter(self):
        payload = {
            "privilege": 9999,  # Invalid privilege id
            "client": self.client_id,
            "page": 1,
            "page_size": 10
        }

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["count"], 0)
        self.assertEqual(len(data["results"]), 0)
