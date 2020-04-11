import asyncio

import aiofiles
from aiohttp import ClientSession
import config as cfg
from pip._vendor import progress

from server.server_main import app

HTML_PATH = cfg.BUILDDIR / 'data.parquet'


async def weg_requester(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
    }
    async with ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            text = await response.read()
            async with aiofiles.open(
                    HTML_PATH / f'scrubed_html.html', 'wb'
            ) as f:
                await f.write(text)
            progress.update(1)


@app.post('/server/resources/html/scraper.html')
async def scrap(request):
    loop = asyncio.get_event_loop()
    print(request.form['url_form_name'])
    for data in request.form['url_form_name']:
        loop.run_until_complete(asyncio.ensure_future(weg_requester(data)))
