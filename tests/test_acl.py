import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from acl.models import AppConfiguration, Role, RolePermission, MasterPrivilege

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
        # before list first populate some of the privileges
        self.client.post(reverse('populate_privileges'), {}, format='json')
        url = reverse('privilege_list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data["results"], list)
        # self.assertEqual(data["count"], 99)

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

    def test_privilege_list_filter_by_order_type(self):
        url = reverse('privilege_list')
        payload = {
            'order_by': 'privilege_name',
            'order_type': 'desc'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PopulatePrivilegesTestCase(BaseTestCase):
    def test_populate_privileges(self):
        url = reverse('populate_privileges')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Permissions populated successfully.", response.json()['message'])
        # self.assertEqual(MasterPrivilege.objects.count(), 99)


class DeleteAllPrivilegesApiViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create some sample privileges
        MasterPrivilege.objects.create(
            namespace="namespace1",
            privilege_name="privilege1",
            privilege_desc="Description 1",
            module_id="module1"
        )
        MasterPrivilege.objects.create(
            namespace="namespace2",
            privilege_name="privilege2",
            privilege_desc="Description 2",
            module_id="module2"
        )

    def test_delete_all_privileges_success(self):
        # Verify privileges exist before deletion
        self.assertEqual(MasterPrivilege.objects.count(), 2)

        url = reverse('delete-all-privileges')
        response = self.client.delete(url)

        # Verify successful deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MasterPrivilege.objects.count(), 0)

    def test_delete_all_privileges_no_content(self):
        # Clear all privileges before making delete request
        MasterPrivilege.objects.all().delete()
        self.assertEqual(MasterPrivilege.objects.count(), 0)

        url = reverse('delete-all-privileges')
        response = self.client.delete(url)

        # Verify no content is returned
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MasterPrivilege.objects.count(), 0)


class RoleCreateAPITestCase(BaseTestCase):
    valid_payload = {
        "role_name": "Admin",
        "role_description": "Administrator role with full permissions",
        "client_id": 1,
        "privilege_names": ["VIEW_ROLE", "CREATE_DEPARTMENT", "VIEW_USER_LIST"]
    }
    invalid_payload = {
        "role_name": "",
        "role_description": "Invalid role without a name",
        "client_id": 1,
        "privilege_names": ["invalid_privilege"]
    }

    def test_create_role_success(self):
        url = reverse('role_create')
        privileges_url = reverse('populate_privileges')

        # Populate privileges if needed
        self.client.post(privileges_url, {}, format="json")

        response = self.client.post(url, self.valid_payload, format='json')
        print(response.status_code)  # Debug print statement
        print(response.data)  # Debug print statement
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_role_WithDuplicateName(self):
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["EDIT_SLA", "VIEW_ROLE"]
        }
        valid_payload_duplicate = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["EDIT_SLA", "VIEW_ROLE"]
        }
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")
        self.client.post(url, valid_payload, format='json')
        response = self.client.post(url, valid_payload_duplicate, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual("please provide valid privilege", data["message"])

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

    def test_create_role_invalid_data_types(self):
        """
        Test role creation with invalid data types for the fields.
        """
        url = reverse('role_create')
        invalid_data_types_payload = {
            "role_name": 123,  # role_name should be a string
            "role_description": 456,  # role_description should be a string
            "client_id": 789,  # client_id should be a string
            "privilege_names": [True, False]  # privilege_names should be a list of strings
        }
        response = self.client.post(url, invalid_data_types_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_role_empty_role_name(self):
        """
        Test role creation with an empty role name.
        """
        url = reverse('role_create')
        empty_role_name_payload = {
            "role_name": "",
            "role_description": "Role with empty name",
            "client_id": 1,
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        response = self.client.post(url, empty_role_name_payload, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)
        self.assertEqual("role_name field may not be blank.", response.data["message"])

    def test_create_role_empty_payload(self):
        url = reverse("role_create")
        empty_payload = {}
        response = self.client.post(url, empty_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.json())
        self.assertIn("privilege_names", response.json()['error'])
        self.assertIn('role_name', response.json()['error'])

    def test_role_create_unauthorized(self):
        """
        Test role creation when the user is not authenticated.
        """
        self.client.logout()  # just removing the token, for  not getting authenticated.
        url = reverse('role_create')
        data = {
            "role_name": "Test Role",
            "role_description": "Test Role Description",
            "client_id": "1",
            "privilege_names": ["VIEW_USER"]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual("Authentication credentials were not valid", response.json()['message'])


class RoleFilterApiTestCase(BaseTestCase):
    def test_role_list_success(self):
        # populate privileges
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")

        url = reverse('role_list')
        # first create a role
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        res1 = self.client.post(reverse('role_create'), valid_payload, format='json')
        valid_payload = {}
        response = self.client.post(url, valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data['results'], list)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['role_name'], "Admin")
        self.assertEqual(data['results'][0]['role_description'], "Administrator role with full permissions")

    def test_role_list_invalid_page(self):
        # populate privileges
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")
        # first create a role
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        self.client.post(reverse('role_create'), valid_payload, format='json')
        url = reverse('role_list')
        invalid_payload_page = {
            "page": -1,
            "page_size": 10
        }
        response = self.client.post(url, invalid_payload_page, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'page and page size should be positive integer')

    def test_role_list_invalid_page_size(self):
        # populate privileges
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")
        # first create a role
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        self.client.post(reverse('role_create'), valid_payload, format='json')
        url = reverse('role_list')
        invalid_payload_page_size = {
            "page": 1,
            "page_size": -10
        }
        response = self.client.post(url, invalid_payload_page_size, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'page and page size should be positive integer')

    def test_role_list_filter(self):
        # populate privileges
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")
        # first create a role
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        self.client.post(reverse('role_create'), valid_payload, format='json')
        url = reverse('role_list')
        filter_payload = {
            "page": 1,
            "page_size": 10,
            "role_name": "Admin"
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data['results'], list)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['role_name'], "Admin")
        self.assertEqual(data['results'][0]['role_description'], "Administrator role with full permissions")

    def test_role_list_order_by(self):
        # populate privileges
        privileges_url = reverse("populate_privileges")
        self.client.post(privileges_url, {}, format="json")
        # first create a role
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        self.client.post(reverse('role_create'), valid_payload, format='json')
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

    def test_role_list_filter_client_id(self):
        # populate privileges
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")
        # first create a role
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        self.client.post(reverse('role_create'), valid_payload, format='json')
        url = reverse('role_list')
        filter_payload = {
            "client_id": 1
        }
        response = self.client.post(url, filter_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.json())
        data = response.json()
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['results'][0]['role_name'], "Admin")
        self.assertEqual(data['results'][0]['role_description'], "Administrator role with full permissions")


class RoleUpdateDeleteApiTestCase(BaseTestCase):
    def test_update_role_success(self):
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

        # now lets update the role
        url_update_role = reverse("role_update", kwargs={'pk': response_created.json()['id']})
        update_data = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT", "VIEW_USER_SHORT_INFO_LIST"]
        }
        response = self.client.put(url_update_role, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.json())

    def test_update_role_invalid(self):
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
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")
        response_created = self.client.post(url, valid_payload, format='json')
        url_update_role = reverse('role_update', kwargs={'pk': response_created.json()['id']})
        response = self.client.delete(url_update_role, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_role_not_found(self):
        """
            This test will check that  trying to update a role that doesn't exist
            returns a 404 status code.
        """
        # Generate a random UUID that does not correspond to any existing role
        random_uuid = uuid.uuid4()
        url_update_role = reverse("role_update", kwargs={'pk': random_uuid})

        update_data = {
            "role_name": "NonExistentRole",
            "role_description": "This role does not exist",
            "client_id": 1,
            "privilege_names": ["CREATE_APPLICATION"]
        }

        response = self.client.put(url_update_role, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RolePrivilegesListTestCase(BaseTestCase):
    def test_role_privileges_success(self):
        # first populate privilege and create a Role
        url = reverse('role_create')
        valid_payload = {
            "role_name": "Admin",
            "role_description": "Administrator role with full permissions",
            "client_id": 1,
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        privileges_url = reverse('populate_privileges')
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
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        privileges_url = reverse('populate_privileges')
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
            "privilege_names": ["VIEW_USER_LIST", "CREATE_DEPARTMENT"]
        }
        privileges_url = reverse('populate_privileges')
        self.client.post(privileges_url, {}, format="json")
        # response_created = self.client.post(url, valid_payload, format='json')
        url_get_single_role = reverse('role_detail_privileges', kwargs={'pk': 'fb12629f-f193-47fr-bdea-84991bd81625'})
        response = self.client.get(url_get_single_role, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_empty_role_list(self):
        """
        This test verifies that the API correctly handles
        cases where no roles exist in the database.
        """
        url = reverse('role_list_privileges')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data, [])

    def test_get_role_invalid_uuid(self):
        """
                This test verifies that the API properly handles
                an invalid UUID format in the request url.
        """
        invalid_uuid = "1234-invalid-uuid"
        url = reverse('role_detail_privileges', kwargs={'pk': invalid_uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], "Invalid UUID format")

    def test_get_role_not_found(self):
        """
            This test verifies that the API properly handles
            when a role with a valid UUID does not exist.
        """
        non_existent_uuid = uuid.uuid4()  # Generate a random UUID
        url = reverse('role_detail_privileges', kwargs={'pk': str(non_existent_uuid)})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], "Role not found")


class RoleUserCreateAPITestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # populate all the roles and create a User
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


# class ClientPrivilegeApiTestCase(BaseTestCase):
#     def test_create_client_privilege(self):
#         url = reverse('client_privilege')
#         payload = {
#             "privilege": 1,
#             "client": "Test Client"
#         }
#
#         response = self.client.post(url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         data = response.json()
#         self.assertIn("id", data)
#
#     def test_create_client_privilege_missing_privilege(self):
#         url = reverse('client_privilege')
#         payload = {
#             "client": "Test Client"
#         }
#
#         response = self.client.post(url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         data = response.json()
#         self.assertIn("error", data)
#
#     def test_create_client_privilege_missing_client(self):
#         url = reverse('client_privilege')
#         payload = {
#             "privilege": 1
#         }
#
#         response = self.client.post(url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         data = response.json()
#         self.assertIn("error", data)


# class ClientPrivilegeModifyApiTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client_privilege = ClientPrivilege.objects.create(
#             privilege=1,
#             client="Test Client",
#             created_by=str(self.user.id),
#         )
#         self.url = reverse('client_privilege_update', args=[self.client_privilege.id])
#
#     def test_retrieve_client_privilege(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEqual(data["id"], str(self.client_privilege.id))
#         self.assertEqual(data["privilege"], self.client_privilege.privilege)
#         self.assertEqual(data["client"], self.client_privilege.client)
#
#     def test_update_client_privilege(self):
#         payload = {
#             "privilege": 2,
#             "client": "Updated Client"
#         }
#
#         response = self.client.put(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEqual(data["id"], str(self.client_privilege.id))
#         self.assertEqual(data["privilege"], payload["privilege"])
#         self.assertEqual(data["client"], payload["client"])
#         self.assertEqual(data["modified_by"], self.user.id)
#
#         # Verify the updated data in the database
#         self.client_privilege.refresh_from_db()
#         self.assertEqual(self.client_privilege.privilege, payload["privilege"])
#         self.assertEqual(self.client_privilege.client, payload["client"])
#         self.assertEqual(self.client_privilege.modified_by, self.user.id)
#
#     def test_partial_update_client_privilege(self):
#         payload = {
#             "privilege": 3
#         }
#
#         response = self.client.patch(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEqual(data["id"], str(self.client_privilege.id))
#         self.assertEqual(data["privilege"], payload["privilege"])
#         self.assertEqual(data["client"], self.client_privilege.client)
#         self.assertEqual(data["modified_by"], self.user.id)
#
#         # Verify the updated data in the database
#         self.client_privilege.refresh_from_db()
#         self.assertEqual(self.client_privilege.privilege, payload["privilege"])
#         self.assertEqual(self.client_privilege.client, self.client_privilege.client)
#         self.assertEqual(self.client_privilege.modified_by, self.user.id)
#
#     def test_delete_client_privilege(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#         # Verify the object is deleted from the database
#         with self.assertRaises(ClientPrivilege.DoesNotExist):
#             ClientPrivilege.objects.get(id=self.client_privilege.id)
#
#     def test_invalid_uuid_format(self):
#         invalid_uuid_url = reverse('client_privilege_update', args=["291df079-755c-422a-ae89-e956h8b95bf5"])
#         response = self.client.get(invalid_uuid_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_role_does_not_exist(self):
#         non_existent_uuid = uuid.uuid4()
#         non_existent_url = reverse('client_privilege_update', args=[non_existent_uuid])
#         response = self.client.get(non_existent_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#
# class ClientPrivilegeFilterApiTestCase(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.privilege = MasterPrivilege.objects.create(
#             id=1,
#             privilege_name="Test Privilege"
#         )
#         self.client_id = 1
#
#         self.client_privilege = ClientPrivilege.objects.create(
#             privilege=self.privilege.id,
#             client=self.client_id,
#             created_by=str(self.user.id),
#         )
#         self.url = reverse('client_privilege_filter')
#
#     def test_filter_client_privilege(self):
#         payload = {
#             "privilege": self.privilege.id,
#             "client": self.client_id,
#             "page": 1,
#             "page_size": 10
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEqual(data["count"], 1)
#         self.assertEqual(len(data["results"]), 1)
#         self.assertEqual(data["results"][0]["id"], str(self.client_privilege.id))
#         self.assertEqual(data["results"][0]["privilege"]["id"], self.privilege.id)
#
#     def test_invalid_page_size(self):
#         payload = {
#             "privilege": self.privilege.id,
#             "client": self.client_id,
#             "page": 1,
#             "page_size": 0  # Invalid page size
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.json()["message"], "page and page size should be positive integer")
#
#     def test_invalid_page_number(self):
#         payload = {
#             "privilege": self.privilege.id,
#             "client": self.client_id,
#             "page": -1,  # Invalid page number
#             "page_size": 10
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.json()["message"], "page and page size should be positive integer")
#
#     def test_page_not_found(self):
#         payload = {
#             "privilege": self.privilege.id,
#             "client": self.client_id,
#             "page": 10,  # Page number beyond available pages
#             "page_size": 1
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.json()["message"], "Page not found")
#
#     def test_order_by_privilege(self):
#         payload = {
#             "order_by": "privilege",
#             "order_type": "desc",
#             "page": 1,
#             "page_size": 10
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEqual(data["count"], 1)
#         self.assertEqual(len(data["results"]), 1)
#         self.assertEqual(data["results"][0]["id"], str(self.client_privilege.id))
#         self.assertEqual(data["results"][0]["privilege"]["id"], self.privilege.id)
#
#     def test_invalid_filter(self):
#         payload = {
#             "privilege": 9999,  # Invalid privilege id
#             "client": self.client_id,
#             "page": 1,
#             "page_size": 10
#         }
#
#         response = self.client.post(self.url, payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         data = response.json()
#         self.assertEqual(data["count"], 0)
#         self.assertEqual(len(data["results"]), 0)


