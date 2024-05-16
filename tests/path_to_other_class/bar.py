from typing import Dict, List

from path_to_class.foo import Student, Teacher


class Group():
    def __init__(self, group_name: str, group_members: List[Student]):
        self.group_name = group_name
        self.group_members = group_members


class Lesson():
    def __init__(self, teacher: Teacher, groups: Dict[str, Group]):
        self.teacher = teacher
        self.groups = groups
