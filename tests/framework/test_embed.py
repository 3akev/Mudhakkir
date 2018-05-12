from datetime import datetime

from discord import Colour
from discord.embeds import EmptyEmbed

from framework.embed import CoolEmbed, get_embed


def test_cool_embed_initializes_color():
    assert isinstance(CoolEmbed().colour, Colour)


def test_cool_embed_initializes_timestamp():
    assert isinstance(CoolEmbed().timestamp, datetime)


def is_embed_valid(embed):
    footer_length = (len(embed.footer.text) if embed.footer else 0)
    ret = True
    ret = ret and len(embed.title) < 256
    ret = ret and len(embed.description) < 2048
    ret = ret and len(embed.author.name) < 256
    ret = ret and len(embed.fields) < 25
    for field in embed.fields:
        ret = ret and len(field.name) < 256
        ret = ret and len(field.value) < 1024
    ret = ret and footer_length < 2048
    ret = ret and (
                   len(embed.title)
                   + len(embed.description)
                   + len(embed.author.name)
                   + sum(len(field.name) + len(field.value) for field in embed.fields)
                   + footer_length
           ) < 6000

    return ret


def test_get_embed_returns_embed():

    header_row = [
        'category', 'author_name', 'author_url',
        'author_icon_url', 'title', 'url',
        'thumbnail_url', 'description', 'image_url',
        'footer_text', 'footer_icon_url', 'colour'
    ]
    row = ['quran', '', '', '', '', '', '', 'test', '', "Qur'an 94:5-6", '', "00ffff"]

    d = dict(zip(header_row, row))
    e = get_embed(d)
    assert isinstance(e, CoolEmbed)

    type(EmptyEmbed).__len__ = lambda s: 0
    assert is_embed_valid(e)
