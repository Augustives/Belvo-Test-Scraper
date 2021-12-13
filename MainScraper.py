import asyncio
import aiohttp
import json
from datetime import datetime

from scrapers.TheVergeScraper import TheVergeScraper
from scrapers.GizmodoScraper import GizmodoScraper
from scrapers.PhoronixScraper import PhoronixScraper
from scrapers.EngadgetScraper import EngadgetScraper


class MainScraper():
    def __init__(self):
        self.create_scrapers()

    def create_scrapers(self):
        self.scrapers = []
        self.scrapers.append(TheVergeScraper())
        self.scrapers.append(GizmodoScraper())
        self.scrapers.append(PhoronixScraper())
        self.scrapers.append(EngadgetScraper())

    def fetch_html_tasks(self, session):
        tasks = []
        for scraper in self.scrapers:
            tasks.append(scraper.fetch_task(session, scraper.URL))
        return tasks

    def extract_feed_url_tasks(self, html_data):
        for i in range(len(self.scrapers)):
            self.scrapers[i].extract_feed_url_task(html_data[i])

    def fetch_feed_tasks(self, session):
        tasks = []
        for scraper in self.scrapers:
            tasks.append(scraper.fetch_task(session, scraper.feed_url))
        return tasks

    def parse_feed_data_tasks(self, feed_data):
        parsed_feed_data = []
        for i in range(len(self.scrapers)):
            parsed_feed_data.extend(
                self.scrapers[i].parse_feed_data_task(feed_data[i]))
        return sorted(
            parsed_feed_data,
            key=lambda x: datetime.strptime(x['publish_date'], "Date=%m-%d-%Y  Hour=%H:%M:%S  Time Zone=%Z%z"),
            reverse=True)

    def write_to_json(self, parsed_feed_data):
        with open('./json/feed_json.json', 'w') as archive:
            json.dump(parsed_feed_data, archive,  indent=4)
            
    async def scraping_routine(self):
        async with aiohttp.ClientSession() as session:
            html_data = await asyncio.gather(*self.fetch_html_tasks(session))
            self.extract_feed_url_tasks(html_data)
            feed_data = await asyncio.gather(*self.fetch_feed_tasks(session))
            parsed_feed_data = self.parse_feed_data_tasks(feed_data)
            self.write_to_json(parsed_feed_data)

    def run(self):
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.scraping_routine())


if __name__ == '__main__':
    scraper = MainScraper()
    scraper.run()