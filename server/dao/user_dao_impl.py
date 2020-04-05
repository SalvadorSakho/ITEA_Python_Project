from sqlalchemy import select

from dao.user_dao import UserDao
from entities.Client import User
from server_utils.DB_handler import SessionFactory
from server.resources.creds import pg_connection as conn


class UserDaoImpl(UserDao):

    def __init__(self):
        self.session = SessionFactory(conn.PG_DB_DBNAME).get_session()

    def create_user(self, name, email):
        new_client = User(name[0], email[0])
        try:
            self.session.add(new_client)
            self.session.commit()
            return self.get_user_by_email(email)
        except Exception as exce:
            print(exce)
            self.session.rollback()

    def get_user_by_email(self, email):
        sql_statement = select([User.name, User.email]) \
            .where(User.email == email[0])
        result_set = self.session.execute(sql_statement)
        for data in result_set:
            return data
