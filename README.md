
# Rate Limiter 

This is an pythonic example of TokenBucket algorithm to implement rate limiter. 



## General Information

A rate limiter is a crucial component in software application when the resources are exposed to outside world and the stakeholders want to control how the resources are being manipulated. 

A rate limiter can be implemented to prevent any DoS or DDoS attack from malicious parties. Dos attack is continious demand of computing resources making evenly resouce distribution impossible and room for resource starvation. 

A rate limiter is also often implemented when the stakeholders want to limit the number of requests permitted to evenly distribute the computing resources to all the parties. 



## Documentation


### Input Style - Terminal 

The bucket size i.e. the total tokens in the bucket. 
```
token_size 
```

Frequency after how many minutes the bucket will be auto reset. 
```
refill_rate_time_in_minutes
```

How many seconds to wait for the next request to the api. 
```
seconds_to_wait_to_simulate_request
```
## Code Structure 

The main interface to the resource - a calculator 
```
api.py 
```

The logic to limit the request frequency to the 
api to access the calculator 
```
rate_limiter.py
```

The resource to share through the api - functionalities of a calculator 
```
calculator.py
```
## Run Locally

Clone the project

```bash
  https://github.com/Mahboob-A/rate-limiter.git
```

Go to the project directory

```bash
  cd rate_limiter
```

Start the server


* for Linux/MacOS

```bash
    python3 api.py 
```

* for windows 
```bash
    python api.py 
```
## FAQ

#### Which algorithm has been implemented in the rate limier

TokenBucket Algorithm

#### Language

Python 


## Screenshots

#### API startup and Acceptance of requests 
![Screenshot from 2024-04-25 11-09-42](https://github.com/Mahboob-A/rate-limiter/assets/109282492/1a2ff81d-0946-4746-9a16-400b6ae46612)

##### Request throttled and Bucket reset after refil time
![Screenshot from 2024-04-25 11-10-33](https://github.com/Mahboob-A/rate-limiter/assets/109282492/97094752-fd9f-4ca5-a743-0642bcfc9f9c)
## Optimizations

The tokenbucket algorithm implemented here is slightly different than the standard how it is done. 

I have customized it while analyzing the requirements. 
