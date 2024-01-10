
def convert_str_bool(string: str) -> bool:
    if string.lower() == "true":
        return True
    return False

def convert_percent(num: float) -> float:
    return num / 100

def calculate_pmt(price: float, interest_rate: float, num_months: int) -> float:
    return -((price * (interest_rate / 12)) / (1 - pow(1 + (interest_rate / 12), -num_months)))

def get_idx_of_sign_change(list_to_search: list, key: str) -> int:
    for i in range(1, len(list_to_search)):
        if list_to_search[i][key] < 0 and list_to_search[i - 1][key] >= 0:
            return i + 1
        elif list_to_search[i][key] > 0 and list_to_search[i - 1][key] <= 0:
            return i + 1
    return -1
