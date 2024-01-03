from flask import Flask, render_template, request, jsonify

from src.mortgage import Mortgage
from src.utils import convert_str_bool

app = Flask(__name__, static_folder='static', template_folder='templates')

def get_mortgage_data(price, num_of_months, interest_rate,
                      housing_inflation, rent_month,
                      initial_expenses, rent_increase,
                      is_first_estate, rent_return_month,
                      is_long_term_rent):
    mortgage_obj = Mortgage(price, num_of_months, interest_rate,
                            housing_inflation, rent_month,
                            initial_expenses, rent_increase,
                            is_first_estate, rent_return_month,
                            is_long_term_rent)
    mortgage_rent_be_value = -1
    mortgage_sell_be_value = -1
    mortgage_table = None
    if mortgage_obj.verify_input():
        mortgage_list = mortgage_obj.calculate_mortgage()
        mortgage_headers = mortgage_obj.generate_headers()
        mortgage_rent_be_value = mortgage_obj.get_rent_idx(mortgage_list)
        mortgage_sell_be_value = mortgage_obj.get_sell_idx(mortgage_list)
        mortgage_table = mortgage_obj.generate_table(mortgage_list, mortgage_headers)
    return mortgage_table, mortgage_rent_be_value, mortgage_sell_be_value

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
        initial_expenses = float(request.form['initial_expenses'])
        rent_increase = float(request.form['rent_increase'])
        is_first_estate = convert_str_bool(request.form['is_first_estate'])
        rent_return_month = float(request.form['rent_return_month'])
        is_long_term_rent = convert_str_bool(request.form['is_long_term_rent'])

    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400

    table, rent_be_value, sell_be_value = get_mortgage_data(price,
                                                            num_of_months,
                                                            interest_rate,
                                                            housing_inflation,
                                                            rent_month,
                                                            initial_expenses,
                                                            rent_increase,
                                                            is_first_estate,
                                                            rent_return_month,
                                                            is_long_term_rent)

    if table:
        response_data = {
            'table': table,
            'rent_be_value': rent_be_value,
            'sell_be_value': sell_be_value
        }
    else:
        response_data = {
            'rent_be_value': rent_be_value,
            'sell_be_value': sell_be_value
        }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
