#!/usr/bin/env python3

from crawler.site_crawler import SiteCrawler


def main():
  # home_url = input('Enter the URL of the site\'s homepage (e.g. http://www.bu.edu/): ')
  home_url = 'https://www.python.org/'

  crawler = SiteCrawler(home_url)
  crawler.crawl()

  print(crawler.sitemap)
  crawler.sitemap.write_to_file('sitemap.csv')

if __name__ == '__main__':
  main()
