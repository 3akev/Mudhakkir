from model.recursive_attr_dict import RecursiveAttrDict

d = {
    'deep': {
        'hierarchy': {
            'included': True
        }
    }
}

recursive = RecursiveAttrDict(d)


def test():
    assert isinstance(recursive['deep'], RecursiveAttrDict)
    assert isinstance(recursive.get('deep'), RecursiveAttrDict)
    assert isinstance(recursive.deep, RecursiveAttrDict)
