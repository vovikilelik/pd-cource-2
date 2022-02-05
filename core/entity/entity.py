class Entity:
    def __init__(self, record):
        self._record = record

    @property
    def record(self):
        return self._record

    def __str__(self):
        return str(self._record)
