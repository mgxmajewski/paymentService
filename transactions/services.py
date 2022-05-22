from abc import ABC
from dataclasses import dataclass, field


# class TransactionToProcess(ABC):
#     pass


@dataclass
class PaymentInfo:
    type: str = 'unprocessed'
    amount: int = 0


# list of the fields with direct mapping (one to one no name changing)
DIRECTLY_MAPPING_FIELDS = ['amount']


def map_direct_fields(data_to_map, data_receiver):
    is_dict_empty = not bool(data_to_map)
    if is_dict_empty:
        return
    for field_to_update in DIRECTLY_MAPPING_FIELDS:
        new_val = data_to_map[field_to_update]
        setattr(data_receiver, field_to_update, new_val)


def pay_by_link_payment_info(data):
    return PaymentInfo('pay_by_link')


def dp_payment_info(data):
    new_payment_info = PaymentInfo()
    map_direct_fields(data, new_payment_info)
    new_payment_info.type = 'dp'
    return new_payment_info


def card_payment_info(data):
    return PaymentInfo('card')


def create_payment_info(processing_strategy_fn, data):
    payment_info = processing_strategy_fn(data)
    return payment_info
