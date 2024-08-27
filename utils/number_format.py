import re

def format_number(number: str) -> str:
    digits = re.sub(r'\D', '', number)
    formatted_number = f"{digits[:3]}-{digits[3:6]}-{digits[6:9]} {digits[9:11]}"

    return formatted_number