from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()
class TestUsers(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'jojo', 
            'email': 'jojo@email.com', 
            'password': 'jojopassword'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)
        self.user2_data = {
            'username': 'hana',
            'email': 'hana@gmail.com',
            'password': 'hanapassword'
        }

    def test_create_user(self):
        url = reverse('users-list')
        response = self.client.post(url, self.user2_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.get(username='jojo')
        self.assertEqual(user.email, 'jojo@email.com')

    def test_create_user_invalid_data(self):
        url = reverse('users-list')
        bad_data = self.user2_data.copy()
        bad_data['email'] = 'invalid'
        response = self.client.post(url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_duplicate_username(self):
        url = reverse('users-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_get_user(self):
        user = self.user
        url = reverse('users-detail', args=[user.id])
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
        user = self.user
        url = reverse('users-detail', args=[user.id])
        data = {'username': 'nina', 'email': 'nina@example.com'}
        response = self.client.patch(url, data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, 'nina')
        self.assertEqual(user.email, 'nina@example.com')

    def test_delete_user(self):
        user = self.user
        self.client.force_authenticate(user=user)
        url = reverse('users-detail', args=[user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user.id).exists())

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