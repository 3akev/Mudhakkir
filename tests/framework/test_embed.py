from datetime import datetime

from discord import Colour

from framework.embed import CoolEmbed, get_embed
from util.embed import is_embed_valid


def test_cool_embed_initializes_color():
    assert isinstance(CoolEmbed().colour, Colour)


def test_cool_embed_initializes_timestamp():
    assert isinstance(CoolEmbed().timestamp, datetime)


def test_get_embed_returns_embed():
    d = {
        'category': 'quran',
        'author_name': '',
        'author_url': '',
        'author_icon_url': '',
        'title': '', 'url': '',
        'thumbnail_url': '',
        'description': 'test',
        'image_url': '',
        'footer_text': "Qur'an 94:5-6",
        'footer_icon_url': '',
        'colour': '00ffff'
    }

    e = get_embed(d)

    assert isinstance(e, CoolEmbed)
    assert is_embed_valid(e)
