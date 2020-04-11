from gino.ext.sanic import Gino
from sanic import Sanic
from server.resources.creds import pg_connection as conn

app = Sanic('Sanic App')
app.config.DB_USER = conn.PG_DB_USER
app.config.DB_PASS = conn.PG_DB_PASS
app.config.DB_NAME = conn.PG_DB_DBNAME
app.config.CONNECTION_STR = f'postgresql://{conn.PG_DB_USER}' \
                            f':{conn.PG_DB_PASS}@localhost:5432/' \
                            f'{conn.PG_DB_DBNAME}'
db = Gino()

