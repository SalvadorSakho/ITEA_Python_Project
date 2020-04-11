import asyncio
import sys
import os
from server.server_utils.server_ini import server_app, db
from sanic import response
from models.Client import User
from server_utils.files_services.files_handler import search_in_static
from server_utils.scraper_services.scraper import Scraper
from tqdm import tqdm


@server_app.get(uri='/')
async def get_main_page(request):
    try:
        if not os.getcwd().endswith('server'):
            os.chdir('./server')
        main_page = server_app.url_for(
            'static', filename='/html/main.html'
        )
        return response.redirect(main_page)
    except Exception as exce:
        return response.html(f'<html>{exce}</html>')


@server_app.get(uri='/static/html/main.html')
async def get_main_page(request):
    try:
        scraper_page_path = await search_in_static('main.html')
        with open(scraper_page_path, 'r') as scraper_html:
            return response.html(scraper_html.read())
    except Exception as exce:
        return response.html(f'<html>{exce}</html>')


@server_app.post(uri='/static/html/main.html')
async def submit_user_data(request):
    name = request.form['u_name_input_name'][0]
    email = request.form['u_name_email_name'][0]
    await db.set_bind(server_app.config['CONNECTION_STR'])
    await User.create(name=name, email=email)
    scraper_page = server_app.url_for(
        'static', filename='/html/scraper.html'
    )
    return response.redirect(scraper_page)


@server_app.get(uri='/static/html/scraper.html')
async def scraper_page(request):
    scraper_page_path = await search_in_static('scraper.html')
    with open(scraper_page_path, 'r') as scraper_html:
        return response.html(scraper_html.read())


@server_app.post(uri='/static/html/scraper.html')
async def scraper_page(request):
    scraper = Scraper()
    progress = tqdm(total=len(request.form['web_page_input_name']),
                    file=sys.stdout, disable=False)

    loop = asyncio.get_event_loop()
    tasks = [
        scraper.scrap(url, progress, loop) for url in
        request.form['web_page_input_name']
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    if len(scraper.incorrect_urls) >= 1:
        return response.text(f'Scraper finished to work.'
                             f'\nWhere detected incorrect urls:'
                             f'\n{[url for url in scraper.incorrect_urls]}')
    else:
        return response.text(f'Scraper finished to work')


if __name__ == '__main__':
    server_app.run(host="127.0.0.1", port=8090)
