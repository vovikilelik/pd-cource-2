from core.json_source import JsonSource


def strict_equals(source, search):
    return source == search


def element_comparator(record, is_equals=strict_equals, **args):
    """
    Функция сравнения элементов
    :param record: входящий элемент
    :param is_equals: функция сравнения по полю
    :param args: список аргументов для сравнения
    :return: boolean
    """
    for key, value in args.items():
        if key not in record or not is_equals(record.get(key), value):
            return False

    return True


class Database(JsonSource):

    def search_records(self, comparator=element_comparator, limit=None, set_direction=True, **args):
        result = []

        for record in self.data:
            if limit is not None and limit <= len(result):
                break

            if comparator(record, **args) == set_direction:
                result.append(record)

        return result

    def search_record(self, comparator=element_comparator, **args):
        records = Database.search_records(self, comparator=comparator, limit=1, **args)
        return records[0] if len(records) > 0 else None

    def remove(self, comparator=element_comparator, **args):
        prev_data = self.data
        self.data = Database.search_records(self, set_direction=False, comparator=comparator, **args)

        return len(prev_data) != len(self.data)
