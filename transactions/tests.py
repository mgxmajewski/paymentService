import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Request via API specific tests.


class ReportTests(APITestCase):
    RequestStubShort = {
        "pay_by_link": [
            {
                "created_at": "2021-05-13T01:01:43-08:00",
                "currency": "EUR",
                "amount": 3000,
                "description": "Gym membership",
                "bank": "mbank"
            }
        ]
    }

    RequestStub = {
        "pay_by_link": [
            {
                "created_at": "2021-05-13T01:01:43-08:00",
                "currency": "EUR",
                "amount": 3000,
                "description": "Gym membership",
                "bank": "mbank"
            }
        ],
        "dp": [
            {
                "created_at": "2021-05-14T08:27:09Z",
                "currency": "USD",
                "amount": 599,
                "description": "FastFood",
                "iban": "DE91100000000123456789"
            }
        ],
        "card": [
            {
                "created_at": "2021-05-13T09:00:05+02:00",
                "currency": "PLN",
                "amount": 2450,
                "description": "REF123457",
                "cardholder_name": "John",
                "cardholder_surname": "Doe",
                "card_number": "2222222222222222"
            },
            {
                "created_at": "2021-05-14T18:32:26Z",
                "currency": "GBP",
                "amount": 1000,
                "description": "REF123456",
                "cardholder_name": "John",
                "cardholder_surname": "Doe",
                "card_number": "1111111111111111"
            }
        ]
    }

    ExpectedResponseShort = [
        {
            'date': '2021-05-13T09:01:43Z',
            'type': 'pay_by_link',
            'payment_mean': 'mbank',
            'description': 'Gym membership',
            'currency': 'EUR',
            'amount': 3000,
            'amount_in_pln': 13494
        }
    ]

    ExpectedResponse = [
        {
            'date': '2021-05-13T07:00:05Z',
            'type': 'card',
            'payment_mean': 'John Doe 2222********2222',
            'description': 'REF123457',
            'currency': 'PLN',
            'amount': 2450,
            'amount_in_pln': 2450
        },
        {
            'date': '2021-05-13T09:01:43Z',
            'type': 'pay_by_link',
            'payment_mean': 'mbank',
            'description': 'Gym membership',
            'currency': 'EUR',
            'amount': 3000,
            'amount_in_pln': 13494
        },
        {
            'date': '2021-05-14T08:27:09Z',
            'type': 'dp',
            'payment_mean': 'DE91100000000123456789',
            'description': 'FastFood',
            'currency': 'USD',
            'amount': 599,
            'amount_in_pln': 2219
        },
        {
            'date': '2021-05-14T18:32:26Z',
            'type': 'card',
            'payment_mean': 'John Doe 1111********1111',
            'description': 'REF123456',
            'currency': 'GBP',
            'amount': 1000,
            'amount_in_pln': 5208
        }
    ]

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

    def test_short_json_report(self):
        """
        Check if report/ returns correct JSON.
        """

        # given
        url = reverse('report')

        # when
        data = json.dumps(self.RequestStubShort)
        result = self.client.post(url, data, content_type='application/json').data

        # then
        print(result)
        expected = self.ExpectedResponseShort
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, self.ExpectedResponseShort)

    def test_long_json_report(self):
        """
        Check if report/ returns correct JSON.
        """

        # given
        url = reverse('report')

        # when
        data = json.dumps(self.RequestStub)
        result = self.client.post(url, data, content_type='application/json').data

        # then
        expected = self.ExpectedResponseShort
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, self.ExpectedResponse)
