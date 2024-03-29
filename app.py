from flask import Flask, render_template, request, jsonify

from src.mortgage import Mortgage
from src.utils import convert_str_bool

app = Flask(__name__, static_folder='static', template_folder='templates')

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        price = float(request.form['price'])
        num_of_months = int(request.form['num_of_months'])
        interest_rate = float(request.form['interest_rate'])
        housing_inflation = float(request.form['housing_inflation'])
        rent_month = float(request.form['rent_month'])
        overbidding = float(request.form['overbidding'])
        property_fixup = float(request.form['property_fixup'])
        realtor_fee = float(request.form['realtor_fee'])
        rent_increase = float(request.form['rent_increase'])
        is_first_estate = convert_str_bool(request.form['is_first_estate'])
        older_than_35 = convert_str_bool(request.form['older_than_35'])
        rent_return_month = float(request.form['rent_return_month'])
        rental_term = str(request.form['rental_term'])

    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400

    table, rent_be_value, sell_be_value, rent_out_be_value = get_mortgage_data(price,
            num_of_months, interest_rate, housing_inflation, rent_month, overbidding,
            property_fixup, realtor_fee, rent_increase, is_first_estate, older_than_35,
            rent_return_month, rental_term)

    if table:
        response_data = {
            'table': table,
            'rent_be_value': rent_be_value,
            'sell_be_value': sell_be_value,
            'rent_out_be_value': rent_out_be_value
        }
    else:
        response_data = {
            'rent_be_value': rent_be_value,
            'sell_be_value': sell_be_value,
            'rent_out_be_value': rent_out_be_value
        }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
