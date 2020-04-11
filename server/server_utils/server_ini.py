from gino.ext.sanic import Gino
from sanic import Sanic
from server.static.creds import pg_connection as conn

server_app = Sanic('Sanic App')
server_app.config.DB_USER = conn.PG_DB_USER
server_app.config.DB_PASS = conn.PG_DB_PASS
server_app.config.DB_NAME = conn.PG_DB_DBNAME
server_app.config.CONNECTION_STR = f'postgresql://{conn.PG_DB_USER}' \
                                   f':{conn.PG_DB_PASS}@localhost:5432/' \
                                   f'{conn.PG_DB_DBNAME}'
server_app.static('/static', './static')
db = Gino()
