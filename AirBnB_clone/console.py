#!/usr/bin/python3
import cmd
from models.base_model import BaseModel
from models import storage
import re
current_classes = {
        'BaseModel' : BaseModel
    }
list_attribut = ["id", "created_at", "updated_at"]
class HBNBCommand(cmd.Cmd):
    intro = 'welcome to my console for Airbnb project'
    prompt = '(hbnb)'
    def precmd(self, line):
        return super().precmd(line)
    def do_EOF(self, line):
        """Inbuilt EOF command to gracefully catch errors."""
        return True
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    def emptyline(self):
        """do nothing on empty line"""
        pass
    def do_help(self, arg):
        """To get help on a command, type help <topic>."""
        return super().do_help(arg)
    def do_create(self, args):
        args = args.split()
        if len (args) < 1:
            print('** class name missing **')
        elif args[0] not in current_classes.keys():
            print("** class doesn't exist **")
        else:
            new_instance = current_classes[args[0]]()
            id = new_instance.id
            new_instance.save()
            print(id)
    def do_show(self, args):
        args = args.split()
        if len(args) < 1:
            print('** class name missing **')
        elif args[0] not in current_classes.keys():
            print("** class doesn't exist **")
        elif len (args) < 2:
            print("** instance id missing **")
        else:
            data = storage.all()
            key = "{}.{}".format(args[0],args[1])
            myobject = data.get(key)
            if myobject is None:
                print("** no instance found **")
            else:
                print(myobject)
    def do_destroy(self, args):
        args = args.split()
        if len (args) < 1:
            print('** class name missing **')
        elif args[0] not in current_classes.keys():
            print("** class doesn't exist **")
        elif len (args) < 2:
            print("** instance id missing **")
        else:
            data = storage.all()
            key = "{}.{}".format(args[0],args[1])
            myobject = data.get(key)
            if myobject is None:
                print("** no instance found **")
            else:
                del data[key]
                storage.save()
    def do_all(self, args):
        args = args.split()
        data = storage.all()
        if len(args) < 1:
            print(["{}".format(str(v)) for _, v in data.items()])
        elif args[0] not in current_classes.keys():
            print ("** class doesn't exist **")
        else:
            print(["{}".format(str(v)) for _, v in data.items() if type(v).__name__ == args[0]])
    def do_update(self, args):
        args = args.split()
        args = args[:4]
        if len(args) < 1:
            print("** class name missing **")
        elif args[0] not in current_classes.keys():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        data = storage.all()
        key = "{}.{}".format(args[0], args[1])
        myObject = data.get(key)
        if myObject is None:
            print("** no instance found **")
        if args[2] in list_attribut:
            return
        first_attr = re.findall(r"^[\"\'](.*?)[\"\']", args[3])
        if first_attr:
            setattr(myObject, args[2], first_attr[0])
        else:
            value_list = args[3].split()
            setattr(myObject, args[2], parse_str(value_list[0]))
        storage.save()
def parse_str(arg):
    """Parse `arg` to an `int`, `float` or `string`.
    """
    parsed = re.sub("\"", "", arg)
    if is_int(parsed):
        return int(parsed)
    elif is_float(parsed):
        return float(parsed)
    else:
        return arg


def is_float(x):
    """Checks if `x` is float.
    """
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True


def is_int(x):
    """Checks if `x` is int.
    """
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b
if __name__ == "__main__":
    HBNBCommand().cmdloop()