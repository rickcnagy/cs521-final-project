from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

from .utils import get_url_contents

class Page:
  def __init__(self, url):
    self.url = self._normalize(url)
    self.domain = urlparse(url).netloc
    self._contents = None

  def get_linked_pages_in_domain(self):
    return [
      Page(self._get_absolute_url(href))
      for href in self._get_linked_href_set()
      if self._shares_domain(href)
    ]

  def _get_linked_href_set(self):
    html = self._get_contents()
    dom = BeautifulSoup(html, 'html.parser')
    return set([anchor.get('href') for anchor in dom.find_all('a')])

  def _get_contents(self):
    if not self._contents:
      self._contents = get_url_contents(self.url)
    return self._contents

  def _get_absolute_url(self, href):
    if urlparse(href).netloc:
      return href
    else:
      return urljoin(self.url, href)

  def _shares_domain(self, href):
    parsed_url = urlparse(href)
    return (
      parsed_url.scheme in ['', 'http', 'https'] and
      parsed_url.netloc in ['', self.domain]
    )

  def _normalize(self, url):
    return url.rstrip('/')

  def __hash__(self):
    return hash(self.url)

  def __eq__(self, other):
    return self.url == other.url

  def __str__(self):
    return self.url
