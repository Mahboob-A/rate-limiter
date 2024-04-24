from array import array
from datetime import datetime, time, timedelta

class RateLimiter: 
    '''
        Rate Limiter class. Custom implementation of TokenBucket algorithm. 
        
        The rate limiter allows at most predefined number of requests to the API interface to access the Calculator class.
        
        All the exceeding requests are throttled. 
        '''
    def __init__(self, token_size=5):
        self.__token_size = token_size
        self.__bucket = [1] * token_size
        self.__last_request_time = self._get_time(next_minute=False)
        self.__next_minute = self._get_time(next_minute=True)

    def print_current_time(self): 
        now = self._get_time(with_seconds=True)
        now = now.strftime("%I:%M:%S %p")
        print('Request Time: ', now)

    def _get_time(self, next_minute=False, with_seconds=False):
        """ returns the current or exactly next minute datetime object as the format: 12:01:00 """
        # now = 19:40:00
        now = datetime.now()

        # one minute future - 19:41:00
        if next_minute: 
            now = now + timedelta(minutes=1)
            now = now.replace(second=0, microsecond=0)
            return now 
        elif with_seconds:
            # to calculate wait seconds 
            return now  
        # else return 19:40:00
        now = now.replace(second=0, microsecond=0)
        return now 

    def _update_request_time(self):
        """ update the requst time with current time"""
        self.__last_request_time = self._get_time()

    def total_token_in_bucket(self):
        ''' return the current length of bucket '''
        return len(self.__bucket)

    def _refill_token_in_bucket(self):
        ''' refil if request minute are different. bucket is refilled at 12:01:00 each minute. '''
        now = self._get_time()
        if now.minute !=  self.__last_request_time.minute or now.hour != self.__last_request_time.hour: 
            del self.__bucket 
            self.__bucket = [1] * self.__token_size

    def _proceed_request(self):
        """pop a token from bucket and proceed the request."""
        self.__bucket.pop()
        return True

    def _throttle_request(self): 
        ''' bucket does not have enough token. drop the request. '''
        now = self._get_time(with_seconds=True)
        seconds_to_wait = 60 - now.second
        print('Your request has been throttled!\nPlease wait {0} seconds to make another request.\n'.format(seconds_to_wait))
        return False 

    def _should_refil(self):
        """Returns True if the current time exceeds the next beginning minute for the first time"""
        now = self._get_time(next_minute=False)
        # print('self.__next: ', self.__next_minute)
        # print('now: ', now)
        if self.__next_minute == now: 
            self.__next_minute = self._get_time(next_minute=True)
            print('***BUCKET RESET***.')
            return True
        else: 
            return False 
        

    def _refil_bucket_at_minute_beginning(self): 
        """ if the time is fresh minute start (12:10:00), then reset the bucket with token size. """
        if self._should_refil(): 
            del self.__bucket 
            self.__bucket = [1] * self.__token_size


    def __manager(self):
        """main entrypoint of the rate limiting logic."""
        self.print_current_time()

        # check if bucket should be reset for beginning new minute. 
        self._refil_bucket_at_minute_beginning()

        curr_total_token = self.total_token_in_bucket()
        if curr_total_token >= 1:
            self._update_request_time()
            return self._proceed_request()
        else: 
            self._refill_token_in_bucket()
            curr_total_token = self.total_token_in_bucket()
            if curr_total_token >= 1: 
                self._update_request_time()
                return self._proceed_request()
            else: 
                return self._throttle_request()

    def run(self):
        """main entrypont for the rate limiter from API class."""
        return self.__manager()


if __name__ == '__main__':
        token_size = 5
        limiter = RateLimiter(token_size=token_size)
