from typing import Dict, Any
import unittest

from gson.gmarshal import unmarshal_from_str


class SomeBody():
    def __init__(self, name: str, age: int, attributes: Dict[str, Any]):
        self.name = name
        self.age = age
        self.attributes = attributes


class TestAnyAttribute(unittest.TestCase):
    somebody = '{"age": 29, "name": "Bob", "attributes": {"bool": true, "int": 1, "str": "string"}}'

    def test_unmarshal_any(self):
        object, e = unmarshal_from_str(self.somebody, SomeBody)
        assert "int" in object.attributes.keys()
        assert "bool" in object.attributes.keys()
        assert "str" in object.attributes.keys()
        assert object.attributes["int"] == 1
        assert object.attributes["bool"]
        assert object.attributes["str"] == "string"
