from munch import AutoMunch


class RecursiveAttrDict(AutoMunch):
    def __getitem__(self, item):
        ret = super().__getitem__(item)
        if isinstance(ret, dict):
            ret = RecursiveAttrDict(ret)
            setattr(self, item, ret)

        return ret

    def get(self, k, d=None):
        ret = super().get(k, d)
        if isinstance(ret, dict):
            ret = RecursiveAttrDict(ret)
            setattr(self, k, ret)

        return ret

    def values(self):
        return (
            (RecursiveAttrDict(x) if isinstance(x, dict) else x)
            for x in super().values()
        )
