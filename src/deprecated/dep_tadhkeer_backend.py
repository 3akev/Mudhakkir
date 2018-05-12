import re

import aiohttp

import discord
from bs4 import BeautifulSoup

from deprecated.database_statics import hadith_api_names, hadith_book_translation_dict
from model.recursive_attr_dict import RecursiveAttrDict


class TadhkeerBackend:
    quran_api_link = 'http://api.alquran.cloud/surah/{0}/editions/ar,en.sahih?offset={1}&limit={2}'
    hadith_link = 'http://sunnah.com/{0}/{1}/{2}'
    tafsir_url = 'http://www.recitequran.com/en/tafsir/en.ibn-kathir/{0}:{1}'

    def __init__(self):
        self.client_session = aiohttp.ClientSession()

    def _make_quran_embed(self, title, surah_name, surah_number, ayahs, author_name):
        embed = discord.Embed(
            title=title,
            description='{0} - {1}'.format(surah_name, surah_number),
            colour=65280  # that is, green
        )
        for ayah in ayahs:
            ayah = RecursiveAttrDict(ayah)
            embed.add_field(
                name='{0}'.format(ayah.numberInSurah),
                value=ayah.text,
                inline=False
            )

        embed.url = self.tafsir_url.format(surah_number, ayahs[0]['numberInSurah'])
        embed.set_author(name=author_name)
        return embed

    def _get_quran_link(self, surah_num, ayah_num, ayah_end):
        limit = ayah_end - (ayah_num - 1) if ayah_end is not None else 1
        link = self.quran_api_link.format(surah_num, ayah_num - 1, limit)
        return link

    async def _fetch_quran(self, surah_num: int, ayah_num: int, ayah_end=None):
        link = self._get_quran_link(surah_num, ayah_num, ayah_end)
        async with self.client_session.get(link) as r:
            return await r.json()

    def _process_response(self, resp):
        ar = RecursiveAttrDict(resp['data'][0])
        en = RecursiveAttrDict(resp['data'][1])

        ar_embed = self._make_quran_embed('تفسير', ar.name, ar.number, ar.ayahs, 'تذكرة')
        en_embed = self._make_quran_embed('Tafsir', en.englishName, en.number, en.ayahs, 'Reminder')

        return ar_embed, en_embed

    async def get_quran(self, surah_num: int, ayah_num: int, ayah_end=None):
        resp = await self._fetch_quran(surah_num, ayah_num, ayah_end)

        return self._process_response(resp)

    @staticmethod
    def _clean_whitespace(text):
        text = re.sub(" +", " ", text)
        text = re.sub("\n+", "\n", text)
        return text

    @staticmethod
    def _make_embed_titles(ar_book_name, en_book_name, book_num, hadith_num):
        ar_title = '{0}'.format(ar_book_name)

        if hadith_num:
            ar_title += ' كتاب {0} حديث {1}'.format(book_num, hadith_num)
        else:
            ar_title += ' حديث {0}'.format(book_num)

        en_title = '{0}'.format(en_book_name)

        if hadith_num:
            en_title += ' book {0} Hadith {1}'.format(book_num, hadith_num)
        else:
            en_title += ' Hadith {0}'.format(book_num)

        return ar_title, en_title

    @staticmethod
    def _make_hadith_embed(title, hadith_text, narrator=None):
        embed = discord.Embed(
            title=title,
            description=('{0}\n***{1}***'.format(narrator, hadith_text) if narrator else hadith_text),
            colour=65280  # that is, green
        )

        return embed

    def _extract_hadith(self, html):
        soup = BeautifulSoup(html, "html.parser")

        en_narrator = self._clean_whitespace(soup.find('div', attrs={'class': 'hadith_narrated'}).text)
        en_text = self._clean_whitespace(soup.find('div', attrs={'class': 'text_details'}).text)
        ar_narrator = self._clean_whitespace(soup.find('span', attrs={'class': 'arabic_sanad'}).text)
        ar_text = self._clean_whitespace(soup.find('span', attrs={'class': 'arabic_text_details'}).text)

        return (en_narrator, en_text), (ar_narrator, ar_text)

    async def _fetch_hadith(self, book_name, book_num, hadith_num):
        link = self.hadith_link.format(book_name, book_num, hadith_num or 1)
        async with self.client_session.get(link) as r:
            resp = await r.text()

        return self._extract_hadith(resp)

    async def get_hadith(self, book_id: int, book_num: int, hadith_num=None):
        book_name = hadith_api_names[book_id]
        (en_narrator, en_text), (ar_narrator, ar_text) = await self._fetch_hadith(book_name, book_num, hadith_num)
        en_book_name, ar_book_name = hadith_book_translation_dict[book_name]
        ar_title, en_title = self._make_embed_titles(ar_book_name, en_book_name, book_num, hadith_num)

        ar_embed = self._make_hadith_embed(ar_title, ar_text, ar_narrator)
        en_embed = self._make_hadith_embed(en_title, en_text, en_narrator)

        return ar_embed, en_embed
