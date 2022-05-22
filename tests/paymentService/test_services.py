import pytest
from assertpy import assert_that

from transactions.services import create_payment_info, pay_by_link_payment_info, dp_payment_info, card_payment_info


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
