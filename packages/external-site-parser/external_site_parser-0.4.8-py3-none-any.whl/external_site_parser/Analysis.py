import re

from .Action import Action
from .utils import X_KEY_VALUE_PATTERN


class Analysis(dict):

    def __init__(self, payload):
        """
        Working off the dangerous assumption that the payload file key-value pairs will always be in the format
        [X|x]-key-name: value, where the value is everything until EOL
        We can try and generate and populate instance variables automatically.

        :param payload:
        :return:
        """
        if payload == "":
            self.name = ""
            self.boundary_string = ""
            self.actions = []
        else:

            subject = re.findall("Subject: (.*)", payload)
            self.name = subject[0]

            args = re.findall(X_KEY_VALUE_PATTERN, payload)
            for x, y in args:
                self[x.replace("-", "_").lower()] = y

            if "Content-Type: multipart/related" in payload:
                self.boundary_string = re.findall("Content-Type: multipart/related; boundary=\"(.*?)\"", payload)[0]
                result = payload.split(f"--{self.boundary_string}")
                self.actions = []
                for part in result[1:-1]:  # Start at index 1, we already parsed the metadata and final part is end confirmation
                    """
                    The multipart message will contain additional parts for sub-tasks, be they informational in nature
                    or actions that will execute on the target machine, they will be ordered in this list.
                    """
                    self.actions.append(Action(part))

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Analysis, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Analysis, self).__delitem__(key)
        del self.__dict__[key]

    def __hash__(self):
        return hash(frozenset(self.json()))

    def __eq__(self, other):
        try:
            return (self.__hash__()) == (other.__hash__())
        except AttributeError:
            return NotImplemented

    def json(self):
        """ Outputs the objects contents as a JSON structure
            commit
        """
        payload = {
        }
        for key, value in self.items():
            payload[key] = value
        return payload

    def __repr__(self):
        return f"{self.name} has {len(self.actions)} actions"

    @classmethod
    def from_json(cls, json_payload):
        del json_payload["_id"]  # mongo related.
        analysis = Analysis("")
        for x, y in json_payload.items():
            analysis[x] = y

        return analysis
