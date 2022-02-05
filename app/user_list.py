from core.database import Database, element_comparator
from core.entity.user import User


class UserList(Database):

    def search_record(self, comparator=element_comparator, **args):
        user = Database.search_record(self, comparator=comparator, **args)

        if user is not None:
            return User(user)

    def get_by_id(self, user_id):
        return self.search_record(id=user_id)

    def get_by_username(self, username):
        return self.search_record(username=username)
