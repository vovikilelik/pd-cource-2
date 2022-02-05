import json


class JsonSource:

    def __init__(self, default_data=None):
        self.data = default_data
        self._file_name = None

    def load_from_file(self, file_name):
        self._file_name = file_name
        with open(file_name, encoding='utf-8') as f:
            self.data = json.load(f)

    def save_to_file(self, file_name=None):
        path = file_name if file_name is not None else self.file_name
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False)

    @property
    def file_name(self):
        return self._file_name

