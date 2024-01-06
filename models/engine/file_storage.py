#!/usr/bin/python3
'''
    Defines class FileStorage
'''
import json
import models


class FileStorage:
    '''
        Serialize instances to JSON file and deserialize to JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            Return the dictionary
        '''
        new_dict = {}
        if cls is None:
            return self.__objects

        if cls != "":
            for k, v in self.__objects.items():
                if cls == k.split(".")[0]:
                    new_dict[k] = v
            return new_dict
        else:
            return self.__objects

    def new(self, obj):
        '''
            Set in __objects objects with key <object class name>.id
            Aguments:
                obj : An instance object.
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''
            Serialize __objects attribute to JSON file.
        '''
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''
            Deserialize the JSON file to __objects.
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
        Delete an object
        '''
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        '''
        Deserializes JSON file to objects
        '''
        self.reload()

    def get(self, cls, id):
        '''
            Retrieves an obj w/class name and id
        '''
        result = None

        try:
            for v in self.__objects.values():
                if v.id == id:
                    result = v
        except BaseException:
            pass

        return result

    def count(self, cls=None):
        '''
            Counts num objects in FileStorage
        '''
        cls_counter = 0

        if cls is not None:
            for k in self.__objects.keys():
                if cls in k:
                    cls_counter += 1
        else:
            cls_counter = len(self.__objects)
        return cls_counter

