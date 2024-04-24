from calculator import Calculator
from rate_limiter import RateLimiter
import time


class API:
    """Interface between the Calculator service. Request is limited with a Rate Limiter."""

    def __init__(self, token_size):
        self.__calc = Calculator()
        self.__limiter = RateLimiter(token_size=token_size)

    def add(self, *args):
        if self.__limiter.run():
            return self.__calc.addition(*args)

    def multiply(self, *args):
        if self.__limiter.run():
            return self.__calc.multiplication(*args)

    def subtract(self, *args):
        if self.__limiter.run():
            return self.__calc.subtraction(*args)

    def division(self, *args):
        if self.__limiter.run():
            return self.__calc.division(*args)


def input_token_size():
    while 1:
        try:
            token_size = int(
                input(
                    "please input the number of request allowed in the api per minute: "
                )
            )
            seconds_to_wait_to_simulate_request = int(input('seconds to wait to simulate requests: '))
            return token_size, seconds_to_wait_to_simulate_request
        except ValueError:
            print("number should be integer.")


def api_welcome():
    print()
    print(
        "Calculator API with Rate Limiter. Custom implementation of TokenBucket Algorithm."
    )
    print(
        "Request are made concurrently. Change wait_time accordingly to simulate request to the API. "
    )
    print(
        "New TokenBucket is available in this time format: 12:01:00 minute i.e. beginning of each minute.\n"
    )
    print('Logic: If the token size is 5 and total request made in current minute are 3\nthen the at the next minute the bucket will be reset to 5 tokens.')
    print()


def main():
    api_welcome()
    token_size, wait_time = input_token_size()
    api = API(token_size=token_size)

    print(f"Request is being made with {wait_time} seconds interval\n")
    time.sleep(wait_time)
    
    print('#######################################')
    num = 0
    while 1:
        # for simplicity, sending concurrent add request to the api.
        res = api.add(1, 2, 3)
        num += 1 
        print('Number of Request: ', num)
        if res:
            print('Request Processed Successfully!')
            print("Addition Result: ", res)
            print()
        time.sleep(wait_time)



if __name__ == "__main__":
    main()
