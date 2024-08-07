from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from ticket_management.models import Category, TicketType, Department, Priority, SLA, ProjectManagement, UserDepartment, \
    Status, Ticket, TicketBehalf, TicketRevision, TicketFollower
import uuid
from datetime import timedelta
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


class TicketTypeCreateApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_create_ticket_type_success(self):
        url = reverse('ticket-create')
        data = {
            "name": "Bug",
            "is_active": True
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Bug')
        self.assertTrue(response.data['is_active'])
        ticket_type = TicketType.objects.get(id=response.data['id'])
        self.assertEqual(ticket_type.name, 'Bug')
        self.assertEqual(ticket_type.created_by, self.user.id)

    def test_create_ticket_type_missing_name(self):
        url = reverse('ticket-create')
        data = {
            "is_active": True
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error'])

    def test_create_ticket_type_long_name(self):
        url = reverse('ticket-create')
        data = {
            "name": "A" * 256,  # Assuming the max_length is 255
            "is_active": True
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error'])

    def test_create_ticket_type_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        url = reverse('ticket-create')
        data = {
            "name": "Bug",
            "is_active": True
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TicketTypeUpdateApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.ticket_type = TicketType.objects.create(
            name="Bug",
            is_active=True,
            created_by=self.user.id
        )
        self.update_url = reverse('ticket-update', kwargs={'pk': self.ticket_type.id})

    def test_update_ticket_type_success(self):
        data = {
            "name": "Feature",
            "is_active": False
        }

        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket_type.refresh_from_db()
        self.assertEqual(self.ticket_type.name, 'Feature')
        self.assertFalse(self.ticket_type.is_active)

    def test_update_ticket_type_missing_name(self):
        data = {
            "is_active": False
        }

        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error'])

    def test_update_ticket_type_long_name(self):
        data = {
            "name": "A" * 256,  # Assuming the max_length is 255
            "is_active": True
        }

        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data['error'])

    def test_update_ticket_type_not_found(self):
        non_existent_id = uuid.uuid4()
        url = reverse('ticket-update', kwargs={'pk': non_existent_id})
        data = {
            "name": "Feature",
            "is_active": False
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_ticket_type_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "name": "Feature",
            "is_active": False
        }

        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SLACreateApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.create_url = reverse('sla_create')
        # Create necessary related objects
        self.department = Department.objects.create(department_name="IT", department_code="IT001")
        self.ticket_type = TicketType.objects.create(name="Bug", is_active=True, created_by=self.user.id)
        self.priority = Priority.objects.create(name="High")

    def test_create_sla_success(self):
        data = {
            "department": self.department.id,
            "ticket_type": self.ticket_type.id,
            "priority": self.priority.id,
            "response_time": "1:00:00",
            "resolution_time": "2:00:00"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sla_missing_fields(self):
        data = {
            "department": self.department.id,
            "priority": self.priority.id,
            "response_time": "1:00:00"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ticket_type', response.data['error'])
        self.assertIn('resolution_time', response.data['error'])

    def test_create_sla_invalid_data(self):
        data = {
            "department": self.department.id,
            "ticket_type": self.ticket_type.id,
            "priority": self.priority.id,
            "response_time": "invalid",
            "resolution_time": "2:00:00"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('response_time', response.data['error'])

    def test_create_sla_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "department": self.department.id,
            "ticket_type": self.ticket_type.id,
            "priority": self.priority.id,
            "response_time": "1:00:00",
            "resolution_time": "2:00:00"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SLARetrieveUpdateDeleteTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create necessary related objects
        self.department = Department.objects.create(department_name="IT", department_code="IT001")
        self.ticket_type = TicketType.objects.create(name="Bug", is_active=True, created_by=self.user.id)
        self.priority = Priority.objects.create(name="High")
        self.sla = SLA.objects.create(
            department=self.department,
            ticket_type=self.ticket_type,
            priority=self.priority,
            response_time=timedelta(hours=1),
            resolution_time=timedelta(hours=2),
            created_by=self.user.id
        )
        self.retrieve_url = reverse('sla_update', args=[self.sla.id])
        self.non_existent_url = reverse('sla_update', args=[uuid.uuid4()])

    def test_retrieve_sla_success(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.sla.id))
        self.assertEqual(str(response.data['department']), str(self.department.id))
        self.assertEqual(str(response.data['ticket_type']), str(self.ticket_type.id))
        self.assertEqual(str(response.data['priority']), str(self.priority.id))

    def test_update_sla_success(self):
        data = {
            "department": self.department.id,
            "ticket_type": self.ticket_type.id,
            "priority": self.priority.id,
            "response_time": "2:00:00",
            "resolution_time": "4:00:00"
        }
        response = self.client.put(self.retrieve_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sla.refresh_from_db()
        self.assertEqual(self.sla.response_time, timedelta(hours=2))
        self.assertEqual(self.sla.resolution_time, timedelta(hours=4))

    def test_delete_sla_success(self):
        response = self.client.delete(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SLA.objects.filter(id=self.sla.id).exists())

    def test_retrieve_non_existent_sla(self):
        response = self.client.get(self.non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_sla_invalid_data(self):
        data = {
            "response_time": "invalid_time"
        }
        response = self.client.put(self.retrieve_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('response_time', response.data['error'])

    def test_delete_non_existent_sla(self):
        response = self.client.delete(self.non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_sla_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_sla_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "response_time": "2:00:00",
            "resolution_time": "4:00:00"
        }
        response = self.client.put(self.retrieve_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_sla_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.delete(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DepartmentCreateApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create a category to use as department_type
        self.category = Category.objects.create(
            name="IT",
        )

        self.create_url = reverse('department_create')

    def test_create_department_success(self):
        data = {
            "department_name": "Engineering",
            "department_code": "ENG001",
            "department_type": self.category.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['department_name'], "Engineering")
        self.assertEqual(response.data['department_code'], "ENG001")
        self.assertEqual(response.data['department_type'], self.category.id)
        self.assertEqual(response.data['created_by'], self.user.id)

    def test_create_department_invalid_data(self):
        data = {
            "department_name": "",  # Invalid name
            "department_code": "ENG001",
            "department_type": self.category.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('department_name', response.data['error'])

    def test_create_department_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "department_name": "Engineering",
            "department_code": "ENG001",
            "department_type": self.category.id
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DepartmentFilterApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create categories to use for department_type
        self.category1 = Category.objects.create(name="HR")
        self.category2 = Category.objects.create(name="IT")

        # Create departments to test filtering
        self.department1 = Department.objects.create(
            department_name="Human Resources",
            department_code="HR001",
            department_type=self.category1,
            created_by=self.user
        )
        self.department2 = Department.objects.create(
            department_name="Information Technology",
            department_code="IT001",
            department_type=self.category2,
            created_by=self.user
        )

        self.filter_url = reverse('department_list')

    def test_filter_department_success(self):
        data = {

        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_department_invalid_page(self):
        data = {
            "department_name": "Human",
            "order_by": "department_name",
            "order_type": "asc",
            "page_size": 1,
            "page": -1  # Invalid page number
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "page and page size should be positive integer")

    def test_filter_department_no_results(self):
        data = {
            "department_name": "Nonexistent",
            "order_by": "department_name",
            "order_type": "asc",
            "page_size": 10,
            "page": 1
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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


class PriorityApiTests(BaseTestCase):
    def setUp(self):
        super().setUp()  # Calls the setup in the BaseTestCase for authentication
        self.url = reverse('priority_list_create')
        self.priority = Priority.objects.create(
            name="High",
            description="High priority level",
            level="P1",
            created_by=self.user,
            updated_by=self.user
        )
        self.category = Priority.objects.create(name="Initial Priority", created_by=self.user)
        self.priority_detail_url = reverse('priority_detail_update_delete', kwargs={'pk': self.priority.id})

    def test_create_priority(self):
        data = {
            "name": "Medium",
            "description": "Medium priority level",
            "level": "P2"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Medium')

    def test_create_priority_missing_name(self):
        data = {
            "description": "High priority level",
            "level": "P1"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)

    def test_list_priority(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_priority(self):
        data = {
            "name": "Critical",
            "description": "Critical priority level",
            "level": "P0"
        }
        response = self.client.put(self.priority_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Critical')

    def test_delete_priority(self):
        response = self.client.delete(self.priority_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_priority(self):
        response = self.client.get(self.priority_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'High')
        self.assertEqual(response.data['description'], 'High priority level')
        self.assertEqual(response.data['level'], 'P1')


class DepartmentUpdateApiTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Create categories to use for department_type
        self.category = Category.objects.create(name="HR")

        # Create a department to test update and delete
        self.department = Department.objects.create(
            department_name="Human Resources",
            department_code="HR001",
            department_type=self.category,
            created_by=self.user
        )

        self.update_url = reverse('department_update', args=[self.department.id])

    def test_update_department_success(self):
        data = {
            "department_name": "HR & Admin",
            "department_code": "HR002",
            "department_type": self.category.id
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


class ProjectCreateApiTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.create_url = reverse('project_create')

    def test_create_project_success(self):
        data = {
            "client_id": "CL001",
            "department_id": "DEP001",
            "project_id": "PRJ001",
            "project_manager_primary": "John Doe",
            "support_group_email": "support@cozentus.com",
            "product_owner": "Jane Smith",
            "contact_name": "Alice Johnson",
            "contact_email": "alice@cozentus.com"
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectManagement.objects.count(), 1)
        project = ProjectManagement.objects.get()
        self.assertEqual(project.client_id, "CL001")
        self.assertEqual(project.department_id, "DEP001")

    def test_create_project_missing_required_fields(self):
        data = {
            "client_id": "CL001"
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", str(response.data))

    def test_create_project_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "client_id": "CL001",
            "department_id": "DEP001",
            "project_id": "PRJ001",
            "project_manager_primary": "John Doe",
            "support_group_email": "support@cozentus.com",
            "product_owner": "Jane Smith",
            "contact_name": "Alice Johnson",
            "contact_email": "alice@cozentus.com"
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProjectFilterApiTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.filter_url = reverse('project_list_filter')

        # Create sample project data for filtering tests
        self.project1 = ProjectManagement.objects.create(
            client_id="CL001", department_id="DEP001", project_id="PRJ001", project_manager_primary="John Doe",
            support_group_email="support@cozentus.com", product_owner="Jane Smith",
            contact_name="Alice Johnson", contact_email="alice@cozentus.com", created_by=self.user.id
        )
        self.project2 = ProjectManagement.objects.create(
            client_id="CL002", department_id="DEP002", project_id="PRJ002", project_manager_primary="Michael Smith",
            support_group_email="support2@cozentus.com", product_owner="Emily Davis",
            contact_name="Bob Brown", contact_email="bob@cozentus.com", created_by=self.user.id
        )

    def test_filter_projects_invalid_page(self):
        data = {
            "page_size": 10,
            "page": 0  # Invalid page number
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("page and page size should be positive integer", str(response.data))

    def test_filter_projects_no_results(self):
        data = {
            "client_id": "NON_EXISTENT_CLIENT",
            "page_size": 10,
            "page": 1
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_projects_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        data = {
            "client_id": "CL001",
            "page_size": 10,
            "page": 1
        }
        response = self.client.post(self.filter_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProjectRetrieveUpdateDeleteApiTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.project = ProjectManagement.objects.create(
            client_id="CL001", department_id="DEP001", project_id="PRJ001", project_manager_primary="John Doe",
            support_group_email="support@cozentus.com", product_owner="Jane Smith",
            contact_name="Alice Johnson", contact_email="alice@cozentus.com", created_by=self.user.id
        )
        self.url = reverse('project_retrieve_update_destroy', kwargs={'pk': self.project.id})

    def test_retrieve_project(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.project.id)
        self.assertEqual(response.data['client_id'], self.project.client_id)

    def test_partial_update_project(self):
        partial_update_data = {
            "client_id": "CL003"
        }
        response = self.client.patch(self.url, partial_update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.client_id, "CL003")

    def test_delete_project(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.project.refresh_from_db()
        self.assertIsNotNone(self.project.deleted_at)

    def test_retrieve_nonexistent_project(self):
        url = reverse('project_retrieve_update_destroy', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_project(self):
        url = reverse('project_retrieve_update_destroy', kwargs={'pk': 99999})
        update_data = {
            "client_id": "CL002",
            "project_manager_primary": "Michael Smith"
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_project(self):
        url = reverse('project_retrieve_update_destroy', kwargs={'pk': 99999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_project_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        update_data = {
            "client_id": "CL002",
            "project_manager_primary": "Michael Smith"
        }
        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
        self.assertEqual(self.status.status_code, 2)

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
        self.category1 = Category.objects.create(name="HR")
        self.category2 = Category.objects.create(name="IT")

        self.department1 = Department.objects.create(
            department_name='HR',
            department_code='HR01',
            department_type=self.category1
        )
        self.department2 = Department.objects.create(
            department_name='Finance',
            department_code='FIN01',
            department_type=self.category2
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


class TicketAPITest(BaseTestCase):

    def setUp(self):
        super().setUp()

        # Creating test users
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password',
            first_name='John',
            last_name='Doe'
        )

        # Create necessary related objects for Ticket
        self.ticket_type = TicketType.objects.create(name='Issue')
        self.department = Department.objects.create(department_name='IT')

    def test_create_ticket_success(self):
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T123',
            'ticket_status': 1,
            'ticket_header': 'Sample Ticket',
            'ticket_details': 'Details of the sample ticket',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3,
            'assigned_to': self.user.id,
            'assigned_by': self.user.id,
            'assigned_at': '2024-07-31T12:00:00Z',
            'reassigned_reason': 'Initial assignment',
            'reassigned_by': self.user.id,
            'reassigned_at': '2024-07-31T12:00:00Z',
            'reassigned_status': 1,
            'hold_from': '2024-07-31T12:00:00Z',
            'hold_to': '2024-08-01T12:00:00Z',
            'cancellation_at': '2024-08-01T12:00:00Z',
            'response_within': '2024-08-02T12:00:00Z',
            'response_at': '2024-08-02T12:00:00Z',
            'response_by': self.user.id,
            'response_status': 1,
            'response_breach': 'None',
            'response_breach_time': '2024-08-02T12:00:00Z',
            'resolution_within': '2024-08-03T12:00:00Z',
            'resolution_postponed_time': '2024-08-03T12:00:00Z',
            'resolution_at': '2024-08-03T12:00:00Z',
            'resolution_by': self.user.id,
            'resolution_status': 1,
            'resolution_breach': 'None',
            'resolution_breach_time': '2024-08-03T12:00:00Z',
            'closed_at': '2024-08-04T12:00:00Z',
            'comments': 'No comments',
            'tags': 'tag1, tag2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().ticket_no, 'T123')

    def test_filter_ticket_success(self):
        # First created a ticket
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T123',
            'ticket_status': 1,
            'ticket_header': 'Sample Ticket',
            'ticket_details': 'Details of the sample ticket',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3,
            'assigned_to': self.user.id,
            'assigned_by': self.user.id,
            'assigned_at': '2024-07-31T12:00:00Z',
            'reassigned_reason': 'Initial assignment',
            'reassigned_by': self.user.id,
            'reassigned_at': '2024-07-31T12:00:00Z',
            'reassigned_status': 1,
            'hold_from': '2024-07-31T12:00:00Z',
            'hold_to': '2024-08-01T12:00:00Z',
            'cancellation_at': '2024-08-01T12:00:00Z',
            'response_within': '2024-08-02T12:00:00Z',
            'response_at': '2024-08-02T12:00:00Z',
            'response_by': self.user.id,
            'response_status': 1,
            'response_breach': 'None',
            'response_breach_time': '2024-08-02T12:00:00Z',
            'resolution_within': '2024-08-03T12:00:00Z',
            'resolution_postponed_time': '2024-08-03T12:00:00Z',
            'resolution_at': '2024-08-03T12:00:00Z',
            'resolution_by': self.user.id,
            'resolution_status': 1,
            'resolution_breach': 'None',
            'resolution_breach_time': '2024-08-03T12:00:00Z',
            'closed_at': '2024-08-04T12:00:00Z',
            'comments': 'No comments',
            'tags': 'tag1, tag2'
        }
        self.client.post(url, data, format='json')
        url = reverse('ticket_filter')
        data = {
            'ticket_no': 'T001',
            'order_by': 'ticket_no',
            'order_type': 'asc',
            'page': 1,
            'per_page': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tickets_with_pagination(self):
        # first create a new ticket
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T123',
            'ticket_status': 1,
            'ticket_header': 'Sample Ticket',
            'ticket_details': 'Details of the sample ticket',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3,
            'assigned_to': self.user.id,
            'assigned_by': self.user.id,
            'assigned_at': '2024-07-31T12:00:00Z',
            'reassigned_reason': 'Initial assignment',
            'reassigned_by': self.user.id,
            'reassigned_at': '2024-07-31T12:00:00Z',
            'reassigned_status': 1,
            'hold_from': '2024-07-31T12:00:00Z',
            'hold_to': '2024-08-01T12:00:00Z',
            'cancellation_at': '2024-08-01T12:00:00Z',
            'response_within': '2024-08-02T12:00:00Z',
            'response_at': '2024-08-02T12:00:00Z',
            'response_by': self.user.id,
            'response_status': 1,
            'response_breach': 'None',
            'response_breach_time': '2024-08-02T12:00:00Z',
            'resolution_within': '2024-08-03T12:00:00Z',
            'resolution_postponed_time': '2024-08-03T12:00:00Z',
            'resolution_at': '2024-08-03T12:00:00Z',
            'resolution_by': self.user.id,
            'resolution_status': 1,
            'resolution_breach': 'None',
            'resolution_breach_time': '2024-08-03T12:00:00Z',
            'closed_at': '2024-08-04T12:00:00Z',
            'comments': 'No comments',
            'tags': 'tag1, tag2'
        }
        self.client.post(url, data, format='json')
        url = reverse('ticket_filter')
        data = {
            'per_page': 1,
            'page': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tickets_invalid_page(self):
        # first create a ticket
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T123',
            'ticket_status': 1,
            'ticket_header': 'Sample Ticket',
            'ticket_details': 'Details of the sample ticket',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3,
            'assigned_to': self.user.id,
            'assigned_by': self.user.id,
            'assigned_at': '2024-07-31T12:00:00Z',
            'reassigned_reason': 'Initial assignment',
            'reassigned_by': self.user.id,
            'reassigned_at': '2024-07-31T12:00:00Z',
            'reassigned_status': 1,
            'hold_from': '2024-07-31T12:00:00Z',
            'hold_to': '2024-08-01T12:00:00Z',
            'cancellation_at': '2024-08-01T12:00:00Z',
            'response_within': '2024-08-02T12:00:00Z',
            'response_at': '2024-08-02T12:00:00Z',
            'response_by': self.user.id,
            'response_status': 1,
            'response_breach': 'None',
            'response_breach_time': '2024-08-02T12:00:00Z',
            'resolution_within': '2024-08-03T12:00:00Z',
            'resolution_postponed_time': '2024-08-03T12:00:00Z',
            'resolution_at': '2024-08-03T12:00:00Z',
            'resolution_by': self.user.id,
            'resolution_status': 1,
            'resolution_breach': 'None',
            'resolution_breach_time': '2024-08-03T12:00:00Z',
            'closed_at': '2024-08-04T12:00:00Z',
            'comments': 'No comments',
            'tags': 'tag1, tag2'
        }
        self.client.post(url, data, format='json')
        url = reverse('ticket_filter')
        data = {
            'per_page': 10,
            'page': -1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_ticket(self):
        # first create a ticket
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T123',
            'ticket_status': 1,
            'ticket_header': 'Sample Ticket',
            'ticket_details': 'Details of the sample ticket',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3,
            'assigned_to': self.user.id,
            'assigned_by': self.user.id,
            'assigned_at': '2024-07-31T12:00:00Z',
            'reassigned_reason': 'Initial assignment',
            'reassigned_by': self.user.id,
            'reassigned_at': '2024-07-31T12:00:00Z',
            'reassigned_status': 1,
            'hold_from': '2024-07-31T12:00:00Z',
            'hold_to': '2024-08-01T12:00:00Z',
            'cancellation_at': '2024-08-01T12:00:00Z',
            'response_within': '2024-08-02T12:00:00Z',
            'response_at': '2024-08-02T12:00:00Z',
            'response_by': self.user.id,
            'response_status': 1,
            'response_breach': 'None',
            'response_breach_time': '2024-08-02T12:00:00Z',
            'resolution_within': '2024-08-03T12:00:00Z',
            'resolution_postponed_time': '2024-08-03T12:00:00Z',
            'resolution_at': '2024-08-03T12:00:00Z',
            'resolution_by': self.user.id,
            'resolution_status': 1,
            'resolution_breach': 'None',
            'resolution_breach_time': '2024-08-03T12:00:00Z',
            'closed_at': '2024-08-04T12:00:00Z',
            'comments': 'No comments',
            'tags': 'tag1, tag2'
        }
        ticket1 = self.client.post(url, data, format='json')
        url = reverse('ticket_detail', kwargs={'pk': ticket1.json()['id']})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ticket_no'], 'T123')

    def test_update_ticket(self):
        # first create a ticket
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T123',
            'ticket_status': 1,
            'ticket_header': 'Sample Ticket',
            'ticket_details': 'Details of the sample ticket',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3,
            'assigned_to': self.user.id,
            'assigned_by': self.user.id,
            'assigned_at': '2024-07-31T12:00:00Z',
            'reassigned_reason': 'Initial assignment',
            'reassigned_by': self.user.id,
            'reassigned_at': '2024-07-31T12:00:00Z',
            'reassigned_status': 1,
            'hold_from': '2024-07-31T12:00:00Z',
            'hold_to': '2024-08-01T12:00:00Z',
            'cancellation_at': '2024-08-01T12:00:00Z',
            'response_within': '2024-08-02T12:00:00Z',
            'response_at': '2024-08-02T12:00:00Z',
            'response_by': self.user.id,
            'response_status': 1,
            'response_breach': 'None',
            'response_breach_time': '2024-08-02T12:00:00Z',
            'resolution_within': '2024-08-03T12:00:00Z',
            'resolution_postponed_time': '2024-08-03T12:00:00Z',
            'resolution_at': '2024-08-03T12:00:00Z',
            'resolution_by': self.user.id,
            'resolution_status': 1,
            'resolution_breach': 'None',
            'resolution_breach_time': '2024-08-03T12:00:00Z',
            'closed_at': '2024-08-04T12:00:00Z',
            'comments': 'No comments',
            'tags': 'tag1, tag2'
        }
        ticket1 = self.client.post(url, data, format='json')
        url = reverse('ticket_detail', kwargs={'pk': ticket1.json()['id']})
        data = {
            'ticket_no': 'T002',
            'ticket_status': 2,
            'ticket_header': 'Updated Ticket Header',
            'ticket_details': 'Updated details of the ticket',
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 2,
            'ticket_priority': 3,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('ticket_detail', kwargs={'pk': ticket1.json()['id']})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ticket.objects.filter(id=ticket1.json()['id']).exists())

    def test_create_ticket_unauthorized(self):
        self.client.credentials()  # Remove token
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T124',
            'ticket_status': 1,
            'ticket_header': 'Unauthorized Ticket',
            'ticket_details': 'This ticket should fail',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_ticket_invalid_data(self):
        url = reverse('ticket_create')
        data = {
            'ticket_no': '',  # Invalid data
            'ticket_status': 1,
            'ticket_header': 'Invalid Ticket',
            'ticket_details': 'This ticket should fail',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TicketBehalfCreateAPITest(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.ticket_type = TicketType.objects.create(name='Issue')
        self.department = Department.objects.create(department_name='IT')
        # create a new ticket
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T123',
            'ticket_status': 1,
            'ticket_header': 'Sample Ticket',
            'ticket_details': 'Details of the sample ticket',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3,
            'assigned_to': self.user.id,
            'assigned_by': self.user.id,
            'assigned_at': '2024-07-31T12:00:00Z',
            'reassigned_reason': 'Initial assignment',
            'reassigned_by': self.user.id,
            'reassigned_at': '2024-07-31T12:00:00Z',
            'reassigned_status': 1,
            'hold_from': '2024-07-31T12:00:00Z',
            'hold_to': '2024-08-01T12:00:00Z',
            'cancellation_at': '2024-08-01T12:00:00Z',
            'response_within': '2024-08-02T12:00:00Z',
            'response_at': '2024-08-02T12:00:00Z',
            'response_by': self.user.id,
            'response_status': 1,
            'response_breach': 'None',
            'response_breach_time': '2024-08-02T12:00:00Z',
            'resolution_within': '2024-08-03T12:00:00Z',
            'resolution_postponed_time': '2024-08-03T12:00:00Z',
            'resolution_at': '2024-08-03T12:00:00Z',
            'resolution_by': self.user.id,
            'resolution_status': 1,
            'resolution_breach': 'None',
            'resolution_breach_time': '2024-08-03T12:00:00Z',
            'closed_at': '2024-08-04T12:00:00Z',
            'comments': 'No comments',
            'tags': 'tag1, tag2'
        }
        self.ticket = self.client.post(url, data, format='json')

    def test_create_ticket_behalf(self):
        url = reverse('ticket_behalf_create')
        data = {
            'ticket_id': self.ticket.json()['id'],
            'behalf_email': 'behalf@example.com',
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TicketBehalf.objects.count(), 1)
        self.assertEqual(TicketBehalf.objects.get().behalf_email, 'behalf@example.com')

    def test_create_ticket_behalf_invalid(self):
        url = reverse('ticket_behalf_create')
        data = {
            'ticket_id': self.ticket.json()['id'],
            'behalf_email': '',  # Invalid email
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TicketBehalf.objects.count(), 0)

    def test_create_ticket_behalf_no_ticket(self):
        url = reverse('ticket_behalf_create')
        data = {
            'ticket_id': 9999,  # Non-existent ticket ID
            'behalf_email': 'behalf@example.com',
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TicketBehalf.objects.count(), 0)


class TicketRevisionCreateAPITest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.ticket_type = TicketType.objects.create(name='Issue')
        self.department = Department.objects.create(department_name='IT')
        # Create test ticket
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T123',
            'ticket_status': 1,
            'ticket_header': 'Sample Ticket',
            'ticket_details': 'Details of the sample ticket',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3,
            'assigned_to': self.user.id,
            'assigned_by': self.user.id,
            'assigned_at': '2024-07-31T12:00:00Z',
            'reassigned_reason': 'Initial assignment',
            'reassigned_by': self.user.id,
            'reassigned_at': '2024-07-31T12:00:00Z',
            'reassigned_status': 1,
            'hold_from': '2024-07-31T12:00:00Z',
            'hold_to': '2024-08-01T12:00:00Z',
            'cancellation_at': '2024-08-01T12:00:00Z',
            'response_within': '2024-08-02T12:00:00Z',
            'response_at': '2024-08-02T12:00:00Z',
            'response_by': self.user.id,
            'response_status': 1,
            'response_breach': 'None',
            'response_breach_time': '2024-08-02T12:00:00Z',
            'resolution_within': '2024-08-03T12:00:00Z',
            'resolution_postponed_time': '2024-08-03T12:00:00Z',
            'resolution_at': '2024-08-03T12:00:00Z',
            'resolution_by': self.user.id,
            'resolution_status': 1,
            'resolution_breach': 'None',
            'resolution_breach_time': '2024-08-03T12:00:00Z',
            'closed_at': '2024-08-04T12:00:00Z',
            'comments': 'No comments',
            'tags': 'tag1, tag2'
        }
        self.ticket = self.client.post(url, data, format='json')

    def test_create_ticket_revision(self):
        url = reverse('ticket_revision_create')
        data = {
            'ticket_id': self.ticket.json()['id'],
            'revision_status': 1,
            'pti': 100,
            'action_taken': '2024-07-31T12:00:00Z',
            'before_revision': 'Initial state',
            'after_revision': 'Updated state',
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TicketRevision.objects.count(), 1)
        self.assertEqual(TicketRevision.objects.get().before_revision, 'Initial state')

    def test_create_ticket_revision_missing_field(self):
        url = reverse('ticket_revision_create')
        data = {
            'ticket_id': self.ticket.json()['id'],
            'revision_status': 1,
            'pti': 100,
            # 'action_taken' is missing
            'before_revision': 'Initial state',
            'after_revision': 'Updated state',
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('action_taken', response.data['error'])

    def test_create_ticket_revision_invalid_ticket(self):
        url = reverse('ticket_revision_create')
        data = {
            'ticket_id': 999,  # Non-existent ticket ID
            'revision_status': 1,
            'pti': 100,
            'action_taken': '2024-07-31T12:00:00Z',
            'before_revision': 'Initial state',
            'after_revision': 'Updated state',
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ticket_id', response.data['error'])


class TicketFollowerCreateAPITest(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.other_user = User.objects.create_user(
            email='otheruser@example.com',
            password='password',
            first_name='Jane',
            last_name='Doe'
        )

        self.ticket_type = TicketType.objects.create(name='Issue')
        self.department = Department.objects.create(department_name='IT')
        # create a new ticket
        url = reverse('ticket_create')
        data = {
            'ticket_no': 'T123',
            'ticket_status': 1,
            'ticket_header': 'Sample Ticket',
            'ticket_details': 'Details of the sample ticket',
            'on_behalf': 1,
            'ticket_category': 2,
            'ticket_type': self.ticket_type.id,
            'department_id': self.department.id,
            'project_id': 1,
            'ticket_priority': 3,
            'assigned_to': self.user.id,
            'assigned_by': self.user.id,
            'assigned_at': '2024-07-31T12:00:00Z',
            'reassigned_reason': 'Initial assignment',
            'reassigned_by': self.user.id,
            'reassigned_at': '2024-07-31T12:00:00Z',
            'reassigned_status': 1,
            'hold_from': '2024-07-31T12:00:00Z',
            'hold_to': '2024-08-01T12:00:00Z',
            'cancellation_at': '2024-08-01T12:00:00Z',
            'response_within': '2024-08-02T12:00:00Z',
            'response_at': '2024-08-02T12:00:00Z',
            'response_by': self.user.id,
            'response_status': 1,
            'response_breach': 'None',
            'response_breach_time': '2024-08-02T12:00:00Z',
            'resolution_within': '2024-08-03T12:00:00Z',
            'resolution_postponed_time': '2024-08-03T12:00:00Z',
            'resolution_at': '2024-08-03T12:00:00Z',
            'resolution_by': self.user.id,
            'resolution_status': 1,
            'resolution_breach': 'None',
            'resolution_breach_time': '2024-08-03T12:00:00Z',
            'closed_at': '2024-08-04T12:00:00Z',
            'comments': 'No comments',
            'tags': 'tag1, tag2'
        }
        self.ticket = self.client.post(url, data, format='json')

    def test_create_ticket_follower(self):
        url = reverse('ticket_follower_create')
        data = {
            'ticket_id': self.ticket.json()['id'],
            'follower_id': self.user.id,
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            TicketFollower.objects.filter(ticket_id=self.ticket.json()['id'], follower_id=self.user.id).exists())

    def test_create_ticket_follower_missing_required_field(self):
        url = reverse('ticket_follower_create')
        data = {

        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_ticket_follower_invalid_data(self):
        url = reverse('ticket_follower_create')
        data = {
            'ticket_id': self.ticket.json()['id'],
            'follower_id': 9999,  # Invalid user ID
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('follower_id', response.data['error'])

    def test_filter_ticket_follower(self):
        # first create ticket follower
        url = reverse('ticket_follower_create')
        data = {
            'ticket_id': self.ticket.json()['id'],
            'follower_id': self.user.id,
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the user
        follower = self.client.post(url, data, format='json')

        url = reverse('ticket_follower_filter')
        data = {
            'ticket_id': self.ticket.json()['id'],
            'follower_id': follower.json()['id'],
            'order_by': 'created_at',
            'order_type': 'asc',
            'page': 1,
            'per_page': 10
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

        data = {
            'ticket_id': self.ticket.json()['id'],
            'follower_id': self.user.id,
            'page': -1,  # Invalid page number
            'per_page': 10
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('page and page size should be positive integer', response.data['message'])

    def test_filter_ticket_follower_no_results(self):
        url = reverse('ticket_follower_filter')
        data = {
            'ticket_id': 9999,  # Non-existent ticket ID
            'page': 1,
            'per_page': 10
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_filter_ticket_follower_ordering(self):
        url = reverse('ticket_follower_filter')
        data = {
            'order_by': 'created_at',
            'order_type': 'desc',
            'page': 1,
            'per_page': 10
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_ticket_follower_invalid_ordering(self):
        url = reverse('ticket_follower_filter')
        data = {
            'order_by': 'invalid_field',  # Invalid ordering field
            'order_type': 'asc',
            'page': 1,
            'per_page': 10
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

