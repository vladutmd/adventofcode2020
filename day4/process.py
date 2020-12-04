from contextlib import contextmanager
from typing import IO, ContextManager, Generator, List, Tuple, Dict


@contextmanager
def file_read(filename: str) -> Generator:
    f = open(filename)
    yield f
    f.close()

def is_pass_valid(pass_dict: Dict[str, str]) -> bool:
    """
    This determines if the passport is valid for the first part.
    """
    if len(pass_dict) == 8:
        return True
    elif len(pass_dict) == 7 and 'cid' not in pass_dict.keys():
        return True
    return False

def process_byr(year: str) -> bool:
    """
    This function processes the birth year in the passport.
    """
    if 1920 <= int(year) <= 2002:
        return True
    return False

def process_iyr(year: str) -> bool:
    """
    This function processes the issue year in the passport.
    """
    if 2010 <= int(year) <= 2020:
        return True
    return False

def process_eyr(year: str) -> bool:
    """
    This function processes the expiration year in the passport.
    """
    if 2020 <= int(year) <= 2030:
        return True
    return False

def process_hgt(height: str) -> bool:
    """
    This function processes the height in the passport.
    """
    units: str = height[-2:]
    if units == 'cm' and (150 <= int(height[:-2]) <= 193):
        return True
    elif units == 'in' and (59 <= int(height[:-2]) <= 76):
        return True
    return False

def process_hcl(haircolor: str) -> bool:
    """
    This function processes the hair colour in the passport.
    """
    options = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2' ,'3', '4', '5',
               '6', '7', '8', '9']
    if haircolor[0] == '#' and all([True if i in options else False for i in
                                    haircolor[1:]]):
        return True
    return False

def process_ecl(eyecolor: str) -> bool:
    """
    This function processes the eye colour in the passport.
    """
    options = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    if eyecolor in options:
        return True
    return False

def process_pid(passportid: str) -> bool:
    """
    This function processes the passport ID in the passport.
    """
    if (len(passportid) == 9) and all([True if i.isdigit() else False for i in
                                     passportid]):
        return True
    return False




def is_pass_truly_valid(pass_dict: Dict[str, str]) -> bool:
    """
    This determines if a given passport passes all the necessary checks.
    """
    if is_pass_valid(pass_dict):
        indicators: int = 0
        indicators += process_byr(pass_dict['byr'])
        indicators += process_iyr(pass_dict['iyr'])
        indicators += process_eyr(pass_dict['eyr'])
        indicators += process_hgt(pass_dict['hgt'])
        indicators += process_hcl(pass_dict['hcl'])
        indicators += process_ecl(pass_dict['ecl'])
        indicators += process_pid(pass_dict['pid'])
        return (indicators == 7)
    return False

if __name__ == '__main__':
    cm: ContextManager[IO] = file_read("input")
    with cm as input_file:
        passports: List[List[str]] = [j for j in [i.replace('\n', ' ').split()
                                                  for i in
                                                  input_file.read().split('\n\n')]]

    passport_list: List[List[Tuple[str, str]]] = []

    for passport in passports:
        list_tuples: List[Tuple[str, str]] = []
        for indicator in passport:
            list_tuples.append(tuple(k for k in indicator.split(':')))
        passport_list.append(list_tuples)

    list_dicts: List[Dict[str, str]] = []
    for passport in passport_list:
        list_dicts.append(dict(passport))

    count: int = 0
    for i in list_dicts:
        count += is_pass_valid(i)
    print(count)

    count: int= 0
    for i in list_dicts:
        count += is_pass_truly_valid(i)
    print(count)
