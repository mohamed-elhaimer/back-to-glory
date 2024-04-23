#!/usr/bin/python3
import json
import os
from models.base_model import BaseModel
class FileStorage:
    __file_path = 'file.json'
    __objects = {}
    def all(self):
        return FileStorage.__objects
    def new(self, obj):
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj
    def save(self):
        with open(FileStorage.__file_path, "w") as f:
            json.dump({k:v.to_dict() for k, v in FileStorage.__objects.items()} , f)
    def reload(self):
        current_classes = {
            'BaseModel': BaseModel,
        }
        if not os.path.exists(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, 'r') as f:
            data = None
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pass
            if data is None:
                return
            FileStorage.__objects = {
                k: current_classes[k.split('.')[0]](**v)
                for k, v in data.items()
            }