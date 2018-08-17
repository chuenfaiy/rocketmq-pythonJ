# -*- coding: utf-8 -*-

import sys
import os
import time
from threading import Thread, Lock
sys.path.append(os.path.split(os.path.realpath(__file__))[0] + '/..')
from pyrmq import *

TOPIC = 'PythonBenchmarkTest'
CONSUMER_GROUP = 'python_benchmark_push_consumer'
NAMESRV = '10.61.2.125:9876'

CONSUME_MESSAGE_TOTAL = 0

def processMessages(messages):
    for msg in messages:
        CONSUME_MESSAGE_TOTAL += 1
    return True

consumer = buildPushConsumer(CONSUMER_GROUP, NAMESRV)
registerListener(consumer, processMessages)
startConsumer(consumer)
print("topic: %s, consumer: %s" % (TOPIC, CONSUMER_GROUP, ))

def sampling():
    global SEND_MESSAGE_TOTAL
    last = 0
    start = time.time()
    stop = 0
    while True:
        time.sleep(1)
        print("consume TPS: %d, total message: %d" % (SEND_MESSAGE_TOTAL - last, SEND_MESSAGE_TOTAL, ))
        last = SEND_MESSAGE_TOTAL

t = Thread(target=sampling)
t.start()
print('sampling thread ' + t.getName() + ' started.\n')

# only one thread to produce message
while True:
    time.sleep(1)
