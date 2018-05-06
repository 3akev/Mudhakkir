from model import argparser


def test_parse_parses_arguments():
    assert argparser.parse('true 4 12.5 stuff') == (['true', '4', '12.5', 'stuff'], {})


def test_parse_parses_keywork_arguments():
    assert argparser.parse('thing=200 size=4454') == ([], {'thing': '200', 'size': '4454'})


def test_parse_parses_mixed_arguments():
    assert argparser.parse('3 3.2 magic thing=1990 bad=true') == (['3', '3.2', 'magic'], {'thing': '1990', 'bad': 'true'})


def test_parse_parses_out_of_order_keyword_arguments():
    assert argparser.parse('3 3.2 thing=1990 magic bad=true') == (['3', '3.2', 'magic'], {'thing': '1990', 'bad': 'true'})


def test_parse_parses_quoted_arguments():
    assert argparser.parse('3 3.2 thing="year 1990" "code magic" bad=true') == (['3', '3.2', 'code magic'], {'thing': 'year 1990', 'bad': 'true'})


def test_to_dict_converts_to_dict():
    dict_list = [
        {'isCool': 'true'},
        {'time': '2002'},
        {'name': 'JohnDoe'}
    ]

    for ind, x in enumerate([f'{k}={v}' for dict_ in dict_list for k, v in dict_.items()]):
        assert argparser.to_dict(x) == dict_list[ind]
