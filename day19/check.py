import re
from contextlib import contextmanager
from typing import IO, ContextManager, Dict, Generator, List, Union


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()


def parse_line(line: str) -> Union[Dict[str, str], str]:
    """
    This functions parses a line of the input and either returns
    a dictionary if it's a rule or a string if it's a message.
    """
    rule: str
    conditions: str
    if ":" in line:  # then it's a rule
        split_line: List[str] = line.split(":")
        rule, conditions = split_line[0], split_line[1].strip()
        return {rule: conditions}
    elif "a" in line or "b" in line:  # then it's a message
        return line
    return "-1"


def parse_rules(raw_rules: Dict[str, str]) -> Dict[str, str]:
    """
    This function goes through the raw rules dictionary and does the
    necessary substitutions and returns one that only has 'a' and 'b'
    in it and no more references to other rules.
    """
    # start with the rules that have "a" or "b" in them
    # those are the ones that are "parsed"
    # then do the ones that contain references to the ones that are parsed
    # and so on
    complete_rules: Dict[str, str] = {}
    while "0" not in complete_rules:
        for rule, conditions in raw_rules.items():
            if rule in complete_rules:
                continue
            elif '"' in conditions:
                complete_rules[rule] = conditions.replace('"', "")
            else:
                # get the rules numbers referred to in the conditions
                # and order them from highest rule number to lowest
                rule_refs = re.findall(r"(\d+)", conditions)
                rule_refs.sort(key=len, reverse=True)
                # check if all the numbers the rule references are in the
                # complete_rules already
                if all([ref in complete_rules for ref in rule_refs]):
                    for ref in rule_refs:
                        raw_rules[rule] = raw_rules[rule].replace(
                            ref, complete_rules[ref]
                        )
                    raw_rules[rule] = raw_rules[rule].replace(" ", "")
                    raw_rules[rule] = "(" + raw_rules[rule] + ")"
                    complete_rules[rule] = raw_rules[rule]
    return complete_rules


def parse_rules_2(raw_rules: Dict[str, str]) -> Dict[str, str]:
    """
    This function goes through the raw rules dictionary for part 2
    and does the necessary substitutions
    """

    complete_rules_2: Dict[str, str] = {}
    while "0" not in complete_rules_2:
        for rule, conditions in raw_rules.items():
            if rule in complete_rules_2:
                continue
            elif '"' in conditions:
                complete_rules_2[rule] = conditions.replace('"', "")
            else:
                # get the rules numbers referred to in the conditions
                # and order them from highest rule number to lowest
                rule_refs = re.findall(r"(\d+)", conditions)
                rule_refs.sort(key=len, reverse=True)
                # check if all the numbers the rule references are in the
                # complete_rules already

                # special cases for 8 42 11 31
                if rule == "8" and "42" in complete_rules_2:
                    complete_rules_2[rule] = complete_rules_2["42"] + "+"
                elif (
                    rule == "11"
                    and "42" in complete_rules_2
                    and "31" in complete_rules_2
                ):
                    complete_rules_2[rule] = (
                        "(("
                        + complete_rules_2["42"]
                        + r"){x}("
                        + complete_rules_2["31"]
                        + r"){x})"
                    )
                elif all([ref in complete_rules_2 for ref in rule_refs]):
                    for ref in rule_refs:
                        raw_rules[rule] = re.sub(
                            ref, complete_rules_2[ref], raw_rules[rule]
                        )
                    raw_rules[rule] = raw_rules[rule].replace(" ", "")
                    raw_rules[rule] = "(" + raw_rules[rule] + ")"
                    complete_rules_2[rule] = raw_rules[rule]
    return complete_rules_2


def validate_message(message: str, rule_0: str) -> bool:
    """
    This function validates a message depending on what the complete_rules ditionary is.
    """
    return bool(re.fullmatch(rule_0, message))


if __name__ == "__main__":
    cm: ContextManager[IO] = file_read("input")
    raw_rules: Dict[str, str] = {}
    messages: List[str] = []
    processed: Union[Dict[str, str], str]
    with cm as input_file:
        for line in input_file.read().splitlines():
            processed = parse_line(line)
            if isinstance(processed, dict):
                raw_rules.update(processed)
            elif isinstance(processed, str):
                messages.append(processed)
    complete_rules: Dict[str, str] = parse_rules(raw_rules)
    rule_0: str = complete_rules["0"]
    print(sum([validate_message(message, rule_0) for message in messages]))

    # ok part 2
    # start with the same messages and raw_rules as before
    raw_rules = {}
    messages = []
    cm = file_read("input")
    with cm as input_file:
        for line in input_file.read().splitlines():
            processed = parse_line(line)
            if isinstance(processed, dict):
                raw_rules.update(processed)
            elif isinstance(processed, str):
                messages.append(processed)
    complete_rules_2: Dict[str, str] = parse_rules_2(raw_rules)

    rule_0 = complete_rules_2["0"].replace("x", "1")
    count: int = sum([validate_message(message, rule_0) for message in messages])

    prev: int = 0
    rep: int = 2
    while prev != count:
        prev = count
        rule_0 = complete_rules_2["0"].replace("x", str(rep))
        count += sum([validate_message(message, rule_0) for message in messages])
        rep += 1
    print(count)
