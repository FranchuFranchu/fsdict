import os
import json
import shutil

RESERVED = [
    "directory",
    "isfile",
    "isdir",
    "get_top_file",
    "_mode",
    "extension",
    "read_func",
    "write_func",
    "set_dir"
    ]

def checkattr(func_item, func_attr):
    def inner(self, *args):
        if args[0] in RESERVED:
            return func_attr(self, *args)
        return func_item(self, *args)
    return inner


def check_key(key):
    if isinstance(key, str):
        if "//" in key:
            raise ValueError("// is not allowed in keys for security reasons ({})".format(key))
        if "." in key:
            raise ValueError("Dots are not allowed in keys for security reasons ({})".format(key))
        return key.replace(".", "/")
    elif isinstance(key, int):
        return key
    raise ValueError("{} is not a valid key type (expected str or int)".format(str(key.__class__)))

def get_top_file(path):
    path = os.path.normpath(path)
    if os.path.isdir(path):
        return None
    if os.path.isfile(path + ".json"):
        return path

    return get_top_file(os.path.join(path, ".."))


class FilesystemDict:
    directory: str
    def __init__(self, directory, create = False, check_exists = True, read_func = json.load, write_func = json.dump, _mode = "file"):
        if not os.path.exists(directory) and check_exists:
            if not create:
                raise FileNotFoundError(directory)
            else:
                os.makedirs(directory)

        self.directory = directory
        self.read_func = read_func
        self.write_func = write_func
        self._mode = _mode

    def set_dir(self, key, value=dict):
        # Instead of making a file, create a directory containing the dict contents

        subf = os.path.join(self.directory, key)

        if isinstance(value, dict):
            try:
                os.mkdir(subf)
            except FileExistsError:
                shutil.rmtree(subf)
                os.mkdir(subf)
            for k, v in value.items():
                self[key][k] = v
            return
        else:
            raise ValueError("Expected dict, got {}".format(type(value)))

    isfile = lambda self: os.path.isfile(self.directory)
    isdir = lambda self: os.path.isdir(self.directory)



    def __getitem__(self, key):
        key = check_key(key)

        if get_top_file(self.directory) == None:
            subf = os.path.join(self.directory, key)
            if not os.path.exists(subf + ".json") and not os.path.isdir(subf):
                raise KeyError(key)

            return self.__class__(subf, check_exists = False, read_func = self.read_func, write_func = self.write_func, _mode = self._mode,)


        # Walk JSON
        top = get_top_file(self.directory)
        with open(top + ".json") as f:
            d = self.read_func(f)

        json_path = self.directory.split(top)[1][1:]

        if json_path == "":
            r = d[key]
        else:
            for i in json_path.split("/"):
                d = d[i]
            r = d[key]

        if isinstance(r, dict):
            return self.__class__(os.path.join(top, json_path), read_func = self.read_func, write_func = self.write_func, _mode = self._mode)
        return r


    def __setitem__(self, key, value):
        
        key = check_key(key)

        if get_top_file(self.directory) == None:
            subf = os.path.join(self.directory, key)
            with open(subf + ".json", "w") as f:
                self.write_func(value, f)
            return


        # Walk JSON
        top = get_top_file(self.directory)
        with open(top + ".json") as f:
            d = self.read_func(f)

        od = d

        json_path = self.directory.split(top)[1][1:]

        if json_path == "":
            d[key] = value
        else:
            for i in json_path.split("/")[:-1]:
                d = d[i]

            d[key] = value

        with open(top + ".json", "w") as f:
            self.write_func(od, f)

    def __delitem__(self, key):
        key = check_key(key)

        if get_top_file(self.directory) == None:
            subf = os.path.join(self.directory, key)
            if not os.path.exists(subf + ".json") and os.path.isdir(subf):
                return shutil.rmtree(subf)

            if os.path.exists(subf + ".json")  and not os.path.isdir(subf):
                return os.remove(subf + ".json")

            raise KeyError(key)


        # Walk JSON
        top = get_top_file(self.directory)
        with open(top + ".json") as f:
            d = self.read_func(f)

        od = d

        json_path = self.directory.split(top)[1][1:]

        if json_path == "":
            del d[key]
        else:
            for i in json_path.split("/")[:-1]:
                d = d[i]

            del d[key]

        with open(top + ".json", "w") as f:
            self.write_func(od, f)

    __getattr__ = checkattr(__getitem__, object.__getattribute__)
    __setattr__ = checkattr(__setitem__, object.__setattr__)
    __delattr__ = checkattr(__delitem__, object.__delattr__)