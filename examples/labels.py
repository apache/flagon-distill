from typing import Any, Dict, List, Callable
import pandas as pd


class FeatureDefinition:
    # Implement class logic
    # TODO: Add a very specific type hint to the rule object:
    # see: https://docs.python.org/3/library/typing.html#annotating-callable-objects
    def __init__(self, label: str, rule: Callable[[Dict[str, Any]], bool]):
        if not callable(rule):
            raise TypeError("Rule not callable")
        
        if isinstance(label, str):
            pass
        else:
            raise TypeError("Label is not a string")
        # Immediately validate the rule, so you can error
        # out/exit early if it's invalid
            # TODO: raise an informative error to the user
            # see:
            # - https://www.geeksforgeeks.org/python-exception-handling/
            # - https://docs.python.org/3/tutorial/errors.html#raising-exceptions

        self.label = label
        self._rule = rule

    # This is a wrapper method around the private rule attribute we
    # store on self during init.
    #
    # Q: Why make the rule private and
    # wrap the call to it in another method?
    # A: This encapsulation allows us to expose a nicer set of behavior
    # and naming conventions to both the user and ourselves as developers.
    # In `label_features` below, you see that we can then check whether
    # a log `matches` the definition which reads more like plain english
    # and is an important part of writing clean, idiomatic python code.
    # TODO: Implement this wrapper function by using the _rule attribute
    def matches(self, log: Dict[str, Any]) -> bool:
            return self._rule(log)


def label_features(
    logs: List[Dict[str, Any]], definitions: List[FeatureDefinition]
) -> List[Dict[str, Any]]:
    # Iterate through all the logs
    for log in logs:
        # Check whether the log matches the definition
        # for each definition supplied in the defintions list
        for definition in definitions:
            # NOTE: This reads much like an English sentence
            # and is self-explanatory. I don't need to read the
            # implementation logic to get a sense of what's happening
            if definition.matches(log):
                # NOTE: Since we're mutating the log itself and interacting
                # with a field that may (does) not already exists, we need
                # to first check if it is present in our log and instantiate
                # it if not.
                if "labels" not in log:
                    log.update({"labels": list()})
                log["labels"].append(definition.label)
    return logs


###########################################################
# Example of how the FeatureDefintion class works
#
# The following if __name__ == "__main__" syntax
# is a way to tell python that if your run this file
# as a script from the command line, then this is the code
# that needs to be executed.
###########################################################
if __name__ == "__main__":
    # TODO: Import logs from JSON file here ...
    json_file = input("Enter your json file path: ")
    logs = setup(json_file, "datetime")
    
    

    # Create a map rule to test out the FeatureDefinition with
    def map_rule(log: Dict[str, Any]) -> bool:
        return "pageUrl" in log and "map" in log["pageUrl"]

    def container_rule(log: Dict[str, Any]) -> bool:
        return "path" in log and "container" in log["path"]
    
    def table_rule(log: Dict[str, Any]) -> bool:
        return "path" in log and "table" in log["path"]
    
    def integer_rule(log: Dict[str, Any]) -> bool:
        return "path" in log and 10 in log["path"]
    


    # TODO: Examine the UserALE logs, see what fields-values exist
    # and write a few more fews we can test our logic against
    # So long as the rule accepts a log and returns a true/false
    # value, it is valid. This is a very expansive signature which
    # supports things like string matching, regular expressions,
    # and more.

    map_page_definition = FeatureDefinition(rule=map_rule, label="map_page")
    container_path_definition = FeatureDefinition(rule=container_rule, label="container_path")
    table_path_definition = FeatureDefinition(rule=table_rule, label="table_path")
    integer_path_definition = FeatureDefinition(rule=integer_rule, label= 10)

    label_features(logs=logs, definitions=[map_page_definition])
    label_features(logs=logs, definitions=[container_path_definition])
    label_features(logs=logs, definitions=[table_path_definition])
    label_features(logs=logs, definitions=[integer_path_definition])

