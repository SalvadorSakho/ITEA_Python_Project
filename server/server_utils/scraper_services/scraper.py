import asyncio
import os
import re
import sys

import aiofiles
from aiohttp import ClientSession
from tqdm import tqdm


class Scraper:
    def __init__(self):
        self.HTML_PATH = '_tml/'

    async def weg_requester(self, url, html_name, session, encoding='utf-8',
                            batch_size=1000,
                            compression='BROTLI'):
        async with session.get(url) as response:
            text = await response.read()
            async with aiofiles.open(f'_tmp/{html_name}', 'wb') as f:
                await f.write(text)
            print(url)

    async def scrap(self, url, progress, loop, incorrect_urls=[]):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|'
            r'[A-Z0-9-]{2,}\.?)|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        if re.match(regex, url) is not None:
            if not os.path.exists("_tmp"):
                os.makedirs("_tmp")
            headers = {
                'User-Agent':
                    'Mozilla'
                    '/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit'
                    '/605.1.15 (KHTML, like Gecko) Version'
                    '/12.1.1 Safari/605.1.15',
            }
            async with ClientSession(headers=headers, loop=loop) as session:
                await self.weg_requester(url, str(url).split("/")[-1], session)
        else:
            incorrect_urls.append(url)
        progress.update(1)


def main():
    scraper = Scraper()
    my_list = []
    my_list.append('https://europa.eu')
    my_list.append('https://en.wikipedia.org')
    my_list.append('https://bbc.com')
    my_list.append('https://www.yahoo.com')
    my_list.append('https://w3.org')
    my_list.append('https://policies.google.com')
    my_list.append('https://gstatic.com')
    my_list.append('https://forbes.com')
    my_list.append('https://change.org')
    my_list.append('https://time.com')
    my_list.append('https://wired.com')
    my_list.append('https://who.int')
    my_list.append('https://pinterest.com')

    progress = tqdm(total=len(my_list),
                    file=sys.stdout, disable=False)
    loop = asyncio.get_event_loop()
    tasks = [scraper.scrap(url, progress) for url in my_list]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    main()
