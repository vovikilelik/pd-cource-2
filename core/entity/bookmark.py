from core.entity.entity import Entity


class Bookmark(Entity):

    @property
    def id(self):
        return self._record['id']

    @property
    def user_id(self):
        return self._record['user_id']

    @property
    def article_id(self):
        return self._record['article_id']
