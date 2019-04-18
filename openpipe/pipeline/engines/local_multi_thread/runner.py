import threading
from queue import Queue


class SegmentRunner(threading.Thread):

    def __init__(self, segment_name, thread_number, input_queue):
        threading.Thread.__init__(self, segment_name)
        self.input_queue = input_queue
        self.control_in = Queue()

    def start(self):
        self.control_in.get()
