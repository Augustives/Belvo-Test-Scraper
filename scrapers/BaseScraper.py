from abc import ABC, abstractmethod
import asyncio
from re import A


class BaseScraper(ABC):
    @abstractmethod
    def parse_feed_data(self, xml):
        pass

    def parse_feed_data_task(self, xml):
        return self.parse_feed_data(xml)

    @abstractmethod
    def extract_feed_url(self, html):
        pass

    def extract_feed_url_task(self, html):
        return self.extract_feed_url(html)

    async def fetch(self, session, url):
        async with session.get(url) as response:
            text = await response.text()
            return text
    
    def fetch_task(self, session, url):
        return asyncio.create_task(self.fetch(session, url))
