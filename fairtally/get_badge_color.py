from howfairis import Compliance


def get_badge_color(compliance: Compliance) -> str:

    score = compliance.count(True)

    if score in [0, 1]:
        return "red"
    if score in [2, 3]:
        return "orange"
    if score in [4]:
        return "yellow"
    if score == 5:
        return "green"

    raise Exception("should not happen")
