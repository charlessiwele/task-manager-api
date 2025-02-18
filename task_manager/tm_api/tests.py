from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from tm_api.services.status_generator import generate_statuses
from rest_framework import status
from tm_api.models import Status

api_client = APIClient()

# Create your tests here.
class ProjectTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Run once to set up non-modified data for all class methods.
        test_admin_username = 'test_admin_username'
        test_admin_email = 'test_admin_email@test_admin_email.test_admin_email'
        test_admin_password = 'test_admin_password'
        User.objects.create_superuser(test_admin_username, test_admin_email, test_admin_password)

        test_staff_username = 'test_staff_username'
        test_staff_email = 'test_staff_email@test_staff_email.test_staff_email'
        test_staff_password = 'test_staff_password'
        test_staff_user = User.objects.create_superuser(test_staff_username, test_staff_email, test_staff_password)
        test_staff_user.is_superuser = False
        test_staff_user.save()


        test_non_staff_username = 'test_non_staff_username'
        test_non_staff_email = 'test_non_staff_email@test_non_staff_email.test_non_staff_email'
        test_non_staff_password = 'test_non_staff_password'
        test_non_staff_user = User.objects.create_superuser(test_non_staff_username, test_non_staff_email, test_non_staff_password)
        test_non_staff_user.is_superuser = False
        test_non_staff_user.is_staff = False
        test_non_staff_user.save()

        statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED']
        generate_statuses(statuses)

    def setUp(self):
        # Setup run before every test method.
        pass


    def tearDown(self):
        # Clean up run after every test method.
        pass


        def test_register(self):
            """
            Test the registration endpoint.
            """
            # Send a POST request to the /register/ endpoint with test data
            result = api_client.post(
                '/register/', 
                {
                    'username': 'test_username',
                    'password': 'test_password',
                }
            )
            
            # Assert that the response status code is 200 OK
            self.assertEqual(result.status_code, status.HTTP_200_OK)
            
            # Assert that the response contains the correct username
            self.assertEqual(result.data.get('username'), 'test_username')
            
            # Assert that the response contains the correct password
            self.assertEqual(result.data.get('password'), 'test_password')


    def test_login_token(self):
        """
        Test the login token endpoint.
        """
        
        result = api_client.post(
            '/login_token/', 
            {
                'username': 'test_admin_username',
                'password': 'test_admin_password',
            }
        )
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertTrue(result.data.get('refresh'))
        self.assertTrue(result.data.get('access'))


    def test_refresh_login_token(self):
        """
        Test the login token refresh endpoint.
        """
        result = api_client.post(
            '/login_token/', 
            {
                'username': 'test_admin_username',
                'password': 'test_admin_password',
            }
        )

        # Confirm an initial access token is generated
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        original_access_token = result.data.get('access')
        original_refresh_token = result.data.get('refresh')
        self.assertTrue(original_access_token)
        self.assertTrue(original_refresh_token)

        refresh_result = api_client.post(
            '/refresh_login_token/', 
            {
                'refresh': original_refresh_token,

            }
        )
        # Confirm a new access token is generated
        new_access_token = refresh_result.data.get('access')
        self.assertNotEqual(new_access_token, original_access_token)

    def test_login_auth(self):
        api_client = APIClient()

        # Login with a session
        login_auth_result = api_client.post(
            path="/login_auth/",
            data={
                'username': 'test_admin_username',
                'password': 'test_admin_password',
            }
        )

        self.assertEqual(login_auth_result.status_code, status.HTTP_200_OK)
        self.assertTrue(api_client.session.session_key)

        # Add a task as a logged in user
        tasks_result = api_client.post(
            '/tasks/', 
            {
                'title': 'title1', 
                'description': 'description1', 
            },
        )
        self.assertEqual(tasks_result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tasks_result.data.get('title'), 'title1')
        self.assertEqual(tasks_result.data.get('description'), 'description1')

    def test_auth_logout(self):
        api_client = APIClient()

        login_auth_result = None
        login_auth_result = api_client.post(
            path="/login_auth/",
            data={
                'username': 'test_admin_username',
                'password': 'test_admin_password',
            }
        )
        self.assertEqual(login_auth_result.status_code, status.HTTP_200_OK)
        logged_in_task_create_result = None
        logged_in_task_create_result = login_auth_result.client.post(
            '/tasks/', 
            {
                'title': 'title1', 
                'description': 'description1', 
            },
        )

        # Logout of session
        self.assertEqual(logged_in_task_create_result.status_code, status.HTTP_201_CREATED)
        logout_result = logged_in_task_create_result.client.get(
            path="/logout_auth/",
        )
        self.assertEqual(logout_result.status_code, status.HTTP_200_OK)
        logged_out_create_task_result = None
        # Attempt to add a task when logged out
        logged_out_create_task_result = api_client.post(
            '/tasks/', 
            {
                'title': 'title1', 
                'description': 'description1', 
            },
        )
        self.assertEqual(logged_out_create_task_result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tasks(self):
        api_client = APIClient()
        # Attempt to add a task when logged out
        before_log_in_create_task_result = api_client.post(
            '/tasks/', 
            {
                'title': 'title1', 
                'description': 'description1', 
            },
        )
        self.assertEqual(before_log_in_create_task_result.status_code, status.HTTP_401_UNAUTHORIZED)

        # Get login token
        login_token_result = before_log_in_create_task_result.client.post(
            '/login_token/', 
            {
                'username': 'test_admin_username',
                'password': 'test_admin_password',
            }
        )
        self.assertEqual(login_token_result.status_code, status.HTTP_200_OK)
        # Attempt to add a task when logged in
        after_log_in_create_task_result = login_token_result.client.post(
            '/tasks/', 
            data={
                'title': 'title1', 
                'description': 'description1', 
            },
            headers={
                "Authorization": "Bearer " + login_token_result.data.get('access')
            }
        )
        self.assertEqual(after_log_in_create_task_result.status_code, status.HTTP_201_CREATED)

        # Blacklist refresh token
        logout_token_result = after_log_in_create_task_result.client.post(
            '/logout_token/', 
            {
                'refresh': login_token_result.data.get('refresh'),
            }
        )
        # Attempt token refresh after blacklisting
        refresh_result = logout_token_result.client.post(
            '/refresh_login_token/', 
            {
                'refresh': login_token_result.data.get('refresh'),
            }
        )
        self.assertEqual(refresh_result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(refresh_result.data, "Token is blacklisted")

    def test_status(self):
        PENDING ='PENDING'
        IN_PROGRESS ='IN_PROGRESS'
        COMPLETED ='COMPLETED'
        generated_pending_status, PENDING_CREATED = Status.objects.get_or_create(name=PENDING)
        generated_in_progress_status, IN_PROGRESS_CREATED = Status.objects.get_or_create(name=IN_PROGRESS)
        generated_completed_status, COMPLETED_CREATED = Status.objects.get_or_create(name=COMPLETED)

        self.assertFalse(PENDING_CREATED)
        self.assertFalse(IN_PROGRESS_CREATED)
        self.assertFalse(COMPLETED_CREATED)
