import re

import numpy as np

BETA_REGEX = re.compile(r"/(.+)\(K/min\)")
MATERIAL_REGEX = re.compile(r"_[A-Z]+_")
R = 8.314


def get_beta(path) -> float:
    """reads beta value from specific place in file"""
    with open(path, "r", encoding="cp1250") as file:
        for line in file:
            if "#RANGE:" in line:
                m = re.search(BETA_REGEX, line)

                if m:
                    return float(m.group(1))

    raise ValueError("Unable to read temperature step from " f"file: {file}")


def get_material(file_name):
    material = re.search(MATERIAL_REGEX, file_name)
    if material:
        return str(material)
    else:
        raise ValueError("Unable to read material type")


def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def round_all(lst, prec=4):
    try:
        return round(lst, prec)
    except TypeError:
        return type(lst)(round_all(x, prec) for x in lst)


def calculate_ei():
    pass


def calculate_ai():
    pass
