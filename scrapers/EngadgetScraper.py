from bs4 import BeautifulSoup
from datetime import datetime
from scrapers.BaseScraper import BaseScraper


class EngadgetScraper(BaseScraper):
    URL = 'https://www.engadget.com'

    def __repr__(self):
        return f'{self.URL}'

    def extract_feed_url(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        rss_urls = soup.find_all(type="application/rss+xml")
        self.feed_url = f'https:{rss_urls[0].get("href")}'

    def parse_feed_data(self, xml):
        parsed_data = []
        soup = BeautifulSoup(xml, 'xml')
        entrys = soup.find_all('item')
        for entry in entrys[:10]:
            parsed_data.append({
                'title': entry.find('title').text,
                'publish_date': self.parse_publish_date(entry.find('pubDate').text),
                'link': entry.find('link').text
                })
        return parsed_data

    def parse_publish_date(self, publish_date: str):
        dt = datetime.strptime(publish_date, "%a, %d %b %Y %H:%M:%S %z")
        tz = dt.tzname()
        if ':' not in dt.tzname():
            tz = f'{dt.tzname()}-00:00'
        return dt.strftime(f"Date=%m-%d-%Y  Hour=%H:%M:%S  Time Zone={tz}")