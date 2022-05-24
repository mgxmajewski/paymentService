from dataclasses import dataclass
import iso8601
import pytz
import requests
from pydantic import BaseModel


class PayByLink(BaseModel):
    created_at: str
    currency: str
    amount: int
    description: str
    bank: str


class DirectPayment(BaseModel):
    created_at: str
    currency: str
    amount: int
    description: str
    iban: str


class Card(BaseModel):
    created_at: str
    currency: str
    amount: int
    description: str
    cardholder_name: str
    cardholder_surname: str
    card_number: str


class PaymentInfo(BaseModel):
    date: str = 'unprocessed'
    type: str
    amount: int
    description: str
    currency: str
    payment_mean: str
    amount_in_pln: int = 0


def pay_by_link_payment_info(data):
    # handle the date
    temp_datetime = get_valid_utc_iso8061_date(data.created_at)
    normalized_date_string = get_date_normalized_str(temp_datetime)

    # direct mapping
    amount = data.amount
    currency = data.currency
    description = data.description

    # conversion to PLN handler
    calculated_amount_in_pln = conversion_handler(temp_datetime, amount, currency)

    # strategy specific mapping
    payment_mean = data.bank

    new_payment_info = PaymentInfo(type='pay_by_link',
                                   date=normalized_date_string,
                                   amount=amount,
                                   currency=currency,
                                   description=description,
                                   payment_mean=payment_mean,
                                   amount_in_pln=calculated_amount_in_pln)
    return new_payment_info


def dp_payment_info(data):
    # handle the date
    temp_datetime = get_valid_utc_iso8061_date(data.created_at)
    normalized_date_string = get_date_normalized_str(temp_datetime)

    # direct mapping
    amount = data.amount
    currency = data.currency
    description = data.description

    # conversion to PLN handler
    calculated_amount_in_pln = conversion_handler(temp_datetime, amount, currency)

    # strategy specific mapping
    payment_mean = data.iban
    new_payment_info = PaymentInfo(type='dp',
                                   date=normalized_date_string,
                                   amount=amount,
                                   currency=currency,
                                   description=description,
                                   payment_mean=payment_mean,
                                   amount_in_pln=calculated_amount_in_pln)
    return new_payment_info


def card_payment_info(data):
    # handle the date
    temp_datetime = get_valid_utc_iso8061_date(data.created_at)
    normalized_date_string = get_date_normalized_str(temp_datetime)

    # direct mapping
    amount = data.amount
    currency = data.currency
    description = data.description

    # conversion to PLN handler
    calculated_amount_in_pln = conversion_handler(temp_datetime, amount, currency)

    # strategy specific mapping
    payment_mean_masked_card_details = get_payment_mean_card_str(data)

    result = PaymentInfo(type='card',
                         date=normalized_date_string,
                         amount=amount,
                         currency=currency,
                         description=description,
                         payment_mean=payment_mean_masked_card_details,
                         amount_in_pln=calculated_amount_in_pln)
    return result


def create_payment_info(processing_strategy_fn, data):
    payment_info = processing_strategy_fn(data)
    return payment_info


def get_payment_mean_card_str(data_source):
    cardholder_name = data_source.cardholder_name
    cardholder_surname = data_source.cardholder_surname
    card_number = data_source.card_number
    masked_card_number = mask_card_nr(card_number)
    return f"{cardholder_name} {cardholder_surname} {masked_card_number}"


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


def get_nbp_exchange_rate(date_of_transaction, currency_of_transaction):
    # QUESTION. Shouldn't here be a 'ask'? Now the specification indicates otherwise.
    # The user gets currency in lower price (not like in real life).
    selected_rate_type = 'bid'
    payload_from_nbp = requests.get(
        f'https://api.nbp.pl/api/exchangerates/rates/c/{currency_of_transaction.lower()}/{date_of_transaction}/?format=json')
    print(payload_from_nbp.json())
    payload_json = payload_from_nbp.json()
    rates_from_nbp = payload_json['rates'][0]
    exchange_rate_str = rates_from_nbp[selected_rate_type]
    exchange_rate = float(exchange_rate_str)
    return exchange_rate


def calculate_amount_in_pln(amount_of_transaction, exchange_rate_of_transaction):
    price_in_currency = amount_of_transaction / 100
    exchange_result = price_in_currency * exchange_rate_of_transaction * 100
    result_rounded_down = int(exchange_result)
    return result_rounded_down


def prepare_nbp_date(datetime_to_parse):
    return datetime_to_parse.strftime('%Y-%m-%d')


def conversion_handler(date, amount, currency):
    if currency is 'PLN':
        calculated_amount_in_pln = amount
    else:
        temp_datetime_nbp = prepare_nbp_date(date)
        temp_exchange_rate = get_nbp_exchange_rate(temp_datetime_nbp, currency)
        calculated_amount_in_pln = calculate_amount_in_pln(amount, temp_exchange_rate)

    return calculated_amount_in_pln


def map_direct_fields(data_source, data_receiver):
    data_receiver.amount = data_source.amount
    data_receiver.currency = data_source.currency
    data_receiver.description = data_source.description
