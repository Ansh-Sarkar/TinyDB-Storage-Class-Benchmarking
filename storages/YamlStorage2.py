#!/usr/bin/env python3
import yaml
from tinydb.storages import Storage, touch

class YamlStorage2(Storage):
    """
    Store the data in a YAML file.
    """
    def __init__(self, filename):  # (1)
        super().__init__()
        self.filename = filename
        touch(filename, create_dirs=False)

    def __str__(self) -> str:
        return str(__name__)
    
    def __repr__(self) -> str:
        return str(__name__)

    def read(self):
        with open(self.filename, encoding='utf-8') as handle:
            try:
                data = yaml.load(handle.read(), Loader=yaml.SafeLoader)
                return data
            except yaml.YAMLError:
                return None  # (3)

    def write(self, data):
        # print(f'Writing Data: {data}')
        with open(self.filename, 'w', encoding='utf-8') as handle:
                yaml.dump(data, handle, Dumper=yaml.SafeDumper)

    def close(self):  # (4)
        pass

__all__ = [ 'YamlStorage2' ]
