# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json


def validate_json(json_data):
    try:
        json.loads(json_data)
    except ValueError as err:
        return False
    return True

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

    def test_simplified_pay_by_link_report(self):
        """
        Ensure server is ready to work.
        """
        # given
        url = reverse('report')
        data = {
            "pay_by_link": [
                {
                    "created_at": "2021-05-13T01:01:43-08:00",
                    "currency": "EUR",
                    "amount": "3000",
                    "description": "Gym membership",
                    "bank": "mbank"
                }
            ]
        }

        # when
        response = self.client.post(url, data, format='application/json')

        # then
        response_first_obj = response.data[0]
        is_valid_jason = validate_json(response_first_obj)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(is_valid_jason)
