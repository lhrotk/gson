import unittest

from gson.gmarshal import marshal, unmarshal_from_str

from path_to_class.foo import School, Student, Teacher
from path_to_other_class.bar import Group, Lesson


class TestMarshalComplex(unittest.TestCase):
    maxDiff = None

    expected_str = '{"teacher": {"age": 40, "name": "Alex", "married": false, "discipline": "Math"}, "groups": {"group A": {"group_name": "GA", "group_members": [{"name": "A", "age": 10, "school": {"address": "17W AVE", "zipcode": "q1w2e3"}, "teacher": {"age": 40, "name": "Alex", "married": false, "discipline": "Math"}}, {"name": "B", "age": 10, "school": {"address": "17W AVE", "zipcode": "q1w2e3"}, "teacher": {"age": 40, "name": "Alex", "married": false, "discipline": "Math"}}]}, "group C": {"group_name": "GB", "group_members": [{"name": "C", "age": 10, "school": {"address": "17W AVE", "zipcode": "q1w2e3"}, "teacher": {"age": 40, "name": "Alex", "married": false, "discipline": "Math"}}, {"name": "D", "age": 10, "school": {"address": "17W AVE", "zipcode": "q1w2e3"}, "teacher": {"age": 40, "name": "Alex", "married": false, "discipline": "Math"}}]}}}'

    def test_marshal(self):
        teacher = Teacher(40, 'Alex', 'Math')
        school = School('17W AVE', 'q1w2e3')
        groups = {
            'group A':
            Group('GA', [
                Student('A', 10, school, teacher),
                Student('B', 10, school, teacher)
            ]),
            'group C':
            Group('GB', [
                Student('C', 10, school, teacher),
                Student('D', 10, school, teacher)
            ])
        }
        lesson = Lesson(teacher, groups)
        res = marshal(lesson)
        self.assertEqual(res, self.expected_str)

    def test_unmarshal(self):
        obj, e = unmarshal_from_str(self.expected_str, Lesson)
        self.assertIsNone(e)
        self.assertIsNotNone(obj)
        self.assertNotEqual(len(obj.groups), 0)
