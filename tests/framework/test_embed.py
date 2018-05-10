from datetime import datetime

from discord import Colour

from framework.embed import CoolEmbed


def test_cool_embed_initializes_color():
    assert isinstance(CoolEmbed().colour, Colour)


def test_cool_embed_initializes_timestamp():
    assert isinstance(CoolEmbed().timestamp, datetime)
