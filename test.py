from fsdict import FilesystemDict
from os import getcwd
from os.path import join

directory = join(getcwd(), "fsdict-test")
a = FilesystemDict(directory, create=True)
a.set_dir("people", {"John": {"age": 15}, "Hannah": {"age": 21}})
a.people.John.age = {"a": 1}