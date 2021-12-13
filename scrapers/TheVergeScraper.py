from bs4 import BeautifulSoup
from datetime import datetime
from scrapers.BaseScraper import BaseScraper

class TheVergeScraper(BaseScraper):
    URL = 'https://www.theverge.com'

    def __repr__(self):
        return f'{self.URL}'

    def extract_feed_url(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        rss_urls = soup.find_all(type="application/rss+xml")
        self.feed_url = rss_urls[1].get('href')

    def parse_feed_data(self, xml):
        parsed_data = []
        soup = BeautifulSoup(xml, 'xml')
        entrys = soup.find_all('entry')
        for entry in entrys[:10]:
            parsed_data.append({
                'title': entry.find('title').text,
                'publish_date': self.parse_publish_date(entry.find('published').text),
                'link': entry.find('link').get('href')
                })
        return parsed_data

    def parse_publish_date(self, publish_date: str):
        dt = datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%S%z")
        tz = dt.tzname()
        if ':' not in dt.tzname():
            tz = f'{dt.tzname()}-00:00'
        return dt.strftime(f"Date=%m-%d-%Y  Hour=%H:%M:%S  Time Zone={tz}")