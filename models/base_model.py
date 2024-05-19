#!/usr/bin/python3
"""Define all common attributes/methods for other classes"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """Parent class of the AirBnB project"""

    def __init__(self, *args, **kwargs):
        """Initialize id, created_at, updated_at
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"

        self.unique_id = str(uuid4())
        self.creation_time = datetime.today()
        self.modification_time = datetime.today()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, time_format)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """Updates the modification_time public instance attribute"""
        self.modification_time = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary of key/value pairs of __dict__
        Key __class__ added to the dictionary
        """
        dictionary_copy = self.__dict__.copy()
        dictionary_copy["created_at"] = self.creation_time.isoformat()
        dictionary_copy["updated_at"] = self.modification_time.isoformat()
        dictionary_copy["__class__"] = self.__class__.__name__

        return dictionary_copy

    def __str__(self):
        """Print in a specific format"""
        return f"[{self.__class__.__name__}] ({self.unique_id}) {self.__dict__}"

