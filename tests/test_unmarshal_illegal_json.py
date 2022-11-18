import unittest

from gson.gmarshal import marshal, unmarshal_from_str
from tests.path_to_class.foo import School, Student, Teacher
from tests.path_to_other_class.bar import Group, Lesson


class TestMarshalComplex(unittest.TestCase):
    expected_str = '{"teacher": {"age": 40, "name": "Alex", "discipline": "Math"}, "groups": {"group A": {"group_name": "GA", "group-members": [{"name": "A", "age": 10, "school": {"address": "17W AVE", "zipcode": "q1w2e3"}, "teacher": {"age": 40, "name": "Alex", "discipline": "Math"}}, {"name": "B", "age": 10, "school": {"address": "17W AVE", "zipcode": "q1w2e3"}, "teacher": {"age": 40, "name": "Alex", "discipline": "Math"}}]}, "group C": {"group_name": "GB", "group_members": [{"name": "C", "age": 10, "school": {"address": "17W AVE", "zipcode": "q1w2e3"}, "teacher": {"age": 40, "name": "Alex", "discipline": "Math"}}, {"name": "D", "age": 10, "school": {"address": "17W AVE", "zipcode": "q1w2e3"}, "teacher": {"age": 40, "name": "Alex", "discipline": "Math"}}]}}}'

    def test_unmarshal(self):
        obj, e = unmarshal_from_str(self.expected_str, Lesson)
        self.assertIsNone(e)
        self.assertIsNotNone(obj)
        self.assertNotEqual(len(obj.groups), 0)
