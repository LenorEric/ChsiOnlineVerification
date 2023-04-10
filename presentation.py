from chsiverify import *

verify_code = ""  # Enter your verify code here

if __name__ == '__main__':
    while True:
        result = verify_chsi(verify_code)
        print(result)
        print(len(result))
        while True:
            pass
