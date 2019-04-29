from queue import SimpleQueue

from .sitemap import Sitemap
from .page import Page


class SiteCrawler:
  def __init__(self, home_url):
    home_page = Page(home_url)

    self.sitemap = Sitemap(home_page)
    self._page_queue = SimpleQueue()

    self._page_queue.put(home_page)

  def crawl(self):
    while not self._page_queue.empty():
      self._crawl_page(self._page_queue.get())

  def _crawl_page(self, page):
    for linked_page in page.get_linked_pages_in_domain():
      if linked_page not in self.sitemap:
        self._page_queue.put(linked_page)
      self.sitemap.increment_page_references(linked_page)
