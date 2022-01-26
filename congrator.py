import json
from datetime import datetime


FORMAT = "%m/%d/%Y"


class Congrator:
    def __init__(self):
        self.children = json.load(open("data/children.json"))
        self.templates = json.load(open("data/templates.json"))
        self.template_count = len(self.templates)
        self.index = -1

    @staticmethod
    def to_date(s: str):
        return datetime.strptime(s, FORMAT)

    def build_message(self, s) -> str:
        if s.get("type") == "holiday":
            return f"Сегодня {s.get('name')}! С чем вас и поздравляю!"
        self.index += 1
        return self.templates[self.index % self.template_count].get("message").replace("@NAME", s.get("name"))

    def get_messages(self) -> list:
        today = datetime.now()
        b_days = [child for child in self.children if
                  self.to_date(child.get("date")).month == today.month and
                  self.to_date(child.get("date")).day == today.day]
        return [self.build_message(child) for child in b_days]

    def reload(self):
        self.children = json.load(open("data/children.json"))
        self.templates = json.load(open("data/templates.json"))
        self.template_count = len(self.templates)
        