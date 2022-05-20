# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase


# Create your tests here.


class ReportTests(APITestCase):
    def test_server_check(self):
        """
        Ensure server is ready to work.
        """
        # given
        url = reverse('serverCheck')
        # when
        response = self.client.get(url, format='application/json')
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Server is ready for work.')
