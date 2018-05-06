from model.argparser.util import tokenize


def parse(string):
    args = []
    kwargs = {}

    tokenized = tokenize(string)
    for segment in tokenized:
        if segment.find('=') != -1:
            kwargs.update(to_dict(segment))
        else:
            args.append(segment)

    return args, kwargs


def to_dict(thing):
    key, value = thing.split('=')
    return {key: value}
