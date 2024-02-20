from queue import Queue
import time


class QueueSpeak:
    def __init__(self, sysGlobals) -> Queue:
        self.queue = Queue()
        self.sysGlobals = sysGlobals

    def awaitQueue(self) -> None:
        while True:
            try:
                if not self.sysGlobals["isSpeaking"].is_set():
                    if self.queue.empty():
                        return None
            except:
                pass

    def putWait(self, item) -> None:
        self.queue.put(item)
        time.sleep(1)
        self.awaitQueue()
    