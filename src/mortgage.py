import math

from typing import Union, Type

from src.conf import MortgageConf
from src.utils import convert_percent, calculate_pmt, get_idx_of_sign_change

class Mortgage:
    def __init__(self, price: float, num_of_months: int,
                 interest_rate: float, housing_inflation: float,
                 rent_month: float, overbidding: float,
                 property_fixup: float, realtor_fee: float,
                 rent_increase: float, is_first_estate: bool,
                 rent_return_month: float, rental_term: str) -> None:
        self._price = price
        self._num_of_months = num_of_months
        self._interest_rate = interest_rate
        self._housing_inflation = housing_inflation
        self._rent_month = rent_month
        self._initial_expenses = overbidding + property_fixup + self._price * convert_percent(realtor_fee)
        self._rent_increase = rent_increase
        self._is_first_estate = is_first_estate
        self._rent_return_month = rent_return_month
        self._rental_term = MortgageConf.convert_rental_term(rental_term)

    def verify_input(self) -> bool:
        if self._is_first_estate:
            self._rental_term = MortgageConf.convert_rental_term("no_term")
        return self.verify_property_price()

    def verify_property_price(self) -> bool:
        if self._is_first_estate:
            if self._price > MortgageConf.FIRST_PROPERTY_MAX_VALUE:
                return False
        else:
            self._price *= (1 + convert_percent(MortgageConf.PROPERTY_TRANSFER_TAX_PERCENT))
        return True

    def generate_headers(self) -> list:
        return ["Month", "Total debt", "Monthly payment", "Payable interest",
                "Repayment due", "Residual debt", "Total paid rent",
                "Total paid interest", "Rent net profit", "Estate value",
                "Selling profit", "Gross return rent",
                "Accumulated gross rent return", "Cost rent",
                "Accumulated cost rent", "Rent out net gain"]

    def generate_table(self, lst_dct: list, headers: list) -> list:
        table = []
        table.append(headers)
        for dct in (lst_dct):
            row = list(dct.values())
            table.append(row)
        return table

    def get_rent_idx(self, mortgage_table: list) -> int:
        return get_idx_of_sign_change(mortgage_table, 'rent_net_profit')

    def get_sell_idx(self, mortgage_table: list) -> int:
        return get_idx_of_sign_change(mortgage_table, 'selling_profit')

    def get_rent_out_idx(self, mortgage_table: list) -> int:
        return get_idx_of_sign_change(mortgage_table, 'rent_out_net_gain')

    def calculate_mortgage(self) -> list:
        lst = []
        dct_init = {}
        dct_init['period'] = 1
        dct_init['total_debt'] = self._price
        dct_init['monthly_payment'] = self._price / self._num_of_months
        dct_init['payable_interest'] = compute_interest_to_be_paid(dct_init['total_debt'], convert_percent(self._interest_rate))
        total_pmt = -calculate_pmt(self._price, convert_percent(self._interest_rate), self._num_of_months)
        dct_init['repayment_due'] = compute_repayment(total_pmt, dct_init['payable_interest'])
        dct_init['residual_debt'] = compute_residual_debt(dct_init['total_debt'], dct_init['repayment_due'])
        dct_init['total_paid_rent'] = self._rent_month
        dct_init['total_paid_interest'] = dct_init['payable_interest']
        dct_init['rent_net_profit'] = compute_total_gain_for_rent(dct_init['total_paid_interest'], self._initial_expenses, dct_init['total_paid_rent'])
        dct_init['estate_value'] = self._price
        dct_init['selling_profit'] = compute_selling_gain(dct_init['estate_value'], dct_init['total_debt'], self._initial_expenses)
        dct_init['rent_out_gross'] = compute_current_renting_out(self._rent_return_month, convert_percent(self._rent_increase), dct_init['period'], self._rental_term)
        dct_init['total_return_from_renting_out'] = dct_init['rent_out_gross']
        dct_init['rent_out_cost'] = compute_renting_out_cost(self._rental_term, dct_init['period'], dct_init['rent_out_gross'])
        dct_init['total_cost_from_renting_out'] = dct_init['rent_out_cost']
        dct_init['rent_out_net_gain'] = compute_renting_out_net_gain(self._rental_term, dct_init['total_return_from_renting_out'], dct_init['total_cost_from_renting_out'], dct_init['total_debt'])
        lst.append(dct_init)
        total_debt = dct_init['total_debt']
        repayment_due = dct_init['repayment_due']
        total_paid_rent = dct_init['total_paid_rent']
        total_paid_interest = dct_init['total_paid_interest']
        estate_value = dct_init['estate_value']
        rent_out_gross = dct_init['rent_out_gross']
        rent_out_cost = dct_init['rent_out_cost']
        total_cost_from_renting_out = rent_out_cost
        total_return_from_renting_out = rent_out_gross
        for period in range(2, self._num_of_months + 1):
            dct = {}
            dct['period'] = period
            dct['total_debt'] = total_debt - repayment_due
            dct['monthly_payment'] = self._price / self._num_of_months
            dct['payable_interest'] = compute_interest_to_be_paid(dct['total_debt'], convert_percent(self._interest_rate))
            dct['repayment_due'] = compute_repayment(total_pmt, dct['payable_interest'])
            dct['residual_debt'] = compute_residual_debt(dct['total_debt'], dct['repayment_due'])
            dct['total_paid_rent'] = total_paid_rent + compute_current_rent(self._rent_month, convert_percent(self._rent_increase), dct['period'])
            dct['total_paid_interest'] = total_paid_interest + dct['payable_interest']
            dct['rent_net_profit'] = compute_total_gain_for_rent(dct['total_paid_interest'], self._initial_expenses, dct['total_paid_rent'])
            dct['estate_value'] = compute_estate_market_value(estate_value, convert_percent(self._housing_inflation))
            dct['selling_profit'] = compute_selling_gain(dct['estate_value'], dct['total_debt'], self._initial_expenses)
            dct['rent_out_gross'] = compute_current_renting_out(rent_out_gross, convert_percent(self._rent_increase), dct['period'], self._rental_term)
            dct['total_return_from_renting_out'] = total_return_from_renting_out
            dct['rent_out_cost'] = compute_renting_out_cost(self._rental_term, dct['period'], dct['rent_out_gross'])
            dct['total_cost_from_renting_out'] = total_cost_from_renting_out
            dct['rent_out_net_gain'] = compute_renting_out_net_gain(self._rental_term, dct['total_return_from_renting_out'], dct['total_cost_from_renting_out'], dct['total_debt'])
            total_debt = dct['total_debt']
            repayment_due = dct['repayment_due']
            total_paid_rent = dct['total_paid_rent']
            total_paid_interest = dct['total_paid_interest']
            estate_value = dct['estate_value']
            rent_out_gross = dct['rent_out_gross']
            rent_out_cost = dct['rent_out_cost']
            total_return_from_renting_out += rent_out_gross
            total_cost_from_renting_out += rent_out_cost
            lst.append(dct)
        return lst

