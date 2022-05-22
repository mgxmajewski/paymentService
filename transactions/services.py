from dataclasses import dataclass


@dataclass
class PaymentInfo:
    type: str = 'unprocessed'
    amount: int = 0
    description = 'unprocessed'
    currency = 'unprocessed'
    payment_mean = 'unprocessed'


# list of the fields with direct mapping (one to one no name changing)
DIRECTLY_MAPPING_FIELDS = ['amount', 'currency', 'description']


def map_direct_fields(data_to_map, data_receiver):
    for field_to_update in DIRECTLY_MAPPING_FIELDS:
        if field_to_update not in data_to_map:
            # good place to collect information if request data was complete
            continue
        new_val = data_to_map[field_to_update]
        setattr(data_receiver, field_to_update, new_val)


def pay_by_link_payment_info(data):
    new_payment_info = PaymentInfo()
    new_payment_info.type = 'pay_by_link'
    if 'bank' in data:
        new_payment_info.payment_mean = data['bank']
    else:
        # good place to collect information if request data was complete
        pass
    return new_payment_info


def dp_payment_info(data):
    new_payment_info = PaymentInfo()
    map_direct_fields(data, new_payment_info)
    new_payment_info.type = 'dp'
    if 'iban' in data:
        new_payment_info.payment_mean = data['iban']
    else:
        # good place to collect information if request data was complete
        pass
    return new_payment_info


def card_payment_info(data):
    new_payment_info = PaymentInfo()
    new_payment_info.type = 'card'
    return new_payment_info


def create_payment_info(processing_strategy_fn, data):
    payment_info = processing_strategy_fn(data)
    return payment_info
