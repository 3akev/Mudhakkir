import yaml

import os

from dropboxer import DropBoxer
from model.recursive_attr_dict import RecursiveAttrDict


class YamlFile:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        if not os.path.isfile(self.filename):
            return RecursiveAttrDict()

        with open(self.filename, 'r', encoding='UTF-8') as f:
            return RecursiveAttrDict(yaml.load(f.read()))

    def write(self, structure):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        with open(self.filename, 'w', encoding='UTF-8') as f:
            f.write(yaml.dump(structure))

        DropBoxer.upload(self.filename)
