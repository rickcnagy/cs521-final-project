from threading import Semaphore

class Sitemap:
  def __init__(self, home_page):
    self.semaphore = Semaphore()
    self._page_reference_counts = {}
    self._page_reference_counts[home_page] = 0

  def increment_page_references(self, page):
    if page not in self:
      self._page_reference_counts[page] = 0
    self._page_reference_counts[page] += 1

  def write_to_file(self, filename):
    with open(filename, 'w') as f:
      f.write(str(self))

  def _pages_sorted_by_reference_count(self):
    pages = self._page_reference_counts.keys()
    return sorted(pages, key=lambda page: self._page_reference_counts[page])

  def __str__(self):
    return '\n'.join(
      '\t'.join([page.url, str(self._page_reference_counts[page])])
      for page in self._pages_sorted_by_reference_count()
    )

  def __contains__(self, page):
    return page in self._page_reference_counts
