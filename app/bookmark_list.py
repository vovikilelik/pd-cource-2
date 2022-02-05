from functools import reduce

from core.database import Database, element_comparator
from core.entity.bookmark import Bookmark


def generate_id(bookmarks):
    return reduce(lambda acc, item: item['id'] if item['id'] > acc else acc, bookmarks, 0) + 1


class BookmarkList(Database):

    def search_record(self, comparator=element_comparator, **args):
        record = Database.search_record(self, comparator=comparator, **args)

        if record is not None:
            return Bookmark(record)

    def search_records(self, comparator=element_comparator, limit=None, **args):
        records = Database.search_records(self, comparator=comparator, limit=limit, **args)

        return [Bookmark(record) for record in records]

    def add(self, user_id, article_id):
        bookmark = {'id': generate_id(self.data), 'user_id': user_id, 'article_id': article_id}
        self.data.append(bookmark)

        return True

    def switch(self, user_id, article_id):
        existed = len(self.search_records(user_id=user_id, article_id=article_id)) > 0

        if existed:
            return self.remove(user_id=user_id, article_id=article_id)
        else:
            return self.add(user_id, article_id)

    def filter_by_article(self, article_id):
        return self.search_records(article_id=article_id)
