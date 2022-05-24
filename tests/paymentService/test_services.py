from datetime import datetime, timezone, timedelta

import pytest
from assertpy import assert_that

from transactions.services import create_payment_info, pay_by_link_payment_info, dp_payment_info, \
    card_payment_info, iso8601_date_parser, convert_date_to_utc, get_date_normalized_str, get_valid_utc_iso8061_date, \
    mask_card_nr, get_nbp_exchange_rate, calculate_amount_in_pln, prepare_nbp_date, PayByLink, DirectPayment, Card, \
    PaymentInfo, process_request, InvalidDateString


@pytest.mark.django_db
class TestTransactionsServices:
    # Transactions stubs
    pay_by_link_transaction_stub_data = {
        'created_at': '2021-05-13T01:01:43-08:00',
        'currency': 'EUR',
        'amount': 3000,
        'description': 'Gym membership',
        'bank': 'mbank'
    }
    PayByLinkTransactionStub = PayByLink(**pay_by_link_transaction_stub_data)

    dp_transaction_stub_data = {
        'created_at': '2021-05-14T08:27:09Z',
        'currency': 'USD',
        'amount': 599,
        'description': 'FastFood',
        'iban': 'DE91100000000123456789',
    }
    DirectPaymentTransactionStub = DirectPayment(**dp_transaction_stub_data)

    card_transaction_stub_data = {
        'created_at': '2021-05-13T09:00:05+02:00',
        'currency': 'PLN',
        'amount': 2450,
        'description': 'REF123457',
        'cardholder_name': 'John',
        'cardholder_surname': 'Doe',
        'card_number': '1234222222226789'
    }
    CardTransactionStub = Card(**card_transaction_stub_data)

    # Transactions stubs
    pay_by_link_payment_info_stub_data = {
        'date': '2021-05-13T09:01:43Z',
        'type': 'pay_by_link',
        'payment_mean': 'mbank',
        'description': 'Gym membership',
        'currency': 'EUR',
        'amount': 3000,
        'amount_in_pln': 13494
    }
    PayByLinkInfoStub = PaymentInfo(**pay_by_link_payment_info_stub_data)

    card_payment_info_stub_data = {
        'date': '2021-05-13T07:00:05Z',
        'type': 'card',
        'payment_mean': 'John Doe 1234********6789',
        'description': 'REF123457',
        'currency': 'PLN',
        'amount': 2450,
        'amount_in_pln': 2450
    }
    CardPaymentInfoStub = PaymentInfo(**card_payment_info_stub_data)

    # Requests stubs
    RequestStub_1 = {
        'pay_by_link': [
            pay_by_link_transaction_stub_data
        ],
    }

    RequestStub_2 = {
        'pay_by_link': [
            pay_by_link_transaction_stub_data
        ],
        'card': [
            card_transaction_stub_data
        ]
    }

    @pytest.fixture(autouse=True)
    def prepare_get_payment_info(self):
        self.create_payment_info = create_payment_info

    # case1
    data_1 = PayByLinkTransactionStub
    processing_strategy_1 = pay_by_link_payment_info
    expected_1 = 'pay_by_link'
    case_1 = processing_strategy_1, data_1, expected_1

    # case2
    data_2 = DirectPaymentTransactionStub
    processing_strategy_2 = dp_payment_info
    expected_2 = 'dp'
    case_2 = processing_strategy_2, data_2, expected_2

    # case3
    data_3 = CardTransactionStub
    processing_strategy_3 = card_payment_info
    expected_3 = 'card'
    case_3 = processing_strategy_3, data_3, expected_3

    @pytest.mark.parametrize("processing_strategy, data, expected", [case_1, case_2, case_3])
    def test_process_transaction_type(self, processing_strategy, data, expected):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # when
        result = self.create_payment_info(processing_strategy, data).type

        # then
        assert_that(result).is_equal_to(expected)

    # case1
    processing_strategy_1 = pay_by_link_payment_info
    data_1 = PayByLinkTransactionStub
    expected_1 = 'mbank'
    case_1 = processing_strategy_1, data_1, expected_1

    # case2
    processing_strategy_2 = dp_payment_info
    data_2 = DirectPaymentTransactionStub
    expected_2 = 'DE91100000000123456789'
    case_2 = processing_strategy_2, data_2, expected_2

    # case3
    processing_strategy_3 = card_payment_info
    data_3 = CardTransactionStub
    expected_3 = 'John Doe 1234********6789'
    case_3 = processing_strategy_3, data_3, expected_3

    @pytest.mark.parametrize("processing_strategy, data, expected", [case_1, case_2, case_3])
    def test_process_transaction_payment_mean(self, processing_strategy, data, expected):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # when
        result = self.create_payment_info(processing_strategy, data).payment_mean

        # then
        assert_that(result).is_equal_to(expected)

    def test_process_transaction_amount(self):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        processing_strategy = dp_payment_info
        data = self.DirectPaymentTransactionStub

        # when
        result = self.create_payment_info(processing_strategy, data).amount

        # then
        assert_that(result).is_equal_to(599)

    def test_process_transaction_currency(self):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # given
        processing_strategy = dp_payment_info
        data = self.DirectPaymentTransactionStub

        # when
        result = self.create_payment_info(processing_strategy, data).currency

        # then
        assert_that(result).is_equal_to("USD")

    def test_process_transaction_description(self):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # given
        processing_strategy = dp_payment_info
        data = self.DirectPaymentTransactionStub

        # when
        result = self.create_payment_info(processing_strategy, data).description

        # then
        assert_that(result).is_equal_to("FastFood")

    def test_process_transaction_date(self):
        # given
        processing_strategy = pay_by_link_payment_info
        data = self.PayByLinkTransactionStub

        # when
        result = self.create_payment_info(processing_strategy, data).date

        # then
        expected = '2021-05-13T09:01:43Z'
        assert_that(result).is_equal_to(expected)

    def test_process_transaction_amount_in_pln(self):
        # given
        processing_strategy = pay_by_link_payment_info
        data = self.PayByLinkTransactionStub

        # when
        result = self.create_payment_info(processing_strategy, data).amount_in_pln

        # then
        expected = 13494
        assert_that(result).is_equal_to(expected)

    def test_full_process_for_card_payment(self):
        # given
        processing_strategy = card_payment_info
        data = self.CardTransactionStub

        # when
        result = self.create_payment_info(processing_strategy, data)

        # then
        expected = self.CardPaymentInfoStub
        assert_that(result).is_equal_to(expected)

    # Request process tests
    @pytest.fixture(autouse=True)
    def prepare_test_process_request(self):
        self.process_request = process_request

    # case1
    request_1 = RequestStub_1
    expected_1 = [PayByLinkInfoStub.dict()]
    case_1 = request_1, expected_1

    # case1
    request_2 = RequestStub_2
    # take in consideration the correct order
    expected_2 = [CardPaymentInfoStub.dict(), PayByLinkInfoStub.dict()]
    case_2 = request_2, expected_2

    @pytest.mark.parametrize("test_request, expected", [case_1, case_2])
    def test_process_request(self, test_request, expected):
        # when
        result = self.process_request(test_request)

        # then
        assert_that(result).is_equal_to(expected)

    # Helpers tests
    @pytest.fixture(autouse=True)
    def prepare_iso8601_date_parser(self):
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

    @pytest.fixture(autouse=True)
    def prepare_convert_time_to_utc(self):
        self.convert_time_to_utc = convert_date_to_utc

    def test_convert_time_to_utc(self):
        # given
        date_input = datetime(2021, 5, 13, 1, 1, 43, tzinfo=timezone.utc) + timedelta(hours=8)

        # when '2021-05-13T09:01:43Z
        expected = datetime(2021, 5, 13, 9, 1, 43, tzinfo=timezone.utc)
        result = convert_date_to_utc(date_input)

        # then
        assert_that(result).is_equal_to(expected)

    @pytest.fixture(autouse=True)
    def prepare_get_date_normalized_str(self):
        self.get_date_normalized_str = get_date_normalized_str

    def test_get_date_normalized_str(self):
        # given
        date_instance = datetime(2007, 1, 25, 12, 0, tzinfo=timezone.utc)

        # when
        result = get_date_normalized_str(date_instance)

        # then
        expected = '2007-01-25T12:00:00Z'
        assert_that(result).is_equal_to(expected)

    @pytest.fixture(autouse=True)
    def prepare_get_valid_utc_iso8061_date(self):
        self.get_valid_utc_iso8061_date = get_valid_utc_iso8061_date

    # case1
    date_string_1 = '2021-05-13T01:01:43-08:00'
    expected_1 = datetime(2021, 5, 13, 9, 1, 43, tzinfo=timezone.utc)
    case_1 = date_string_1, expected_1

    # case2
    date_string_2 = '2021-05-14T08:27:09Z'
    expected_2 = datetime(2021, 5, 14, 8, 27, 9, tzinfo=timezone.utc)
    case_2 = date_string_2, expected_2

    # case3
    date_string_3 = '2021-05-13T09:00:05+02:00'
    expected_3 = datetime(2021, 5, 13, 7, 0, 5, tzinfo=timezone.utc)
    case_3 = date_string_3, expected_3

    # case4
    date_string_4 = '2021-05-14T18:32:26Z'
    expected_4 = datetime(2021, 5, 14, 18, 32, 26, tzinfo=timezone.utc)
    case_4 = date_string_4, expected_4

    @pytest.mark.parametrize("date_string, expected", [case_1, case_2, case_3, case_4])
    def test_get_valid_utc_string(self, date_string, expected):
        # when
        result = get_valid_utc_iso8061_date(date_string)

        # then
        assert_that(result).is_equal_to(expected)

    def test_get_valid_utc_string_error_handling(self):
        wrong_date_string = 'XX21-05-14T18:32:26Z'
        # when
        with pytest.raises(InvalidDateString):
            get_valid_utc_iso8061_date(wrong_date_string)

    @pytest.fixture(autouse=True)
    def prepare_mask_card_nr(self):
        self.mask_card_nr = mask_card_nr

    def test_mask_card_nr(self):
        # given
        card_nr_str = '1234222222226789'

        # when
        result = mask_card_nr(card_nr_str)

        # then
        expected = '1234********6789'
        assert_that(result).is_equal_to(expected)

    @pytest.fixture(autouse=True)
    def prepare_get_exchange_rate(self):
        self.get_nbp_exchange_rate = get_nbp_exchange_rate

    def test_get_exchange_rate(self):
        # given
        date_of_transaction = '2021-05-14'
        currency_of_transaction = 'USD'

        # when
        result = get_nbp_exchange_rate(date_of_transaction, currency_of_transaction)

        # then
        expected = 3.7055
        assert_that(result).is_equal_to(expected)

    @pytest.fixture(autouse=True)
    def prepare_calculate_amount_in_pln(self):
        self.calculate_amount_in_pln = calculate_amount_in_pln

    def test_calculate_amount_in_pln(self):
        # given
        amount_of_transaction = 599
        exchange_rate_of_transaction = 3.7055

        # when
        result = calculate_amount_in_pln(amount_of_transaction, exchange_rate_of_transaction)

        # then
        expected = 2219
        assert_that(result).is_equal_to(expected)

    @pytest.fixture(autouse=True)
    def prepare_prepare_nbp_date(self):
        self.prepare_nbp_date = prepare_nbp_date

    def test_prepare_nbp_date(self):
        # given
        datetime_for_nbp = datetime(2021, 5, 14, 1, 1, 43, tzinfo=timezone(timedelta(days=-1, seconds=57600), '-08:00'))

        # when
        result = prepare_nbp_date(datetime_for_nbp)

        # then
        expected = '2021-05-14'
        assert_that(result).is_equal_to(expected)
