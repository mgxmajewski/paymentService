import pytest
from assertpy import assert_that
from transactions.services import get_payment_info, PaymentInfo


@pytest.mark.django_db
class TestTransactionsServices:

    @pytest.fixture(autouse=True)
    def prepare_get_payment_info(self):
        self.get_payment_info = get_payment_info

    def test_get_payment_info(self):
        """
        Ensure server is ready to work.
        """

        # given
        transaction_type = 'pay_by_link'

        # when
        result = self.get_payment_info('pay_by_link')

        # then
        assert_that(result).is_equal_to(PaymentInfo(type='pay_by_link'))
