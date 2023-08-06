import re


class Action(dict):
    """
    NOTE: Actions can also be multipart
    """

    def __init__(self, payload):
        self.content_type = re.findall("Content-Type: (.*)", payload)[0]

        """Some content does not have an id"""
        if self.content_type == "text/html; charset=us-ascii":
            self.content_id = None
            # We still have the content type line and empty line before + after to ignore.
            self.content = "".join(payload.split("\n")[3:-2])

        else:  #
            self.content_id = re.findall("Content-id: (.*)", payload)[0]
            # We still have the content type line and empty line before + after to ignore.
            self.content = "".join(payload.split("\n")[5:-2])

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Action, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Action, self).__delitem__(key)
        del self.__dict__[key]

    def __hash__(self):
        return hash(frozenset(self.json()))

    def __eq__(self, other):
        try:
            return (self.__hash__()) == (other.__hash__())
        except AttributeError:
            return NotImplemented

    def __repr__(self):
        return f""""
                "content_type: {self.content_type},
                "content_id": {self.content_id},
                "content": {self.content}
                """

    def dict(self):
        return {
            "content_type": self.content_type,
            "content_id": self.content_id,
            "content": self.content
        }

    def __debug(self):
        pass
