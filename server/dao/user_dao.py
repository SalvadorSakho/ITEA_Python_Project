from abc import ABC, abstractmethod


class UserDao(ABC):

    @abstractmethod
    def create_user(self, name, email):
        pass

    @abstractmethod
    def get_user_by_email(self, email):
        pass
