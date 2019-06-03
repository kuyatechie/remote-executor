import json


class Deserializer(object):
    def __init__(self, dump):
        self.dump = dump

    @staticmethod
    def deserialize(dump):
        return json.loads(dump)

    def get_message(self):
        message = self.deserialize(self.dump)
        return message
