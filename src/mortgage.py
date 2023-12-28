import math

class Mortgage:
    def __init__(self, price: float, num_of_months: int, interest_rate: float,
                 housing_inflation: float, rent_month: float,
                 initial_expenses: float, rent_increase: float,
                 is_first_estate: bool) -> None:
        self._price = price
        self._num_of_months = num_of_months
        self._interest_rate = interest_rate
        self._housing_inflation = housing_inflation
        self._rent_month = rent_month
        self._initial_expenses = initial_expenses
        self._rent_increase = rent_increase
        self._is_first_estate = is_first_estate

def convert_percent(num: float) -> float:
    return num / 100

def calculate_pmt(price: float, interest_rate: float, num_months: int) -> float:
    return -((price * (interest_rate / 12)) / (1 - pow(1 + (interest_rate / 12), -num_months)))

def compute_interest_to_be_paid(total_debt: float, interest_rate: float) -> float:
    return total_debt * (convert_percent(interest_rate) / 12)

def compute_repayment(pmt: float, payable_interest: float) -> float:
    return pmt - payable_interest

def compute_residual_debt(total_debt: float, repayment_due: float) -> float:
    return total_debt - repayment_due

def compute_total_gain_for_rent(total_paid_interest: float, initial_fees: float, total_paid_rent: float) -> float:
    return total_paid_interest + initial_fees - total_paid_rent

def compute_selling_gain(estate_worth: float, total_debt: float, initial_fees: float) -> float:
    return estate_worth - total_debt - initial_fees

def compute_current_rent(rent_to_compare: float, rent_annual_increase: float, month: int) -> float:
    return rent_to_compare * pow(1 + convert_percent(rent_annual_increase), math.floor((month - 1) / 12))

def compute_estate_market_value(estate_worth: float, market_increase: float) -> float:
    return estate_worth * (1 + convert_percent(market_increase) / 12)

def get_idx_of_sign_change(list_to_search: list, key: str) -> int:
    for i in range(1, len(list_to_search)):
        if list_to_search[i][key] < 0 and list_to_search[i - 1][key] >= 0:
            return i + 1
        elif list_to_search[i][key] > 0 and list_to_search[i - 1][key] <= 0:
            return i + 1
    return -1

def calculate_mortgage_table(price: float, num_of_months: int, interest_rate: float,
                             housing_inflation: float, rent_month: float,
                             initial_expenses: float, rent_increase: float) -> list:
    lst = []
    dct_init = {}
    dct_init['period'] = 1
    dct_init['total_debt'] = price
    dct_init['payable_interest'] = compute_interest_to_be_paid(dct_init['total_debt'], interest_rate)
    total_pmt = -calculate_pmt(price, convert_percent(interest_rate), num_of_months)
    dct_init['repayment_due'] = compute_repayment(total_pmt, dct_init['payable_interest'])
    dct_init['residual_debt'] = compute_residual_debt(dct_init['total_debt'], dct_init['repayment_due'])
    dct_init['total_paid_rent'] = rent_month
    dct_init['total_paid_interest'] = dct_init['payable_interest']
    dct_init['rent_net_profit'] = compute_total_gain_for_rent(dct_init['total_paid_interest'], initial_expenses, dct_init['total_paid_rent'])
    dct_init['estate_value'] = price
    dct_init['selling_profit'] = compute_selling_gain(dct_init['estate_value'], dct_init['total_debt'], initial_expenses)
    lst.append(dct_init)
    total_debt = dct_init['total_debt']
    repayment_due = dct_init['repayment_due']
    total_paid_rent = dct_init['total_paid_rent']
    total_paid_interest = dct_init['total_paid_interest']
    estate_value = dct_init['estate_value']
    for period in range(2, num_of_months + 1):
        dct = {}
        dct['period'] = period
        dct['total_debt'] = total_debt - repayment_due
        dct['payable_interest'] = compute_interest_to_be_paid(dct['total_debt'], interest_rate)
        dct['repayment_due'] = compute_repayment(total_pmt, dct['payable_interest'])
        dct['residual_debt'] = compute_residual_debt(dct['total_debt'], dct['repayment_due'])
        dct['total_paid_rent'] = total_paid_rent + compute_current_rent(rent_month, convert_percent(rent_increase), dct['period'])
        dct['total_paid_interest'] = total_paid_interest + dct['payable_interest']
        dct['rent_net_profit'] = compute_total_gain_for_rent(dct['total_paid_interest'], initial_expenses, dct['total_paid_rent'])
        dct['estate_value'] = compute_estate_market_value(estate_value, convert_percent(housing_inflation))
        dct['selling_profit'] = compute_selling_gain(dct['estate_value'], dct['total_debt'], initial_expenses)
        total_debt = dct['total_debt']
        repayment_due = dct['repayment_due']
        total_paid_rent = dct['total_paid_rent']
        total_paid_interest = dct['total_paid_interest']
        estate_value = dct['estate_value']
        lst.append(dct)
    return lst

def get_rent_idx(mortgage_table: list) -> int:
    return get_idx_of_sign_change(mortgage_table, 'rent_net_profit')

def get_sell_idx(mortgage_table: list) -> int:
    return get_idx_of_sign_change(mortgage_table, 'selling_profit')

def generate_headers() -> list:
    return ["Month", "Total debt", "Payable interest", "Repayment due",
            "Residual debt", "Total paid rent", "Total paid interest",
            "Rent net profit", "Estate value", "Selling profit"]