def compute_interest_to_be_paid(total_debt: float, interest_rate: float) -> float:
    return total_debt * (interest_rate / 12)

def compute_repayment(pmt: float, payable_interest: float) -> float:
    return pmt - payable_interest

def compute_residual_debt(total_debt: float, repayment_due: float) -> float:
    return total_debt - repayment_due

def compute_total_gain_for_rent(total_paid_interest: float, initial_fees: float, total_paid_rent: float) -> float:
    return total_paid_interest + initial_fees - total_paid_rent

def compute_selling_gain(estate_worth: float, total_debt: float, initial_fees: float) -> float:
    return estate_worth - total_debt - initial_fees

def compute_current_rent(rent_to_compare: float, rent_annual_increase: float, month: int) -> float:
    return rent_to_compare * pow(1 + rent_annual_increase, math.floor((month - 1) / 12))

def compute_estate_market_value(estate_worth: float, market_increase: float) -> float:
    return estate_worth * (1 + market_increase / 12)

def compute_current_renting_out(rent: float, renting_out_annual_increase: float, month: int, rent_term: Union[int, Type["MortgageConf.RentTerm"]]) -> float:
    months_to_skip = 0
    if rent_term == MortgageConf.RentTerm.LONG_TERM:
        months_to_skip = MortgageConf.LONG_TERM_MONTHS_TO_SKIP
    elif rent_term == MortgageConf.RentTerm.SHORT_TERM:
        months_to_skip = MortgageConf.SHORT_TERM_MONTHS_TO_SKIP
    elif rent_term == MortgageConf.RentTerm.MIXED_TERM:
        months_to_skip = MortgageConf.MIXED_TERM_MONTHS_TO_SKIP
    else:
        return 0
    if month % months_to_skip == 0:
        return rent
    elif month % 12 == 0:
        adjusted_rate_of_increase = 1 + renting_out_annual_increase
        next_month_rent = rent * adjusted_rate_of_increase
        return next_month_rent
    else:
        return rent

def compute_renting_out_cost(rent_term: Union[int, Type["MortgageConf.RentTerm"]], month: int, rent: float) -> float:
    next_renovation = 0
    if rent_term == MortgageConf.RentTerm.LONG_TERM:
        next_renovation = MortgageConf.LONG_TERM_MONTHS_TO_SKIP
    elif rent_term == MortgageConf.RentTerm.SHORT_TERM:
        next_renovation = MortgageConf.SHORT_TERM_MONTHS_TO_SKIP
    elif rent_term == MortgageConf.RentTerm.MIXED_TERM:
        next_renovation = MortgageConf.MIXED_TERM_MONTHS_TO_SKIP
    else:
        return 0
    if month % next_renovation == 0:
        return rent * MortgageConf.RENOVATION_COSTS_MONTHLY_RENTS
    else:
        return 0

def compute_renting_out_net_gain(rent_term: Union[int, Type["MortgageConf.RentTerm"]], total_return_rent: float, total_cost_rent: float, total_debt: float) -> float:
    if rent_term == MortgageConf.RentTerm.NO_TERM:
        return 0
    else:
        return total_return_rent - total_cost_rent - total_debt
