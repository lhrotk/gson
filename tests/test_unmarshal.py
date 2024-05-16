import unittest

from gson.gmarshal import marshal, unmarshal_from_str

from path_to_class.foo import School, Student, Teacher


class TestMarshal(unittest.TestCase):
    expected_json_str = '{"name": "Tom", "age": 18, "school": {"address": "18E Ave", "zipcode": "Q1W2E3"}, "teacher": {"age": 29, "name": "Bob", "married": false, "discipline": "History"}, "room_mates": [{"name": "Shirley", "age": 18}]}'

    def test_marshal(self):
        tom = Student(
            "Tom",
            18,
            School("18E Ave", "Q1W2E3"),
            Teacher(29, "Bob", "History"),
            room_mates=[Student("Shirley", 18)],
        )

        res = marshal(tom)
        self.assertEqual(res, self.expected_json_str)

    def test_unmarshal_from_str(self):
        stu_obj, e = unmarshal_from_str(self.expected_json_str, Student)
        self.assertIsNone(e)
        self.assertIsNotNone(stu_obj.school)
        self.assertIsNotNone(stu_obj.teacher)
        self.assertNotEqual(len(stu_obj.room_mates), 0)
