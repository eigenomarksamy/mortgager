from typing import Union, Type

class MortgageConf:

    class RentTerm:
        NO_TERM = 0
        LONG_TERM = 1
        SHORT_TERM = 2
        MIXED_TERM = 3

    FIRST_PROPERTY_MAX_VALUE = 440000

    PROPERTY_TRANSFER_TAX_PERCENT = 2

    LONG_TERM_RENTED_MONTHS = 3 * 12

    SHORT_TERM_RENTED_MONTHS = 1

    MIXED_TERM_RENTED_MONTHS = 1.5 * 12

    LONG_TERM_RENT_MONTHS_VACANT_PER_YEAR = 1

    SHORT_TERM_RENT_MONTHS_VACANT_PER_YEAR = 6

    MIXED_TERM_RENT_MONTHS_VACANT_PER_YEAR = 3

    LONG_TERM_MONTHS_TO_SKIP = 13

    SHORT_TERM_MONTHS_TO_SKIP = 5

    MIXED_TERM_MONTHS_TO_SKIP = 7

    RENOVATION_COSTS_MONTHLY_RENTS = 3

    RENTAL_TERM_MAP = {"no_term": RentTerm.NO_TERM,
                       "long_term": RentTerm.LONG_TERM,
                       "short_term": RentTerm.SHORT_TERM,
                       "mixed_term": RentTerm.MIXED_TERM}

    @staticmethod
    def convert_rental_term(txt_str: str) -> Union[int, Type["MortgageConf.RentTerm"]]:
        if txt_str == "long_term":
            return MortgageConf.RentTerm.LONG_TERM
        elif txt_str == "short_term":
            return MortgageConf.RentTerm.SHORT_TERM
        elif txt_str == "mixed_term":
            return MortgageConf.RentTerm.MIXED_TERM
        else:
            return MortgageConf.RentTerm.NO_TERM