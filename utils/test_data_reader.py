import json


class TestDataReader:
    @staticmethod
    def read_json(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)