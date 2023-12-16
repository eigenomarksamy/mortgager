from flask import Flask, render_template, request, jsonify

from src.mortgage import calculate_mortgage_table, generate_headers, \
    get_rent_idx, get_sell_idx

app = Flask(__name__, static_folder='static', template_folder='templates')

def generate_table(lst_dct):
    table = []
    headers = generate_headers()
    table.append(headers)
    for dct in (lst_dct):
        row = list(dct.values())
        table.append(row)
    return table

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
    except ValueError:
        return jsonify({'error': 'Invalid input. Please enter valid numbers.'}), 400

    result_lst = calculate_mortgage_table(price, num_of_months, interest_rate,
                                          housing_inflation, rent_month,
                                          initial_expenses, rent_increase)

    rent_be_value = get_rent_idx(result_lst)
    sell_be_value = get_sell_idx(result_lst)

    table = generate_table(result_lst)

    response_data = {
        'table': table,
        'rent_be_value': rent_be_value,
        'sell_be_value': sell_be_value
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
