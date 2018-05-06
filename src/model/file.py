import yaml

import os

from attrdict import AttrDict

from dropboxer import DropBoxer


class YamlFile:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        if not os.path.isfile(self.filename):
            return AttrDict()

        with open(self.filename, 'r', encoding='UTF-8') as f:
            return AttrDict(yaml.load(f.read()))

    def write(self, structure):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        with open(self.filename, 'w', encoding='UTF-8') as f:
            f.write(yaml.dump(structure))

        DropBoxer.upload(self.filename)
