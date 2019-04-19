"""
    This is a worker cron job that is used to keep WhatBot's backend awake
"""
import requests
import time


def main(url='https://whatbot9900backend.herokuapp.com/'):

    start_time = time.time()
    while True:
        time_diff = int(time.time() - start_time)
        if not time_diff % 60:
            print('Running...'.format(time_diff))
        if not time_diff % (60*29):  # Sends a get request every 29 min
            result = requests.get(url)
            print(result)


if __name__ == '__main__':
    main()
