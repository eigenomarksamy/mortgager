
def convert_str_bool(string: str) -> bool:
    if string.lower() == "true":
        return True
    return False

def convert_percent(num: float) -> float:
    return num / 100

def calculate_pmt(price: float, interest_rate: float, num_months: int) -> float:
    return -((price * (interest_rate / 12)) / (1 - pow(1 + (interest_rate / 12), -num_months)))
