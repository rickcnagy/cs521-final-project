from requests import get


def get_url_contents(url):
  print(f'DEBUG: get({url})')
  return get(url).text
