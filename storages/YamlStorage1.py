#!/usr/bin/env python3
import yaml
from tinydb.storages import Storage, touch

class YamlStorage1(Storage):
    """
    Store the data in a YAML file.
    """
    def __init__(self, path, **kwargs):
        """
        Create a new instance & storage file, if it doesn't exist.
        param: path (str) = Location for storing the YAML data.
        """
        super().__init__()
        # create directories set to False for now to avoid empty
        # string based base directory creation issues.
        touch(path, create_dirs = False) # Create file if not exists
        self.kwargs = kwargs
        self._handle = open(
            path, 'r+',
            encoding='utf-8'
        )

    def __str__(self) -> str:
        return str(__name__)
    
    def __repr__(self) -> str:
        return str(__name__)

    def close(self):
        self._handle.close()

    def read(self):
        # Get the file size
        self._handle.seek(0, 2)
        size = self._handle.tell()

        if not size:
            return None # File is empty
        else:
            self._handle.seek(0)
            loaded = yaml.load(self._handle, Loader=yaml.SafeLoader)
            # print(f'Loaded Data: {loaded}')
            return loaded

    def write(self, data):
        self._handle.seek(0)
        serialized = yaml.dump(data, **self.kwargs, Dumper=yaml.SafeDumper)
        self._handle.write(serialized)
        self._handle.flush()
        self._handle.truncate()

__all__ = [ 'YamlStorage1' ]
