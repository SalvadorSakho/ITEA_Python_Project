from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.resources.creds import pg_connection as conn


class SessionFactory:
    def __init__(self, db_name):
        user = conn.PG_DB_USER
        password = conn.PG_DB_PASS
        self.engine = create_engine(
            f'postgresql://{user}:{password}@localhost:5432/{db_name}',
            convert_unicode=True,
        )

    def get_session(self):
        try:
            session = sessionmaker(autocommit=False,
                                   autoflush=False,
                                   bind=self.engine)
            session.configure()
            return session()
        except Exception as exeption:
            print(exeption)
