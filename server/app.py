import os
from collections.abc import Iterable
from collections import defaultdict
from sanic import Sanic, response
from dao.user_dao_impl import UserDaoImpl

app = Sanic('Sanic App')
resource_urls = defaultdict(list)


@app.route(uri='/', methods=['GET'])
async def get_main_page(request):
    try:
        main_html_path = ''
        if not os.getcwd().endswith('server'):
            os.chdir('./server')
        for folder in os.listdir('./resources'):
            if folder == 'html':
                main_html_path = os.path.join(".\\resources", folder)
        main_html_path += '\\main.html'
        with open(main_html_path, 'r', encoding='utf8') as html:
            return response.html(html.read())
    except Exception as exce:
        return response.html(f'<html>{exce}</html>')


@app.route(uri='/', methods=['POST'])
async def submit_user_data(request):
    user = UserDaoImpl().create_user(
        request.form['u_name_input_name']
        , request.form['u_name_email_name']
    )
    if user is not None:
        return response.text(
            f'Registered new client:\n name: {user[0]}\n email: {user[1]}')
    else:
        return response.text(f"We could not registered new client")


@app.route(uri='/scraper', methods=['POST'])
async def scraper_page(request):
    file_path = search_in_resource('scraper')
    with open(file_path, 'r', encoding='utf8') as html:
        return response.html(html.read())


async def search_in_resource(object_name):
    folder = []
    for file_structure_object in os.walk('resources'):
        if isinstance(file_structure_object, Iterable):
            folder.append(file_structure_object)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8090, debug=True)
