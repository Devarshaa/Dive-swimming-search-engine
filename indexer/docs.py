import json


class Docs:
    def __init__(self, id, title, url, meta_info, anchor, rank):
        self.id = id
        self.title = title
        self.url = url
        self.meta_info = meta_info
        self.anchor = anchor
        self.rank = rank

    def to_json(self):
        return self.__dict__

    def __str__(self):
        return json.dumps(self, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()
