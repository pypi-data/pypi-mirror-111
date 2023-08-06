import re
import json

from .Action import Action
from .utils import X_KEY_VALUE_PATTERN,CIS_RULE_PATTERN
from typing import Dict


class Fixlet(dict):

    def __init__(self, payload):
        self.id = None
        self.category = None
        self.default_action = None
        self.source = None
        self.source_severity = None
        self.source_release_date = None
        self.download_size = None
        self.modication_time = None
        self.request_id = None
        self.scm_batch_id = None
        self.scm_control = None
        self.scm_id = None
        self.scm_metadata = None
        self.scm_os = None
        self.scm_selected = None
        self.scm_sentinel_idref = None
        self.scm_tp_relevance = None
        self.scm_tp_remediation = None
        self.set_value = None
        self.xccdf_benchmark = None
        self.xccdf_profile = None
        self.xccdf_xml = None
        self.type = None

        if payload == "":
            self.boundary_string = ""
            self.name = ""
            self.actions = []
            self.output_file = ""
        else:
            self.boundary_string = re.findall("Content-Type: multipart/related; boundary=\"(.*?)\"", payload)[0]
            result = payload.split(f"--{self.boundary_string}")

            subject = re.findall("Subject: (.*)", payload)
            self.name = subject[0]

            args = re.findall(X_KEY_VALUE_PATTERN, result[0])
            for x, y in args:
                self[x.replace("-", "_").lower()] = y

            # todo: add in cis_id
            if "Content-Type: multipart/related" in payload:
                self.actions = []
                for part in result[1:-1]:  # Start at index 1, we already parsed the metadata and final part is end confirmation
                    """
                    The multipart message will contain additional parts for sub-tasks, be they informational in nature
                    or actions that will execute on the target machine, they will be ordered in this list.
                    """
                    self.actions.append(Action(part))

                output_file = re.findall("\"[a-zA-Z0-9]*\.out\"", payload)
                if output_file:
                    self.output_file = output_file[0]
                else:
                    self.output_file = ""

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Fixlet, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Fixlet, self).__delitem__(key)
        del self.__dict__[key]

    def __hash__(self):
        return hash(frozenset(self.json()))

    def __eq__(self, other):
        try:
            return (self.__hash__()) == (other.__hash__())
        except AttributeError:
            return NotImplemented

    @property
    def rule_id(self):  # todo: maybe alias cis?
        try:
            return re.findall(CIS_RULE_PATTERN, self.xccdf_rule)[0]
        except Exception as e:
            return None

    @property
    def profile(self):  # todo: maybe alias level?
        try:
            return 1 if "Level_2" in self.xccdf_profile else 2
        except Exception as e:
            return None

    @property
    def source_version(self):
        try:
            return re.findall(CIS_RULE_PATTERN, self.source)[0]
        except Exception as e:
            return None

    @property
    def benchmark_version(self):
        try:
            return re.findall(CIS_RULE_PATTERN, self.scm_os)[0]
        except Exception as e:
            return None

    @property  # todo: is this still relevant?
    def is_deploy_and_run_relient(self):
        return True if self.output_file != "" in self.fixlet_scm_tp_remediation else False

    def json(self) -> json:
        """ Outputs the objects contents as a JSON structure
            commit
        """
        payload = {
        }
        for key, value in self.items():
            payload[key] = value

        # Handle any properties we want to add in.
        payload["benchmark_version"] = self.benchmark_version
        payload["source_version"] = self.source_version
        payload["profile"] = self.profile
        payload["rule_id"] = self.rule_id

        return json.dumps(payload)

    def dict(self) -> Dict:
        """ Outputs the objects contents as a JSON structure
            commit
        """

        payload = {
        }
        for key, value in self.items():
            if key == "actions":
                dicted_list = []
                for x in value:
                    dicted_list.append(x)
                payload[key] = dicted_list
            else:
                payload[key] = value

        # Handle any properties we want to add in.
        payload["benchmark_version"] = self.get("benchmark_version", "Can't Find Benchmark Version")
        payload["source_version"] = self.get("source_version", "Can't Find Source Version")
        payload["profile"] = self.get("profile", "Can't Find Profile")
        payload["rule_id"] = self.get("rule_id", "Can't Find Rule ID")
        return payload

    @classmethod
    def from_json(cls, json_payload):
        del json_payload["_id"]  # mongo related.
        fixlet = Fixlet("")
        for x, y in json_payload.items():
            fixlet[x] = y

        return fixlet

    def is_functionally_identical(self, other_fixlet):
        """
        Functional changes seem to be concentrated in certain fixlets.
        Namely:

        So this function specifically compares these and checks these 6 fields
        todo: add in actions to this.
        :return:
        """
        functional_fields = ["id", "category", "source", "scm_tp_relevance", "scm_tp_remediation","output_file"]
        diffs = []
        for attribute in functional_fields:
            if self.get(attribute) != other_fixlet.get(attribute):
                diffs.append(attribute)
            else:
                 pass
        return diffs

    def bes(self):  # todo: This would be a very useful feature.
        pass

    def __repr__(self):
        return f"{self.id}"
