from sanic import response
from server_utils.server_ini import app
from server_utils.files_services.files_handler import search_in_resource


@app.route(uri='/scraper_services', methods=['POST'])
async def scraper_page(request):
    file_path = search_in_resource('scraper_services')
    with open(file_path, 'r', encoding='utf8') as html:
        return response.html(html.read())
