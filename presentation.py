from chsiverify import *

verify_code = "AB3YM4WTNM4H3XGU"  # Enter your verify code here

if __name__ == '__main__':
    while True:
        result = verify_chsi(verify_code)
        print(result)
        print(len(result))
