from bs4 import BeautifulSoup

from .utils import get_url_contents, get_content_type, normalize_url, get_absolute_url, share_domain, is_mailto_or_tel

class Page:
  def __init__(self, absolute_url):
    self.url = normalize_url(absolute_url, include_scheme=True)
    self.schemeless_url = normalize_url(absolute_url, include_scheme=False)
    self._content_type = None
    self._contents = None

  def get_linked_pages_in_domain(self):
    return set(
      Page(url)
      for url in self._get_linked_urls()
      if share_domain(self.url, url)
    )

  def _get_linked_urls(self):
    if not self._is_crawlable(): return set()

    html = self._get_contents()
    dom = BeautifulSoup(html, 'html.parser')

    return set(
      get_absolute_url(self.url, anchor.get('href'))
      for anchor in dom.find_all('a')
      if anchor.get('href') and not is_mailto_or_tel(anchor.get('href'))
    )

  def _get_contents(self):
    if self._contents is None:
      self._contents = get_url_contents(self.url)
    return self._contents

  def _is_crawlable(self):
    if self._content_type is None:
      self._content_type = get_content_type(self.url)
    return self._content_type and self._content_type.startswith('text/html')

  def __hash__(self):
    return hash(self.schemeless_url)

  def __eq__(self, other):
    return self.schemeless_url == other.schemeless_url

  def __str__(self):
    return self.url
