from abc import ABC
from dataclasses import dataclass


# class TransactionToProcess(ABC):
#     pass


@dataclass
class PaymentInfo:
    type: str


def pay_by_link_payment_info(data):
    print(data)
    return PaymentInfo('pay_by_link')


def dp_payment_info(data):
    print(data)
    return PaymentInfo('dp')


def card_payment_info(data):
    print(data)
    return PaymentInfo('card')


def create_payment_info(processing_strategy_fn, data):
    payment_info = processing_strategy_fn(data)
    return payment_info
