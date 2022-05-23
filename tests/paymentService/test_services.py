from datetime import datetime, timezone, date
import iso8601

import pytest
from assertpy import assert_that


from transactions.services import PaymentInfo, create_payment_info, pay_by_link_payment_info, dp_payment_info, \
    card_payment_info, iso8601_date_parser


@pytest.mark.django_db
class TestTransactionsServices:

    @pytest.fixture(autouse=True)
    def prepare_get_payment_info(self):
        self.process_transaction = create_payment_info

    # case1
    processing_strategy_1 = pay_by_link_payment_info
    expected_1 = 'pay_by_link'
    case_1 = processing_strategy_1, expected_1

    # case2
    processing_strategy_2 = dp_payment_info
    expected_2 = 'dp'
    case_2 = processing_strategy_2, expected_2

    # case3
    processing_strategy_3 = card_payment_info
    expected_3 = 'card'
    case_3 = processing_strategy_3, expected_3

    @pytest.mark.parametrize("processing_strategy, expected", [case_1, case_2, case_3])
    def test_process_transaction_type(self, processing_strategy, expected):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # given
        data = {}

        # when
        result = self.process_transaction(processing_strategy, data).type

        # then
        assert_that(result).is_equal_to(expected)

    # case1
    processing_strategy_1 = pay_by_link_payment_info
    data_1 = {'bank': 'mbank'}
    expected_1 = 'mbank'
    case_1 = processing_strategy_1, data_1, expected_1

    # case2
    processing_strategy_2 = dp_payment_info
    data_2 = {'iban': 'DE91100000000123456789'}
    expected_2 = 'DE91100000000123456789'
    case_2 = processing_strategy_2, data_2, expected_2

    @pytest.mark.parametrize("processing_strategy, data, expected", [case_1, case_2])
    def test_process_transaction_payment_mean(self, processing_strategy, data, expected):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # when
        result = self.process_transaction(processing_strategy, data).payment_mean

        # then
        assert_that(result).is_equal_to(expected)

    def test_process_transaction_amount(self):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # given
        processing_strategy = dp_payment_info
        data = {"amount": 100}

        # when
        result = self.process_transaction(processing_strategy, data).amount

        # then
        assert_that(result).is_equal_to(100)

    def test_process_transaction_currency(self):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # given
        processing_strategy = dp_payment_info
        data = {"currency": "USD"}

        # when
        result = self.process_transaction(processing_strategy, data).currency

        # then
        assert_that(result).is_equal_to("USD")

    def test_process_transaction_description(self):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # given
        processing_strategy = dp_payment_info
        data = {"description": "FastFood"}

        # when
        result = self.process_transaction(processing_strategy, data).description

        # then
        assert_that(result).is_equal_to("FastFood")

    @pytest.fixture(autouse=True)
    def prepare_get_payment_info(self):
        self.iso8601_date_parser = iso8601_date_parser

    def test_date_parser(self):
        # given
        date_input = '2007-01-25T12:00:00Z'

        # when
        expected = datetime(2007, 1, 25, 12, 0, tzinfo=timezone.utc)
        print(f'expected: {expected}')
        result = iso8601_date_parser(date_input)

        # then
        assert_that(result).is_equal_to(expected)
