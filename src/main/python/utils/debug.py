import sys
import time

def pexit(*msg):
    print(msg)
    exit(1)

def pwait(*msg, seconds=5):
    print(msg)
    time.sleep(seconds)




