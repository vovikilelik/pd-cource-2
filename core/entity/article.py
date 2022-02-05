from core.entity.entity import Entity


class Article(Entity):

    @property
    def id(self):
        return self._record['id']

    @property
    def user_id(self):
        return self._record['user_id']

    @property
    def title(self):
        return self._record.get('title', 'Без названия')

    @property
    def pic(self):
        return self._record['pic']

    @property
    def content(self):
        return self._record['content']

    @property
    def views_count(self):
        return self._record['views_count']

    @property
    def likes_count(self):
        return self._record['likes_count']
