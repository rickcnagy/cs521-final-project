#!/usr/bin/env python3

from crawler.site_crawler import SiteCrawler
from crawler.utils import is_full_url


def main():
  """Main entrypoint to the crawler program

  Gets the site's homepage URL from user input, crawls the site with
  SiteCrawler, then outputs the pages ranked by importance to TSV.
  """
  home_url = input('Enter the URL of the site\'s homepage (e.g. http://www.bu.edu/): ')

  if not is_full_url(home_url):
    print('Invalid URL: ' + home_url)
    exit()

  crawler = SiteCrawler(home_url)
  crawler.crawl()

  print(crawler.sitemap)
  crawler.sitemap.write_to_file('sitemap.tsv')

if __name__ == '__main__':
  main()
