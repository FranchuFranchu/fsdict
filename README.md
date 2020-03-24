# fsdict
Store python dictionaries in a mixed directory/file structure

## Sample code

    from fsdict import FilesystemDict
    from os import getcwd
    from os.path import join
    
    directory = join(getcwd(), "fsdict-test")
    a = FilesystemDict(directory, create=True)
    a.set_dir("people", {"John": {"age": 15}, "Hannah": {"age": 21}})
    
    new_age = input("Update John's age")
    a.people["John"].age = int(new_age)