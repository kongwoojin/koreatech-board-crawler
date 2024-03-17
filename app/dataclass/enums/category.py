from enum import Enum


def get_category(text: str):
    if text == "일반공지":
        return Category.NOTICE
    elif text == "대외활동":
        return Category.EA
    elif text == "교내활동":
        return Category.CA
    elif text == "근로장학생모집":
        return Category.WORK
    elif text == "":
        return Category.NONE
    else:
        return Category.ETC


class Category(Enum):
    NONE = "NONE"
    NOTICE = "NOTICE"
    EA = "EA"  # External Activity
    CA = "CA"  # Campus Activity
    WORK = "WORK"
    ETC = "ETC"

    def __init__(self, category):
        self.category = category

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
