#!/usr/bin/env python3

""" Module containing console functionality """

import cmd
import sys

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand - command line interface implementation
    """

    available_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Review": Review,
        "Amenity": Amenity,
    }
    prompt = "(hbnb) "
    file = None

    def precmd(self, command_line):
        """Initial configurations before executing commands"""
        if not sys.stdin.isatty():
            print()
        if "." in command_line:
            args = command_line.split(".")
            class_name = args[0]
            commands = args[1].replace(".", " ").replace(",", " ")
            commands = commands.replace("(", " ").replace(")", " ")
            commands = commands.split()
            command_line = commands[0] + " " + class_name
            for i in range(1, len(commands)):
                commands[i] = commands[i].replace('"', "").replace("'", "")
                command_line = command_line + " " + commands[i]
        return cmd.Cmd.precmd(self, command_line)

    def do_quit(self, command_line):
        """Quit command to exit the program"""
        self.close()
        quit()

    def emptyline(self):
        """Do nothing if an empty line is entered"""
        pass

    def do_EOF(self, command_line):
        """Handle End-of-File"""
        print()
        return True

    def do_create(self, command_line):
        """Creates an object of any available class"""
        if not command_line:
            print("** class name missing **")
            return
        elif command_line not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
            return

        new_instance = HBNBCommand.available_classes[command_line]()
        storage.save()
        print(new_instance.unique_id)

    def do_show(self, command_line):
        """Shows the string representation of an object instance"""
        result = self.check_arguments(command_line)

        if result[0]:
            class_key = result[1] + "." + result[2]
            try:
                print(storage._FileStorage__objects[class_key])
            except KeyError:
                print("** no instance found **")

    def do_all(self, command_line):
        """Prints all instances created or all instances of a certain class"""
        if command_line and command_line not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
            return

        instance_list = []
        for key, value in storage._FileStorage__objects.items():
            if command_line:
                if key.partition(".")[0] == command_line:
                    instance_list.append(str(storage._FileStorage__objects[key]))
            else:
                instance_list.append(str(storage._FileStorage__objects[key]))
        print(instance_list)

    def do_destroy(self, command_line):
        """Deletes an instance based on class name or id"""
        result = self.check_arguments(command_line)

        if result[0]:
            class_key = result[1] + "." + result[2]
            if class_key in storage._FileStorage__objects.keys():
                del storage._FileStorage__objects[class_key]
                storage.save()
            else:
                print("** no instance found **")

    def do_update(self, command_line):
        """Updates an instance based on class name and id by
        adding or updating attribute"""
        result = self.check_arguments(command_line)
        if result[0]:
            tokens = command_line.split()
            if len(tokens) < 4:
                if len(tokens) == 2:
                    print("** attribute name missing **")
                    return
                elif len(tokens) == 3:
                    print("** value missing **")
                    return
            class_key = result[1] + "." + result[2]
            if class_key in storage._FileStorage__objects.keys():
                instance = storage._FileStorage__objects[class_key]
                setattr(instance, tokens[2], tokens[3])
                storage.save()
            else:
                print("** no instance found **")

    def do_count(self, command_line):
        """Counts number of instances of a class"""
        if not command_line:
            print("** class name missing **")
            return
        if command_line not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
            return
        count = 0
        for key in storage._FileStorage__objects.keys():
            if key.split(".")[0] == command_line:
                count = count + 1
        print(count)

    def check_arguments(self, command_line):
        """Check class existence, class name, and instance id"""
        new_split = command_line.partition(" ")
        class_name = new_split[0]
        class_id = new_split[2]
        success = 1

        if not class_name:
            print("** class name missing **")
            success = 0

        elif class_name not in HBNBCommand.available_classes:
            print("** class doesn't exist **")
            success = 0

        elif not class_id:
            print("** instance id missing **")
            success = 0

        if class_id and " " in class_id:
            class_id = class_id.partition(" ")[0]

        return (success, class_name, class_id)

    def close(self):
        """Finalize"""
        if self.file:
            self.file.close()
            self.file = None


if __name__ == "__main__":
    HBNBCommand().cmdloop()

