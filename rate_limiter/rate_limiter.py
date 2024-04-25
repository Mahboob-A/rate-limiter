from array import array
from datetime import datetime, time, timedelta

class RateLimiter: 
    '''
        Rate Limiter class. Custom implementation of TokenBucket algorithm. 
        
        The rate limiter allows at most predefined number of requests to the API interface to access the Calculator class.
        
        All the exceeding requests are throttled. 
        '''
    #  refil_rate_time_in_minutes - after this timeframe, the bucket will be auto reset.
    def __init__(self, token_size=5, refill_rate_time_in_minutes=1):
        self.__token_size = token_size
        self.__bucket = [1] * token_size
        self.__refill_rate_time_in_minutes = refill_rate_time_in_minutes 
        self.__next_refill_time = self._get_time(next_refill_time=True)
        self.__refill_time_counter = self.__refill_rate_time_in_minutes # to show correct wait time during throttling

    def print_current_time(self): 
        now = self._get_time(with_seconds=True)
        now = now.strftime("%I:%M:%S %p")
        print('Request Time: ', now)

    def _get_time(self, next_refill_time=False, with_seconds=False):
        """ returns the current or exactly next minute datetime object as the format: 12:01:00 """
        # now = 19:40:00
        now = datetime.now()

        # hour:minute:second format. this is the future time when the bucket will refill again.
        # if current time- 19:40:10 then next refil time will be if refil rate is 1 minute:  19:41:00
        if next_refill_time:
            now = now + timedelta(minutes=self.__refill_rate_time_in_minutes)
            now = now.replace(second=0, microsecond=0)
            return now 
        # to calculate wait seconds in throttling
        elif with_seconds:
            return now  

        # else return current time without second: ex 19:40:00
        now = now.replace(second=0, microsecond=0)
        return now 

    def total_token_in_bucket(self):
        ''' return the current length of bucket '''
        return len(self.__bucket)

    def _proceed_request(self):
        """pop a token from bucket and proceed the request."""
        self.__bucket.pop()
        return True

    def _throttle_request(self): 
        ''' bucket does not have enough token. drop the request. '''
        now = self._get_time(with_seconds=True)

        if now.second == 00: 
            self.__refill_time_counter -= 1
            seconds_to_wait = self.__refill_time_counter * 60 - now.second
        else:
            seconds_to_wait = self.__refill_time_counter * 60 - now.second
        print(
            "# Your request has been throttled!\nPlease wait {0} seconds to make another request.\n".format(
                 seconds_to_wait
            )
        )
        return False 

    def _should_refill(self):
        """Returns True if the current time exceeds the next beginning time for the first time"""
        now = self._get_time()
        # print('self.__next: ', self.__next_minute)
        # print('now: ', now)
        if self.__next_refill_time == now:
            #  update next refill time and refil counter
            self.__next_refill_time = self._get_time(next_refill_time=True)
            self.__refill_time_counter = self.__refill_rate_time_in_minutes
            print('***BUCKET RESET***.')
            return True
        else: 
            return False 

    def _refill_bucket(self):
        """ if the time is fresh minute start ex (12:10:00), then reset the bucket with token size. """
        if self._should_refill(): 
            del self.__bucket 
            self.__bucket = [1] * self.__token_size

    def __manager(self):
        """main entrypoint of the rate limiting logic."""
        self.print_current_time()

        # check if bucket should be reset for beginning new minute.
        self._refill_bucket()

        curr_total_token = self.total_token_in_bucket()
        if curr_total_token >= 1:
            return self._proceed_request()
        else: 
            self._refill_bucket()  
            curr_total_token = self.total_token_in_bucket()
            if curr_total_token >= 1: 
                return self._proceed_request()
            else: 
                return self._throttle_request()

    def run(self):
        """main entrypont for the rate limiter from API class."""
        return self.__manager()


if __name__ == '__main__':
        token_size = 5
        limiter = RateLimiter(token_size=token_size)
