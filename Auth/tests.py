from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.test import Client

# Create your tests here.
User = get_user_model()
class TestUsers(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'jojo', 
            'email': 'jojo@email.com', 
            'password': 'jojopassword'
        }

    def test_create_user(self):
        url = reverse('users-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='jojo')
        self.assertEqual(user.email, 'jojo@email.com')

    def test_create_user_invalid_data(self):
        url = reverse('users-list')
        bad_data = self.user_data.copy()
        bad_data['email'] = 'invalid'
        response = self.client.post(url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user_duplicate_username(self):
        url = reverse('users-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_get_user(self):
        # need to fix AttributeError: 'TestUsers' object has no attribute 'user'
        # create object to fix this
        url = reverse('users-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'jojo')
        self.assertEqual(response.data['email'], 'jojo@email.com')

        User.objects.create_user('zara', 'zara@example.com', 'password')
        User.objects.create_user('jane', 'jane@example.com', 'password')
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_update_user(self):
        user = User.objects.create_user(self.user_data)
        url = reverse('users-detail', args=[user.id])
        data = {'username': 'nina', 'email': 'nina@example.com'}
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, 'nina')
        self.assertEqual(user.email, 'nina@example.com')

    def test_delete_user(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        url = reverse('users-detail', args=[user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #Error, need to use asserttrue or change value
        self.assertEqual(User.objects.filter(id=user.id).exists())

    def test_delete_nonexistent_user(self):
        url = reverse('users-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_user_without_password_raises_error(self):
        data = self.user_data.copy()
        data['password'] = ''
        url = reverse('users-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_email_raises_error(self):
        data = self.user_data.copy()
        data['email'] = ''
        url = reverse('users-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_username_raises_error(self):
        data = self.user_data.copy()
        data['username'] = ''
        url = reverse('users-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)