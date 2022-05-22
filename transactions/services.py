from abc import ABC
from dataclasses import dataclass


class TransactionToProcess(ABC):
    pass


@dataclass
class PaymentInfo:
    type: str


def pay_by_link_payment_info(data: TransactionToProcess):
    print(data)
    return PaymentInfo('pay_by_link')


def dp_payment_info(data: TransactionToProcess):
    print(data)
    return


def card_payment_info(data: TransactionToProcess):
    print(data)
    return


def create_payment_info(processing_strategy_fn, data: TransactionToProcess):
    payment_info = processing_strategy_fn(data)
    return payment_info
