from model.argparser import util


def test_tokenize_splits_string():
    assert util.tokenize('thing x y z') == ['thing', 'x', 'y', 'z']


def test_tokenize_regards_double_quoted_args():
    assert util.tokenize('"cool arg" 23') == ['cool arg', '23']
    assert util.tokenize('you "know it" True') == ['you', 'know it', 'True']


def test_tokenize_parses_keyword_arguments():
    assert util.tokenize('stuff=cool 305 magic') == ['stuff=cool', '305', 'magic']
    assert util.tokenize('stuff="really cool" 30') == ['stuff=really cool', '30']
