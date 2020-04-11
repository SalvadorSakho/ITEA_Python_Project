from server.server_utils.server_ini import app, db
from sanic import response
from models.Client import User
import os


@app.get(uri='/')
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


@app.post(uri='/')
async def submit_user_data(request):
    name = request.form['u_name_input_name'][0]
    email = request.form['u_name_email_name'][0]
    await db.set_bind(app.config['CONNECTION_STR'])
    await User.create(name=name, email=email)
    return response.text(await User.query.gino.all())


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8090)
