import threading


class Counter:
    def __init__(self, value):
        self.value = value
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

    def decrement(self):
        with self.lock:
            self.value = max(0, self.value - 1)

    def get_value(self):
        with self.lock:
            return self.value


class Text:
    def __init__(self, value, size=4):
        self.value = value
        self.size = size
        self.lock = threading.Lock()

    def append(self, key):
        with self.lock:
            if len(self.value) == self.size:
                self.value = key
            else:
                self.value += key

    def get_value(self):
        with self.lock:
            return self.value
