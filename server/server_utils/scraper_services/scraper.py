import asyncio
import re
import sys
import aiofiles
from aiohttp import ClientSession
from tqdm import tqdm
from server.server_utils.server_ini import SCRAPDIR, regex
from server_utils.files_services.files_handler import create_folder


class Scraper:
    def __init__(self, user_id, urls_list, response):
        self.incorrect_urls = []
        self.user_id = user_id
        self.urls_list = urls_list
        self.HTMLS_Path = f'{SCRAPDIR}/{self.user_id}'
        self.response = response
        self.header = {
            'User-Agent':
                'Mozilla'
                '/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit'
                '/605.1.15 (KHTML, like Gecko) Version'
                '/12.1.1 Safari/605.1.15',
        }

    async def weg_requester(self, url, session):
        async with session.get(url) as response:
            file_name = str(url).split("/")[-1] \
                if str(url).split("/")[-1].find(".html") != -1 \
                else str(url).split("/")[-1] + ".html"
            text = await response.read()
            async with aiofiles.open(
                    f'{self.HTMLS_Path}/{file_name}', 'wb'
            ) as f:
                await f.write(text)

    async def scrap(self):
        async with ClientSession(headers=self.header) as session:
            for url in self.urls_list:
                if re.match(regex, url) is not None:
                    await create_folder(self.HTMLS_Path)
                    await self.weg_requester(url, session)
                else:
                    self.incorrect_urls.append(url)
        return self.incorrect_urls
