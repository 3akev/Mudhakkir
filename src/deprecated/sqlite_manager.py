import random

from cogs.tadhkirah.database_statics import hadith_api_names
from statics import databaseFile
import sqlite3


class SQLiteManager:
    quran_table = 'quran'
    hadith_table = 'hadith'

    def __init__(self, database_file=databaseFile):
        self.conn: sqlite3.Connection = None
        self.c = None
        self.database_file = database_file

    def get_cursor(self) -> sqlite3.Cursor:
        self.conn = sqlite3.connect(self.database_file)
        return self.conn.cursor()

    def commit_cursor(self, c):
        c.close()
        self.conn.commit()
        self.conn.close()

    def close_cursor(self, c):
        c.close()
        self.conn.close()

    def _change_quran_table(self, sql_cmd, surah, ayah, ayah_end=None):
        c = self.get_cursor()
        c.execute(sql_cmd.format(
            tn=self.quran_table,
            surah=surah,
            ayah=ayah,
            ayah_end=ayah_end
        ))
        self.commit_cursor(c)

    def add_quran(self, surah, ayah, ayah_end=None):
        sql = "INSERT INTO {tn} (surah_num, ayah_num"
        sql += ", ayah_num_end) " if ayah_end is not None else ') '
        sql += "VALUES ({surah}, {ayah}"
        sql += ", {ayah_end}) " if ayah_end is not None else ')'

        self._change_quran_table(sql, surah, ayah, ayah_end)

    def remove_quran(self, surah, ayah, ayah_end=None):
        sql = "DELETE FROM {tn} WHERE surah_num={surah} AND ayah_num={ayah}"
        if ayah_end is not None:
            sql += " AND ayah_num_end={ayah_end}"

        self._change_quran_table(sql, surah, ayah, ayah_end)

    def _change_hadith_table(self, sql_cmd, book_name, book_num, hadith_num=None):
        book_id = hadith_api_names.index(book_name)
        c = self.get_cursor()

        c.execute(sql_cmd.format(
            tn=self.hadith_table,
            book_id=book_id,
            book_num=book_num,
            hadith_num=hadith_num
        ))
        self.commit_cursor(c)

    def add_hadith(self, book_name, book_num, hadith_num=None):
        sql = "INSERT INTO {tn} (book_id, book_num"
        sql += ", hadith_num) " if hadith_num is not None else ") "
        sql += "VALUES ({book_id}, {book_num}"
        sql += ", {hadith_num})" if hadith_num is not None else ")"

        self._change_hadith_table(sql, book_name, book_num, hadith_num)

    def remove_hadith(self, book_name, book_num, hadith_num=None):
        sql = "DELETE FROM {tn} WHERE book_id={book_id} AND book_num={book_num}"
        if hadith_num is not None:
            sql += " AND hadith_num={hadith_num}"

        self._change_hadith_table(sql, book_name, book_num, hadith_num)

    def _get_random_from(self, table):
        c = self.get_cursor()
        c.execute("SELECT * FROM {tn} ORDER BY RANDOM() LIMIT 1".format(tn=table))
        ret = c.fetchone()
        self.close_cursor(c)
        return ret

    def get_random(self):
        table = random.choice([self.quran_table, self.hadith_table])
        return table, self._get_random_from(table)

    def get_hadith(self):
        return self._get_random_from(self.hadith_table)

    def get_quran(self):
        return self._get_random_from(self.quran_table)
