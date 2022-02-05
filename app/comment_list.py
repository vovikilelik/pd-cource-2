from app.user_list import UserList
from core.database import Database, element_comparator
from core.entity.comment import Comment
from core.entity.post_comment import PostComment


def get_post_comment_list(comment_list, users: UserList):
    return [PostComment(c.record, users.search_record(id=c.user_id)) for c in comment_list]


class CommentList(Database):

    def search_record(self, comparator=element_comparator, **args):
        record = Database.search_record(self, comparator=comparator, **args)

        if record is not None:
            return Comment(record)

    def search_records(self, comparator=element_comparator, limit=None, **args):
        records = Database.search_records(self, comparator=comparator, limit=limit, **args)

        return [Comment(record) for record in records]
