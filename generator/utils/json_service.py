import json


class JsonHandler:
    def load_json(self, path):
        with open(path) as json_file:
            data = json.load(json_file)
        return data
