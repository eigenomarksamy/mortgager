"""Request handling shared by the Flask server (app.py) and the static build.

Both pass in the raw form fields as strings and get back the same response,
so the parsing and calculation only live in one place. In the static build,
static/js/script.js calls calculate_json() in the browser through Pyodide.
"""
import json
from typing import Mapping, Tuple

from src.mortgage import Mortgage
from src.utils import convert_str_bool


def get_mortgage_data(price, num_of_months, interest_rate,
                      housing_inflation, rent_month, overbidding,
                      property_fixup, realtor_fee, rent_increase,
                      is_first_estate, older_than_35, rent_return_month,
                      rental_term):
    mortgage_obj = Mortgage(price, num_of_months, interest_rate,
                            housing_inflation, rent_month,
                            overbidding, property_fixup, realtor_fee,
                            rent_increase, is_first_estate, older_than_35,
                            rent_return_month, rental_term)
    mortgage_rent_be_value = -1
    mortgage_sell_be_value = -1
    mortgage_rent_out_be_value = -1
    mortgage_table = None
    if mortgage_obj.verify_input():
        mortgage_list = mortgage_obj.calculate_mortgage()
        mortgage_headers = mortgage_obj.generate_headers()
        mortgage_rent_be_value = mortgage_obj.get_rent_idx(mortgage_list)
        mortgage_sell_be_value = mortgage_obj.get_sell_idx(mortgage_list)
        mortgage_rent_out_be_value = mortgage_obj.get_rent_out_idx(mortgage_list)
        mortgage_table = mortgage_obj.generate_table(mortgage_list, mortgage_headers)
    return mortgage_table, mortgage_rent_be_value, mortgage_sell_be_value, mortgage_rent_out_be_value


def calculate(form: Mapping[str, str]) -> Tuple[dict, int]:
    """Parses the form fields and returns (response data, HTTP status)."""
    try:
        price = float(form['price'])
        num_of_months = int(form['num_of_months'])
        interest_rate = float(form['interest_rate'])
        housing_inflation = float(form['housing_inflation'])
        rent_month = float(form['rent_month'])
        overbidding = float(form['overbidding'])
        property_fixup = float(form['property_fixup'])
        realtor_fee = float(form['realtor_fee'])
        rent_increase = float(form['rent_increase'])
        is_first_estate = convert_str_bool(form['is_first_estate'])
        older_than_35 = convert_str_bool(form['older_than_35'])
        rent_return_month = float(form['rent_return_month'])
        rental_term = str(form['rental_term'])

    except ValueError:
        return {'error': 'Invalid input. Please enter valid numbers.'}, 400

    table, rent_be_value, sell_be_value, rent_out_be_value = get_mortgage_data(price,
            num_of_months, interest_rate, housing_inflation, rent_month, overbidding,
            property_fixup, realtor_fee, rent_increase, is_first_estate, older_than_35,
            rent_return_month, rental_term)

    response_data = {
        'rent_be_value': rent_be_value,
        'sell_be_value': sell_be_value,
        'rent_out_be_value': rent_out_be_value
    }
    if table:
        response_data['table'] = table
    return response_data, 200


def calculate_json(form_json: str) -> str:
    """Entry point for the browser: form fields as JSON in, response as JSON out."""
    response_data, _status = calculate(json.loads(form_json))
    return json.dumps(response_data)
