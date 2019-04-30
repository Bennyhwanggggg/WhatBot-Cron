"""
    This is a worker cron job that is used to keep WhatBot's backend awake
"""
import requests
import time
import numpy as np
import datetime
from data_tool.data_source import *
from database.DataBaseManager import DataBaseManager


class DataTool:
    def __init__(self, database_manager=DataBaseManager()):
        self.database_manager = database_manager

    def get_random_index(self, n=6):
        probs = np.random.dirichlet(np.ones(n), size=1)
        return np.random.choice(np.arange(0, n), p=probs[0])

    def get_random_amp(self):
        return random.choice(range(-5, 5)) / 100

    def start(self, n_timeslot=10000):
        for i in range(n_timeslot):
            ts = datetime.datetime.now() - datetime.timedelta(seconds=i * 42)
            idx = self.get_random_index()
            intent = intent_list[idx][0]
            template_sentence_list = intent_list[idx][1]
            base_confidence = intent_list[idx][2]
            confidence = base_confidence + self.get_random_amp()
            course_name = random.choice(course_list)[0]
            query_text = random.choice(template_sentence_list).format(course_code=course_name)
            self.add_intent_data(intent, query_text, confidence, str(ts))

    def add_intent_data(self, intent, query_text, confidence, timestamp=datetime.datetime.now()):
        """Collect user data and upload it to database

        :param intent: intent that the user triggered
        :type: str
        :param query_text: user's query text
        :type: str
        :param confidence: the confidence level from Dialogflow
        :type: float
        :param: timestamp: timestamp when the query is entered
        :type: datetime
        :return: query execution status
        :rtype: str
        """
        query = "INSERT INTO intent_data(intent, query_text, confidence, timestamp) VALUES (%s, %s, %s, %s)"
        inputs = (intent, query_text, confidence, timestamp)
        return self.database_manager.execute_query(query, inputs)


def main(url='https://whatbot9900backend.herokuapp.com/'):

    data_tool = DataTool()
    next_day = random.randint(1, 4)

    start_time = time.time()
    while True:
        time_diff = int(time.time() - start_time)
        if not time_diff % 60:
            print('Running...'.format(time_diff))
        if not time_diff % (60*29):  # Sends a get request every 29 min
            result = requests.get(url)
            print(result)
        if not time_diff % (60*60*24*next_day):
            print('Time to generate data')
            data_tool.start()
            next_day = random.randint(1, 4)


if __name__ == '__main__':
    main()
