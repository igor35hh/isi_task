from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from dialogs.views import ThreadViewSet

client = Client()


class DialogsTest(TestCase):

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

    def test_post_token_thread(self):

        # first thread
        url = reverse('thread-list')
        secure = 'Token {}'.format(self.test_admin.token())

        data = {'participants': [self.test_admin.pk, self.test_driver.pk]}
        response = client.post(url, data, content_type='application/json',
                               HTTP_AUTHORIZATION=secure)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # second thread
        data = {'participants': [self.test_driver.pk]}
        response = client.post(url, data, content_type='application/json',
                               HTTP_AUTHORIZATION=secure)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check user's threads
        url = reverse('customuser-detail', kwargs={'pk': self.test_admin.pk})
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('threads')), 1)

        # third thread must be deleted
        url = reverse('thread-list')
        data = {'participants': [self.test_admin.pk]}
        response = client.post(url, data, content_type='application/json',
                               HTTP_AUTHORIZATION=secure)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check we have only two threads
        url = reverse('thread-list')
        response = client.get(url)
        view = ThreadViewSet.as_view(
            {'get': 'list'})(response.wsgi_request)
        self.assertEqual(response.data, view.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # check update thread and delete
        url = reverse('thread-detail', kwargs={'pk': 1})
        data = {'participants': [self.test_admin.pk]}
        response = client.put(url, data, content_type='application/json',
                              HTTP_AUTHORIZATION=secure)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check we have only one after update threads
        url = reverse('thread-list')
        response = client.get(url)
        view = ThreadViewSet.as_view(
            {'get': 'list'})(response.wsgi_request)
        self.assertEqual(response.data, view.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_token_message(self):

        # first thread
        url = reverse('thread-list')
        secure = 'Token {}'.format(self.test_admin.token())

        data = {'participants': [self.test_admin.pk, self.test_driver.pk]}
        response = client.post(url, data, content_type='application/json',
                               HTTP_AUTHORIZATION=secure)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # first message
        url = reverse('message-list')
        data = {'text': 'test message one', 'sender':
                self.test_admin.pk, 'thread': 1}
        response = client.post(url, data, content_type='application/json',
                               HTTP_AUTHORIZATION=secure)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # second message
        url = reverse('message-list')
        data = {'text': 'test message two', 'sender':
                self.test_admin.pk, 'thread': 1}
        response = client.post(url, data, content_type='application/json',
                               HTTP_AUTHORIZATION=secure)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # thread's messages
        url = reverse('thread-detail', kwargs={'pk': 1})
        response = client.get(url)
        view = ThreadViewSet.as_view(
            {'get': 'retrieve'})(response.wsgi_request, pk=1)
        self.assertEqual(response.data, view.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('messages')), 2)
