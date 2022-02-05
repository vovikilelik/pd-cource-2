from app.bookmark_list import BookmarkList
from app.comment_list import CommentList
from app.user_list import UserList
from core.entity.article import Article
from core.database import Database, element_comparator, strict_equals
from core.entity.bookmark import Bookmark
from core.entity.post import Post


def create_post(article: Article, users: UserList, bookmarks: BookmarkList, comments: CommentList):
    return Post(
        article.record,
        users.get_by_id(article.user_id),
        bookmarks_count=len(bookmarks.search_records(article_id=article.id)),
        comments_count=len(comments.search_records(article_id=article.id))
    )


def array_equals(a, b):
    if type(b) == list:
        return a in b
    else:
        return strict_equals(a, b)


def array_comparator(record, **args):
    return element_comparator(record, is_equals=array_equals, **args)


def query_equals(a, b):
    return str(a).lower().find(str(b).lower()) > -1


def query_comparator(record, **args):
    return element_comparator(record, is_equals=query_equals, **args)


def get_post_list(article_list: list[Article], users: UserList, bookmarks: BookmarkList, comments: CommentList):
    return [create_post(record, users, bookmarks, comments) for record in article_list]


class ArticleList(Database):

    def search_record(self, comparator=element_comparator, **args) -> Article:
        record = Database.search_record(self, comparator=comparator, **args)

        if record is not None:
            return Article(record)

    def search_records(self, comparator=element_comparator, limit=None, **args):
        records = Database.search_records(self, comparator=comparator, limit=limit, **args)

        return [Article(record) for record in records]

    def filter_by_bookmark(self, bookmarks: list[Bookmark], limit=None, **args):
        id_list = [b.article_id for b in bookmarks]
        return self.search_records(comparator=array_comparator, limit=limit, id=id_list, **args)

    def filter_by_query(self, limit=None, content=None, tags=None):
        return self.search_records(comparator=query_comparator, limit=limit, content=content)

    def get_raw_list(self):
        return [Article(record) for record in self.data]
