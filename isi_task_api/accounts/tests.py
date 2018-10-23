from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from accounts.auth.backends import AccountAuthBackend
from accounts.views import CustomUserViewSet

client = Client()

class CustomUserTest(TestCase):

    def setUp(self):
        
        user_data = {}
        
        user_data['username'] = 'test_admin'
        user_data['first_name'] = 'admin_one'
        user_data['last_name'] = 'admin_two'
        user_data['email'] = 'admin@example.com'
        user_data['password'] = 'admin@1234'
        user_data['user_type'] = 'admin'
        self.test_admin = CustomUser.objects.create_superuser(**user_data)
        
        user_data['username'] = 'test_driver'
        user_data['first_name'] = 'driver_one'
        user_data['last_name'] = 'driver_two'
        user_data['email'] = 'driver@example.com'
        user_data['password'] = 'admin@1234'
        user_data['user_type'] = 'driver'
        self.test_driver = CustomUser.objects.create_superuser(**user_data)
        
        
    def test_model_auth_user(self):
        test_admin = CustomUser.objects.get(username='test_admin')
        test_driver = CustomUser.objects.get(username='test_driver')
        
        self.assertNotEqual(test_admin, None, 'user is None')
        self.assertNotEqual(test_driver, None, 'user is None')
        
        auth_test_admin = AccountAuthBackend().authenticate(None, 
                                            test_admin.username, 'admin@1234')
        auth_test_driver = AccountAuthBackend().authenticate(None, 
                                                test_driver.username, 'admin@1234')
        
        self.assertEqual(test_admin, auth_test_admin, 'user is not equal')
        self.assertEqual(test_driver, auth_test_driver, 'user is not equal')
        
    def test_model_auth_token_user(self):
        
        url = '/api/login/'
        data = {'username':'test_admin', 'password':'admin@1234'}
        response = client.post(url, data, content_type='application/json')
        
        self.assertTrue(response.data.get('token', None), 'no token')
        self.assertEqual(response.wsgi_request.path, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_view_all_users(self):
        
        url = reverse('customuser-list')
        
        response = client.get(url)
        
        view = CustomUserViewSet.as_view({'get':'list'})(response.wsgi_request)
        
        self.assertEqual(response.data, view.data)
        self.assertEqual(response.wsgi_request.path, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_get_view_single_user(self):   
        
        #first user
        url = reverse('customuser-detail', kwargs={'pk': self.test_admin.pk})
        response = client.get(url)
        
        view = CustomUserViewSet.as_view({'get':'retrieve'})(response.wsgi_request, 
                                                             pk=self.test_admin.pk)
        
        self.assertEqual(response.data, view.data)
        self.assertEqual(response.wsgi_request.path, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #second user
        url = reverse('customuser-detail', kwargs={'pk': self.test_driver.pk})
        response = client.get(url)
        
        view = CustomUserViewSet.as_view({'get':'retrieve'})(response.wsgi_request, 
                                                             pk=self.test_driver.pk)
        
        self.assertEqual(response.data, view.data)
        self.assertEqual(response.wsgi_request.path, url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
        
        
        
        
        
