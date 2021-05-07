import threading


class Counter(object):

    def __init__(self, value=0):
        self.val = value
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.val += 1

    def decrement(self):
        with self.lock:
            self.val -= 1

    def value(self):
        with self.lock:
            return self.val


