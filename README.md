# Async Web Scraper

### Description
Using Python async programming, scrape information from 4 differente blogs and websites.
Fetch HTML, extract de RSS or Atom feed URL, fetch the feed, extract title, link and publish date, at last sort the entrys and write a JSON file.

### Technologies
Project is created with:
* Python
* Asyncio
* Aiohttp
* Docker

## Setup
To run this project:

```
docker build . -t belvo-scraper 
docker-compose up -d 
```