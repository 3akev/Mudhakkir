from unittest.mock import MagicMock, Mock

import pytest
from pygsheets import Worksheet, DataRange, Cell

from cogs.tadhkirah.tadhkeer_backend import TadhkeerBackend
from util.async import get_mock_coro
from util.embed import is_embed_valid


header_row = [
    'category', 'author_name', 'author_url',
    'author_icon_url', 'title', 'url',
    'thumbnail_url', 'description', 'image_url',
    'footer_text', 'footer_icon_url', 'colour'
]
row1 = ['quran', '', '', '', '', '', '', 'test1', '', "Qur'an 94:5-6", '', "00ffff"]
row2 = ['hadith', '', '', '', '', '', '', 'test2', '', "Bukhari", '', "00ffff"]


rows = [header_row, row1, row2]


class TadhkeerBackendTest(TadhkeerBackend):
    def __init__(self, loop):
        super().__init__(loop)
        self._sheet = MagicMock(Worksheet)
        self._sheet.get_row = lambda n: rows[n - 1]
        self._sheet.rows = len(rows)
        self._header_row = header_row

    def _authorize_client(self):
        self._sheet = MagicMock(Worksheet)


@pytest.fixture()
def tb(event_loop):
    yield TadhkeerBackendTest(event_loop)


@pytest.mark.asyncio
async def test_wait_for_ready_logs_in_if_not_already(tb):
    tb._sheet = None
    tb._readying = False

    await tb._wait_for_ready()

    assert tb._sheet is not None


@pytest.mark.asyncio
async def test_wait_for_ready_waits_if_logging_in(monkeypatch, tb):
    tb._sheet = None
    tb._readying = True
    mocked_sleep = get_mock_coro()
    monkeypatch.setattr('cogs.tadhkirah.tadhkeer_backend.asyncio.sleep', mocked_sleep)

    def x(y): tb._readying = False
    mocked_sleep.side_effect = x

    await tb._wait_for_ready()

    assert mocked_sleep.called
    assert tb._readying is False


@pytest.mark.asyncio
async def test_wait_for_ready_passes_if_ready(tb):
    assert tb._sheet is not None
    tb._readying = False
    tb._authorize_client = Mock()

    await tb._wait_for_ready()

    assert not tb._authorize_client.called


def test_make_embed_makes_embed_from_row(tb):
    e = tb._make_embed(row1)
    assert is_embed_valid(e)


@pytest.mark.asyncio
async def test_get_makes_embed_from_row_number(tb):
    e = await tb._get(2)
    assert is_embed_valid(e)


@pytest.mark.asyncio
async def test_get_random_gets_random_tadhkirah_from_sheet(tb):
    for _ in range(10):
        e = await tb.get_random()
        assert is_embed_valid(e)
        assert e.title != 'title'  # i.e: it's not the header row


@pytest.mark.asyncio
async def test_get_random_from_category_gets_random_row_within_category(tb):
    range_mock = MagicMock(DataRange)
    tb._sheet.get_named_range.return_value = range_mock
    range_mock.cells = [
        [MagicMock(spec=Cell, value=x[0], row=ind + 1)]
        for ind, x in enumerate(rows)
    ]

    for _ in range(10):
        e = await tb.get_from_category('quran')
        assert is_embed_valid(e)
        assert e.description == 'test1'

        e = await tb.get_from_category('hadith')
        assert is_embed_valid(e)
        assert e.description == 'test2'
