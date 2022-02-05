from core.entity.entity import Entity


class User(Entity):

    @property
    def id(self):
        return self._record['id']

    @property
    def username(self):
        return self._record['username']

    @property
    def avatar(self):
        return self._record['avatar']
