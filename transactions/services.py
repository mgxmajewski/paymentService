from dataclasses import dataclass
import iso8601
import pytz


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


def iso8601_date_parser(date_str):
    date_from_str = iso8601.parse_date(date_str)
    return date_from_str


def convert_date_to_utc(date_instance):
    utc = pytz.utc
    date_in_utc = date_instance.astimezone(utc)
    return date_in_utc


def get_date_normalized_str(date_instance):
    return date_instance.strftime('%Y-%m-%dT%H:%M:%SZ')


def get_valid_utc_iso8061_date(date_str):
    validated_date = iso8601_date_parser(date_str)
    converted_to_utc_date = convert_date_to_utc(validated_date)
    return converted_to_utc_date


def mask_card_nr(card_nr_str):
    first_four = card_nr_str[:4]
    last_four = card_nr_str[-4:]
    mask_width = len(card_nr_str) - len(first_four) - len(last_four)
    masked_digits = '*' * mask_width
    masked_number = f'{first_four}{masked_digits}{last_four}'
    return masked_number

# base fetch url
# http://api.nbp.pl/api/exchangerates/rates/c/usd/2016-04-04/?format=json
# ask is the value to use for calculation ("selling price")
