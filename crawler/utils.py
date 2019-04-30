from requests import get, head
from urllib.parse import urlparse, urljoin, urlunparse

REQUEST_TIMEOUT_SECONDS = 10


def get_url_contents(url):
  print(f'GET({url})')
  return get(url, timeout=REQUEST_TIMEOUT_SECONDS).text


def get_content_type(url):
  response = head(url, timeout=REQUEST_TIMEOUT_SECONDS, allow_redirects=True)
  return response.headers.get('content-type')


def normalize_url(url, include_scheme=True):
  parsed = urlparse(url)
  parsed = parsed._replace(fragment='')
  parsed = parsed._replace(path=parsed.path.rstrip('/').rstrip('\\'))
  if not include_scheme:
    parsed = parsed._replace(scheme='')
  return urlunparse(parsed)


def get_absolute_url(base_url, href):
  if urlparse(href).netloc:
    return href
  else:
    return urljoin(base_url, href)


def share_domain(a, b):
  return urlparse(a).netloc == urlparse(b).netloc


def is_mailto_or_tel(href):
  return href.startswith('tel:') or href.startswith('mailto:')
