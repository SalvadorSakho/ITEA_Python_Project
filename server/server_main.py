import os
import random

from server.server_utils.server_ini import server_app, db
from sanic import response
from models.Client import User
from server_utils.files_services.files_handler import search_in_static, \
    compress_descriptions
from server_utils.scraper_services.scraper import Scraper
from server_utils.server_ini import SCRAPDIR

scraper_page = server_app.url_for('static', filename='/html/scraper.html')
main_page = server_app.url_for('static', filename='/html/main.html')


@server_app.get(uri='/')
async def get_main_page(request):
    try:
        if not os.getcwd().endswith('server'):
            os.chdir('./server')
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
    return response.redirect(scraper_page)


@server_app.get(uri='/static/html/scraper.html')
async def scraper_page(request):
    scraper_page_path = await search_in_static('scraper.html')
    with open(scraper_page_path, 'r') as scraper_html:
        return response.html(scraper_html.read())


@server_app.post(uri='/static/html/scraper.html')
async def scraper_page(request):
    # add check if user is unknown
    unknown_user_id = random.randint(100000, 999999)
    scraper = Scraper(
        unknown_user_id
        , request.form['web_page_input_name']
        , response
    )
    try:
        incorrect_urls = await scraper.scrap()
        await compress_descriptions(f'{SCRAPDIR}/{unknown_user_id}')
        u_zip_file = server_app.url_for(
            'return_zip',
            user_id=unknown_user_id
        )
        return response.redirect(u_zip_file)
    except Exception as exc:
        return response.html(f'<html>{exc.with_traceback()}</html>')


@server_app.get(uri='/static/scrapdir/<user_id>.zip')
async def return_zip(request, user_id):
    return response.file(f'{SCRAPDIR}/{user_id}.zip').send(
        response.redirect(main_page))


if __name__ == '__main__':
    server_app.run(host="127.0.0.1", port=8090)
