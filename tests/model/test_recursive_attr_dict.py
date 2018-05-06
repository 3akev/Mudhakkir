from model.recursive_attr_dict import RecursiveAttrDict

d = {
    'deep': {
        'hierarchy': {
            'included': True
        }
    }
}

recursive = RecursiveAttrDict(d)


def test_basic():
    assert isinstance(recursive['deep'], RecursiveAttrDict)
    assert isinstance(recursive.get('deep'), RecursiveAttrDict)
    assert isinstance(recursive.deep, RecursiveAttrDict)
    assert isinstance([x for x in recursive.values()][0], RecursiveAttrDict)


def test_set():
    recursive.deep.hierarchy['included'] = False
    assert recursive.deep.hierarchy['included'] is False
