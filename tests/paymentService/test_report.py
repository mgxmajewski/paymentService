import pytest
from transactions.utils import get_transaction_types
from assertpy import assert_that


@pytest.mark.django_db
class TestReportUtilsTests:

    @pytest.fixture(autouse=True)
    def prepare_brute_force_cow_transport(self):
        self.get_transaction_types = get_transaction_types

    def test_server_check(self):
        """
        Ensure server is ready to work.
        """

        # given
        request = {
            "pay_by_link": [],
            "dp": [],
            "card": []
        }

        # when
        response = self.get_transaction_types(request)

        # then
        assert_that(response).is_equal_to(["pay_by_link", "dp", "card"])
