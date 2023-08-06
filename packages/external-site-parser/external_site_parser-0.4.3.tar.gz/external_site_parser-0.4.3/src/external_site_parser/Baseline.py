import re
import logging
from .Task import Task
from .Fixlet import Fixlet
from .Analysis import Analysis
from .utils import BASELINE_CONTENT_TYPE_PATTERN


class Baseline(dict):

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    def __init__(self, payload, *, log_level=logging.INFO, **kwargs):
        """
        :param payload: Takes in a http multtipart payload
        :param unique_id: Optional id for external tracking purposes, since there is nothing in the payload that
        identifies a unique version, timestamp or iteration. Modified dates do not have to be unique.
        """
        logging.getLogger().setLevel(log_level)

        # todo: change this hack, need to get this working for from_json class method
        if payload == "":
            self.mime_version = ""
            self.subject = ""
            self.relevant_when = ""
            self.relevance_evaluation_period = ""
            self.fixlets = {}
            self.tasks = {}
            self.analyses = {}
            self.unique_id = None  # todo: rename, not really unique , maybe ref number?

        else:

            # todo: add in support for custom info to be passed through, this will be added to the object but
            # prefixed with custom_ to differentiate.
            baseline_delimiter = re.findall(BASELINE_CONTENT_TYPE_PATTERN, payload)[0]
            parts = payload.split(f"--{baseline_delimiter}")

            self.mime_version = re.findall("MIME-Version: (.*)", parts[0])[0]
            self.subject = re.findall("Subject: (.*)", parts[0])[0]
            self.relevant_when = re.findall("X-Relevant-When: (.*)", parts[0])[0]
            self.relevance_evaluation_period = re.findall("X-Relevance-Evaluation-Period: (.*)", parts[0])[0]
            # self.relevance_child_evaluation_period = re.findall(" X-Relevance-Child-Evaluation-Period: (.*)", parts[0])[0]
            self.fixlets = {}
            self.tasks = {}
            self.analyses = {}
            self.unique_id = None

            logging.info(f"Starting parsing for baseline  {self.subject}.")

            for part in parts[1:]:  # First part is handled above
                try:
                    parsed_part = find_type(part)
                    if type(parsed_part) == Task:
                        self.tasks[parsed_part.id] = parsed_part

                        if "Deploy and Run" in parsed_part.name:
                            self.deploy_and_run_id = parsed_part.id
                            logging.info(f"Deploy and Run script found: {self.deploy_and_run_id}")

                    elif type(parsed_part) == Fixlet:
                        self.fixlets[parsed_part.id] = parsed_part
                    elif type(parsed_part) == Analysis:
                        self.analyses[parsed_part.id] = parsed_part
                    elif len(part) == 3:  # -- and a new line character. End of file. Expected.
                        logging.info("Reached end of baseline.")
                        logging.info(f"Parsed {len(self.tasks)} tasks.")
                        logging.info(f"Parsed {len(self.fixlets)} fixles.")
                        logging.info(f"Parsed {len(self.analyses)} analyses.")
                    else:
                        print("Parser couldn't parse")  # todo: Handle this better
                        print(parsed_part)
                except Exception as e:
                    logging.exception(f"Failed trying to parse {part}")
                    logging.exception(e)

            # Fixlets will share the same values
            try:
                logging.info(f"Gathering baseline info from fixlets")
                first_key = list(self.fixlets)[0]
                self.source_release_date = self.fixlets.get(first_key).source_release_date
                self.modification_time = self.fixlets.get(first_key).modication_time
                self.cis_benchmark = self.fixlets.get(first_key).benchmark_version
                self.xccdf_benchmark = self.fixlets.get(first_key).xccdf_benchmark
                self.name = self.fixlets.get(first_key).source
                logging.info(f"Baseline Created.")

            except Exception as e:
                print(e)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Baseline, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Baseline, self).__delitem__(key)
        del self.__dict__[key]

    def __repr__(self):
        return f"{self.subject} has {len(self.tasks)} tasks," \
               f"and {len(self.fixlets)} fixlets, and {len(self.analyses)} analyses"

    def __hash__(self):
        return hash(frozenset(self.json()))

    def __eq__(self, other):
        try:
            return (self.__hash__()) == (other.__hash__())
        except AttributeError:
            return NotImplemented

    def add_health_check(self):
        pass

    def json(self):
        """ Outputs the objects contents as a JSON structure
            commit
        """
        payload ={
        }
        for key, value in self.items():
            # if key in ["fixlets", "tasks", "analyses"]:
            payload[key] = value

        payload["rule_id"] = self.rule_id
        payload["source_release_date"] = self.source_release_date
        payload["modification_time"] = self.modification_time
        payload["cis_benchmark"] = self.cis_benchmark
        payload["xccdf_benchmark"] = self.xccdf_benchmark
        payload["name"] = self.name
        payload["deploy_and_run_id"] = self.deploy_and_run_id

        return payload

    def differences(self, target_baseline):
        new_fixlets = []
        relevance_changes = []
        remediation_changes = []
        deploy_and_run_change = False
        deploy_and_run_fixlets = []

        baseline_differences = {
        }
        target_baseline_tests = []
        for x, y in target_baseline.fixlets.items():
            target_baseline_tests.append(y)

        if target_baseline == None:
            pass
        for key, value in self.items():
            if key == "tasks":
                for task_name, task in value.items():
                    if target_baseline.get("tasks").get(task_name) != task:
                        pass
            elif key == "fixlets":
                for fixlet_name, fixlet in value.items():
                    if target_baseline.get("fixlets").get(fixlet_name, "") == "":
                        new_fixlets.append(fixlet)
                        if baseline_differences.get("new", ""):
                            baseline_differences["new"].append(fixlet)
                        else:
                            baseline_differences["new"] = [fixlet]
                    else:
                        result_set = target_baseline.get("fixlets").get(fixlet_name).is_functionally_identical(fixlet)
                        fixlet = target_baseline.get("fixlets").get(fixlet_name)

                        for attribute in result_set:
                            if baseline_differences.get(attribute, ""):
                                baseline_differences[attribute].append(fixlet)
                            else:
                                baseline_differences[attribute] = [fixlet]
                    try:
                        target_baseline_tests.remove(fixlet)
                    except:
                        print("COULDN OT REMOVE KEY")
            elif key == "analyses":
                pass
            elif target_baseline.get(key) != value:
                pass
        print("Deploy and run required") if deploy_and_run_change else print("Deploy and run not required")
        for x in deploy_and_run_fixlets:
            pass
        return baseline_differences

    def info(self):
        pass

    @property
    def hash(self):
        import hashlib
        tester = hash(frozenset(self))
        test = hashlib.sha256().hexdigest()

    @classmethod
    def from_json(cls):
        return cls("")

    # def set_log_level(self, ):
    #     logging.getLogger().setLevel(logging.INFO)

def find_type(payload):
    """Checks substring of payload to determine whether payload is """
    if "X-Fixlet-Type: Fixlet" in payload:
        return Fixlet(payload)
    elif "X-Fixlet-Type: Analysis" in payload:
        return Analysis(payload)
    elif "X-Fixlet-Type: Task" in payload:
        return Task(payload)
    else:
        return f"Error: {payload}"
