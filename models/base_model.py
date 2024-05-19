#!/usr/bin/python3
"""define all common attribute/method for other classes"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """parent class of AirBnB project"""

    def __init__(self, *args, **kwargs):
        """initialize id, created_at, updated_at
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        time_form = "%Y-%m-%dT%H:%M:%S.%f"

        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(val, time_form)
                else:
                    self.__dict__[key] = val
        else:
            models.storage.new(self)

    def save(self):
        """updates the updated_at public instance attribute"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        returns dictionary of key/value of __dict__
        key __class__ added to the dictionary
        """
        dicti = self.__dict__.copy()
        dicti["created_at"] = self.created_at.isoformat()
        dicti["updated_at"] = self.updated_at.isoformat()
        dicti["__class__"] = self.__class__.__name__

        return dicti

    def __str__(self):
        """print in a format"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