class AppConfigurationListCreateAPITest(BaseTestCase):

    def setUp(self):
        self.client = APIClient()
        # Create test user
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password',
            first_name='John',
            last_name='Doe'
        )
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Create a sample AppConfiguration
        self.config = AppConfiguration.objects.create(
            application_name="TestApp",
            email_history_days=30,
            activity_history_days=60,
            client_start_no="C001",
            project_start_no="P001",
            ticket_start_no="T001",
            ticket_auto_close_days=7,
            auto_notification_hours=24,
            created_by=self.user.email
        )

    def test_list_app_configurations(self):
        url = reverse('appconfiguration_list_create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['application_name'], self.config.application_name)

    def test_create_app_configuration(self):
        url = reverse('appconfiguration_list_create')
        data = {
            "application_name": "NewApp",
            "email_history_days": 45,
            "activity_history_days": 90,
            "client_start_no": "C002",
            "project_start_no": "P002",
            "ticket_start_no": "T002",
            "ticket_auto_close_days": 10,
            "auto_notification_hours": 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AppConfiguration.objects.count(), 2)
        self.assertEqual(AppConfiguration.objects.last().application_name, "NewApp")

    def test_create_app_configuration_duplicate_name(self):
        url = reverse('appconfiguration_list_create')
        data = {
            "application_name": "TestApp",  # Duplicate application_name
            "email_history_days": 45,
            "activity_history_days": 90,
            "client_start_no": "C003",
            "project_start_no": "P003",
            "ticket_start_no": "T003",
            "ticket_auto_close_days": 15,
            "auto_notification_hours": 48
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Application name must be unique.', response.data['message'])

    def test_create_app_configuration_missing_fields(self):
        url = reverse('appconfiguration_list_create')
        data = {
            "application_name": "IncompleteApp"
            # Missing required fields like email_history_days, activity_history_days, etc.
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.json())
        self.assertIn('email_history_days field is required.', response.json()['message'])
        self.assertIn('activity_history_days', response.json()['error'])


class AppConfigurationListUpdateDestroyTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.configuration = AppConfiguration.objects.create(
            application_name='Test App',
            email_history_days=30,
            activity_history_days=60,
            client_start_no='CS1001',
            project_start_no='PS1001',
            ticket_start_no='TS1001',
            ticket_auto_close_days=7,
            auto_notification_hours=24,
            created_by='testuser',
        )
        self.valid_payload = {
            'application_name': 'Updated App',
            'email_history_days': 45,
            'activity_history_days': 90,
            'client_start_no': 'CS2002',
            'project_start_no': 'PS2002',
            'ticket_start_no': 'TS2002',
            'ticket_auto_close_days': 14,
            'auto_notification_hours': 12,
        }
        self.invalid_payload = {
            'application_name': '',
            'email_history_days': -10,
            'activity_history_days': 'ninety',
            'client_start_no': '',
            'project_start_no': '',
            'ticket_start_no': '',
            'ticket_auto_close_days': '',
            'auto_notification_hours': '',
        }

    def test_retrieve_appconfiguration(self):
        response = self.client.get(
            reverse('appconfiguration_detail', kwargs={'pk': self.configuration.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['application_name'], self.configuration.application_name)
        self.assertEqual(response.data['email_history_days'], self.configuration.email_history_days)
        self.assertEqual(response.data['ticket_auto_close_days'], 7)

    def test_update_appconfiguration_valid(self):
        response = self.client.put(
            reverse('appconfiguration_detail', kwargs={'pk': self.configuration.pk}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.configuration.refresh_from_db()
        self.assertEqual(self.configuration.application_name, 'Updated App')
        self.assertEqual(self.configuration.email_history_days, 45)

    def test_update_appconfiguration_invalid(self):
        response = self.client.put(
            reverse('appconfiguration_detail', kwargs={'pk': self.configuration.pk}),
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.configuration.refresh_from_db()
        self.assertNotEqual(self.configuration.application_name, '')
        self.assertNotEqual(self.configuration.email_history_days, -10)

    def test_partial_update_appconfiguration(self):
        response = self.client.patch(
            reverse('appconfiguration_detail', kwargs={'pk': self.configuration.pk}),
            data={'application_name': 'Partially Updated App'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.configuration.refresh_from_db()
        self.assertEqual(self.configuration.application_name, 'Partially Updated App')

    def test_delete_appconfiguration(self):
        response = self.client.delete(
            reverse('appconfiguration_detail', kwargs={'pk': self.configuration.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AppConfiguration.objects.count(), 0)
