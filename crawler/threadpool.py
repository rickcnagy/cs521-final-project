from threading import Thread

class Threadpool:
  def __init__(self, target=None, args=None, thread_count=None):
    self._target = target
    self._args = args
    self._thread_count = thread_count
    self._threads = set()
    self.running = False

  def start(self):
    self.running = True
    for _ in range(self._thread_count):
      thread = Thread(target=self._target, args=self._args)
      thread.start()
      self._threads.add(thread)

  def stop(self):
    for thread in self._threads:
      thread.join()
    self.running = False
