from typing import List


class Teacher():
    def __init__(self, age: int, name: str, discipline: str):
        self.age = age
        self.name = name
        self.discipline = discipline


class Student():
    def __init__(self,
                 name: str,
                 age: int,
                 school: 'School' = None,
                 teacher: Teacher = None,
                 room_mates: List['Student'] = None):
        self.name = name
        self.age = age
        self.school = school
        self.teacher = teacher
        self.room_mates = room_mates
        return


class School():
    def __init__(self, address: str, zipcode: str):
        self.address = address
        self.zipcode = zipcode
        return
