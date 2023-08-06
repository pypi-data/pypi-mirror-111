import json
import os


class Credentials:
    def __init__(self, argv):
        for key, val in argv.items():
            self.__dict__[key] = val


    def __repr__(self):
        return f"These are the available keys: {list(self.__dict__.keys())}."


    @classmethod
    def from_json(cls, json_data, filepath=None):
        if filepath:
            header_data = os.path.join(filepath, json_data)
            with open(header_data, 'r') as f:
                key_dict = json.load(f)
                return Credentials(key_dict)
        else:
            with open(json_data, 'r') as f:
                key_dict = json.load(f)
                return Credentials(key_dict)
