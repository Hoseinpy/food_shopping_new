from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class SingupTestCase(APITestCase):

    def test_singup(self):
        data = {'username': 'amir', 'password': '11', 'confirm_password': '11'}

        response = self.client.post(reverse('singup-api'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)