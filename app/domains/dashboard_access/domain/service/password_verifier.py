import hmac


def verify_password(input_password: str, expected_password: str | None) -> bool:
    if not expected_password:
        return False
    return hmac.compare_digest(input_password, expected_password)
