from typing import Union, Type

class MortgageConf:

    class RentTerm:
        NO_TERM = 0
        LONG_TERM = 1
        SHORT_TERM = 2
        MIXED_TERM = 3

    FIRST_PROPERTY_MAX_VALUE = 440000

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