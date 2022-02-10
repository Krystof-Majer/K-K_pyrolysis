import re

BETA_REGEX = re.compile(r"/(.+)\(K/min\)")


def get_beta(path) -> float:
    """reads beta value from specific place in file"""
    with open(path, "r", encoding="cp1250") as file:
        for line in file:
            if "#RANGE:" in line:
                m = re.search(BETA_REGEX, line)

                if m:
                    return float(m.group(1))

    raise ValueError("Unable to read temperature step from " f"file: {file}")
