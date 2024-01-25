import threading


class SafePrint:
    _lock = threading.Lock()

    @classmethod
    def print(cls, text):
        with cls._lock:
            print(text)
