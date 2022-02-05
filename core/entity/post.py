from core.entity.article import Article
from core.entity.user import User

MAX_PREVIEW_LENGTH = 100


class Post(Article):

    def __init__(self, record, user: User, comments_count=0, views_count=0, bookmarks_count=0):
        Article.__init__(self, record)
        self._user = user
        self._comments_count = comments_count
        self._views_count = views_count
        self._bookmarks_count = bookmarks_count

    @property
    def user(self):
        return self._user

    @property
    def content_preview(self):
        return f'{self.content[:MAX_PREVIEW_LENGTH]}...'

    @property
    def comments_count(self):
        return self._comments_count

    @property
    def views_count(self):
        return self._views_count

    @property
    def bookmarks_count(self):
        return self._bookmarks_count
