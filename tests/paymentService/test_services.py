import pytest
from assertpy import assert_that
from transactions.services import create_payment_info, pay_by_link_payment_info, TransactionToProcess


@pytest.mark.django_db
class TestTransactionsServices:

    @pytest.fixture(autouse=True)
    def prepare_get_payment_info(self):
        self.process_transaction = create_payment_info

    def test_process_transaction(self):
        """
        Ensure transaction type after processing matches the chosen strategy
        """

        # given
        processing_strategy = pay_by_link_payment_info
        data = TransactionToProcess()

        # when
        result = self.process_transaction(processing_strategy, data).type

        # then
        assert_that(result).is_equal_to('pay_by_link')
