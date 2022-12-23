from .parser import *

__all__ = ["verify_chsi", "pre_check_verify_code"]


def pre_check_verify_code(verify_code: str) -> bool:
    if len(verify_code) != 16:
        return False
    if verify_code[0] != 'A':
        return False
    if not verify_code.isalnum():
        return False
    if not verify_code.isupper():
        return False
    return True
