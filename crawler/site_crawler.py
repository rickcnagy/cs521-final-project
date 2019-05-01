from queue import Queue
from signal import SIGINT, SIGTERM, signal

from .page import Page
from .sitemap import Sitemap
from .threadpool import Threadpool

WORKER_THREAD_COUNT = 16


def worker(page_queue, sitemap):
  while True:
    page = page_queue.get()
    if page is None:
      break
    _crawl_page(page, page_queue, sitemap)
    page_queue.task_done()


def _crawl_page(page, page_queue, sitemap):
  for linked_page in page.get_linked_pages_in_domain():
    with sitemap.semaphore:
      if linked_page not in sitemap:
        page_queue.put(linked_page)
      sitemap.increment_page_references(linked_page)


class SiteCrawler:
  """Recursively crawls all of the pages on a site.

  Creates a threadpool with WORKER_THREAD_COUNT threads, then uses those workers
  to crawl the site through a standard queue-based crawler model. If sigterm or
  sigint is caught on the main thread, all of the workers are gracefully killed
  and the program exits.

  Attributes:
    sitemap: A Sitemap containing all of the information found so far in the
      crawl.
  """

  def __init__(self, home_url):
    home_page = Page(home_url)

    self.sitemap = Sitemap(home_page)

    self._page_queue = Queue()
    self._page_queue.put(home_page)

    self._threadpool = Threadpool(
      target=worker,
      args=(self._page_queue, self.sitemap),
      thread_count=WORKER_THREAD_COUNT,
    )

    signal(SIGINT, self._caught_signal)
    signal(SIGTERM, self._caught_signal)

  def crawl(self):
    self._threadpool.start()
    self._page_queue.join()
    self._stop_crawl()

  def _caught_signal(self, signum, *args):
    self._stop_crawl()
    exit(signum)

  def _stop_crawl(self):
    print('Stopping...')
    if self._page_queue.empty() and not self._threadpool.running: return

    while not self._page_queue.empty():
      self._page_queue.get()
      self._page_queue.task_done()

    for i in range(WORKER_THREAD_COUNT):
      self._page_queue.put(None)

    self._threadpool.stop()
