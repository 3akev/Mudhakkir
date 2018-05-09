import os
import sqlite3
from unittest.mock import Mock

import pytest

from cogs.tadhkirah.sqlite_manager import SQLiteManager
from statics import parentDir

db_file = os.path.join(parentDir, 'tests/test_resources/tadhkirah.sqlite')


@pytest.fixture
def sq():
    yield SQLiteManager(db_file)


def test_get_cursor_returns_cursor(sq):
    assert isinstance(sq.get_cursor(), sqlite3.Cursor)


def test_commit_cursor_commits_changes_and_closes(sq):
    c = sq.get_cursor()
    sq.conn = Mock()
    sq.commit_cursor(c)

    assert sq.conn.commit.called
    assert sq.conn.close.called


def test_close_cursor_closes_cursor(sq):
    c = sq.get_cursor()
    sq.conn = Mock()
    sq.close_cursor(c)

    assert sq.conn.close.called


def test_add_quran_remove_quran_adds_row_to_quran_table_and_removes_it(sq):
    sq.add_quran(1, 1, 2)

    c = sq.get_cursor()
    c.execute("SELECT * FROM {tn} WHERE surah_num=1".format(tn=sq.quran_table))
    assert c.fetchone() == (1, 1, 2)
    sq.close_cursor(c)

    sq.remove_quran(1, 1, 2)

    c = sq.get_cursor()
    c.execute("SELECT * FROM {tn} WHERE surah_num=1".format(tn=sq.quran_table))
    assert c.fetchone() is None
    sq.close_cursor(c)


def test_add_hadith_remove_hadith_adds_row_to_hadith_table_and_removes_it(sq):
    sq.add_hadith('bukhari', 2, 1)

    c = sq.get_cursor()
    c.execute("SELECT * FROM {tn} WHERE book_id=0 AND book_num=2".format(tn=sq.hadith_table))
    assert c.fetchone() == (0, 2, 1)
    sq.close_cursor(c)

    sq.remove_hadith('bukhari', 2, 1)

    c = sq.get_cursor()
    c.execute("SELECT * FROM {tn} WHERE book_id=0 AND book_num=2".format(tn=sq.hadith_table))
    assert c.fetchone() is None
    sq.close_cursor(c)


def test_get_quran_gets_random_quran_row(sq):
    assert sq.get_quran() is not None


def test_get_hadith_gets_random_hadith_row(sq):
    assert sq.get_hadith() is not None


def test_get_random_gets_random_row(sq):
    table, result = sq.get_random()
    assert result is not None
