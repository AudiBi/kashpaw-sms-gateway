import re


def validate_phone(number: str) -> bool:

    pattern = r"^509\d{8}$"

    return re.match(pattern, number) is not None