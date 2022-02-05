from core.entity.bookmark import Bookmark


class Comment(Bookmark):

    @property
    def content(self):
        return self._record['content']
