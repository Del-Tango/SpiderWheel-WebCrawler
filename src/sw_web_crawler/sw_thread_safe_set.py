#!/usr/bin/env python3
import threading


class ThreadSafeSet(list):

    def __init__(self):
        self.lock = threading.Lock()
        self._set = set()

    def get(self):
        with self.lock:
            return self._set.pop()

    def put(self, o):
        with self.lock:
            self._set.add(o)

    def get_all(self):
        with self.lock:
            return self._set

    def clear(self):
        with self.lock:
            self._set.clear()
