import unittest

from gson.gmarshal import unmarshal_from_str

from path_to_class.foo import Teacher


class TestMarshal(unittest.TestCase):
    t1 = '{"age": 29, "name": "Bob", "discipline": "History", "married": "false"}'
    t2 = '{"age": 29, "name": "Bob", "discipline": "History", "married": "True"}'
    t3 = '{"age": 29, "name": "Bob", "discipline": "History", "married": 0}'

    def test_unmarshal_from_str(self):
        teacher_obj, e = unmarshal_from_str(self.t1, Teacher)
        self.assertIsNone(e)
        self.assertEqual(teacher_obj.married, False)
        teacher_obj, e = unmarshal_from_str(self.t2, Teacher)
        self.assertIsNone(e)
        self.assertEqual(teacher_obj.married, True)
        teacher_obj, e = unmarshal_from_str(self.t3, Teacher)
        self.assertIsNone(e)
        self.assertEqual(teacher_obj.married, False)
