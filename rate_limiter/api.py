from calculator import Calculator
from rate_limiter import RateLimiter
import time


class API:
    """Interface between the Calculator service. Request is limited with a Rate Limiter."""

    def __init__(self, token_size=5, refill_rate_time_in_minutes=1):
        self.__calc = Calculator()
        self.__limiter = RateLimiter(token_size=token_size, refill_rate_time_in_minutes=refill_rate_time_in_minutes)

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
                    "please input the number of request allowed in the api per refill time: "
                )
            )
            refill_rate_time_in_minutes = int(input('frequency when the bucket will be auto reset (in minutes): '))
            seconds_to_wait_to_simulate_request = float(input('seconds to wait to simulate requests: '))
            return (
                token_size,
                refill_rate_time_in_minutes, 
                seconds_to_wait_to_simulate_request
            )
        except ValueError:
            print("number should be integer or float in case of wait_time for request simulation.")


def api_welcome():
    print("\n################################")
    print(
        "Calculator API with Rate Limiter. Custom implementation of TokenBucket Algorithm."
    )
    print(
        "Request are made concurrently. Change wait_time accordingly to simulate request to the API. "
    )
    print(
        "New TokenBucket is available in this time format: 12:01:00 minute i.e. beginning of a minute.\n"
    )
    print('Logic: If the token size is 5, bucket refill rate is 1 minute,\nand total requests made in current minute are 3,\nthen the at the next bucket refill time the bucket will be reset to 5 tokens.')
    print("################################\n")


def main():
    api_welcome()

    token_size, refill_rate_time_in_minutes,  wait_time = input_token_size()

    api = API(token_size=token_size, refill_rate_time_in_minutes=refill_rate_time_in_minutes)
    
    print("\n#######################################\n")
    print('Total Tokens in Bucket: ', token_size)
    print('Frequency to Reset Bucket in Minute: ', refill_rate_time_in_minutes)
    print(f"Request is being made with {wait_time} seconds interval\n")
    print('#######################################\n')
    time.sleep(3)
    
    num = 0
    while 1:
        # for simplicity, sending concurrent add request to the api.
        res = api.add(1, 2, 3)
        num += 1 
        print('Number of Request: ', num)
        if res:
            print('-> Request Processed Successfully!')
            print("Addition Result: ", res)
            print()
        time.sleep(wait_time)


if __name__ == "__main__":
    main()
