from attrdict import AttrDict


class RecursiveAttrDict(AttrDict):
    def __getitem__(self, item):
        ret = super().__getitem__(item)
        if isinstance(ret, dict):
            return RecursiveAttrDict(ret)
        else:
            return ret

    def get(self, k, d=None):
        ret = super().get(k, d)
        if isinstance(ret, dict):
            return RecursiveAttrDict(ret)
        else:
            return ret
