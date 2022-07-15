import importlib
from typing import Type

from class_for_test.foo import School, Student, Teacher
from gmarshal import marshal, unmarshal_from_str

if __name__ == '__main__':
    tom = Student('Tom',
                  18,
                  School('18E Ave', 'Q1W2E3'),
                  Teacher(29, 'Bob', 'History'),
                  room_mates=[Student('Shirley', 18)])
    res = marshal(tom)
    print(res)
    obj = unmarshal_from_str(res, Student)
    print(obj)
