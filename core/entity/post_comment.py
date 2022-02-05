from core.entity.comment import Comment
from core.entity.user import User


class PostComment(Comment):

    def __init__(self, record, user: User):
        Comment.__init__(self, record)
        self._user = user

    @property
    def user(self):
        return self._user
