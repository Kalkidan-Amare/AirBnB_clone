#!/usr/bin/python3
"""Connvert dictionary representation to a JSON string"""
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel
import json


class FileStorage:
    """
    serializes instances to a JSON file
    deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns __object dictionary"""
        return FileStorage.__objects

    def new(self, obj):
        """sets __objects"""
        obcl_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obcl_name, obj.id)] = obj

    def save(self):
        """serializes to JSON file"""
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """deserializes JSON file"""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
