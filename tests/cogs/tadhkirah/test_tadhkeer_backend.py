import asyncio
from unittest.mock import MagicMock

import pytest
from pygsheets import Worksheet

from cogs.tadhkirah.tadhkeer_backend import TadhkeerBackend
from framework.embed import CoolEmbed
from util.embed import is_embed_valid


row = ['quran', '', '', '', '', '', '', 'test', '', "Qur'an 94:5-6", '', "00ffff"]


class TadhkeerBackendTest(TadhkeerBackend):
    def __init__(self):
        super().__init__(asyncio.get_event_loop())
        self._sheet = MagicMock(Worksheet)
        f = asyncio.Future()
        f.set_result(row)
        self._sheet.get_row.return_value = f
        self._header_row = [
            'category', 'author_name', 'author_url',
            'author_icon_url', 'title', 'url',
            'thumbnail_url', 'description', 'image_url',
            'footer_text', 'footer_icon_url', 'colour'
        ]


@pytest.fixture()
def tb():
    yield TadhkeerBackendTest()


def test_make_embed_makes_embed_from_row(tb):
    e = tb._make_embed(row)
    assert isinstance(e, CoolEmbed)
    assert is_embed_valid(e)
