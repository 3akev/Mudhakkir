import aiohttp

import discord

from model.recursive_attr_dict import RecursiveAttrDict


class TadhkeerBackend:
    quran_api_link = 'http://api.alquran.cloud/surah/{0}/editions/ar,en.sahih?offset={1}&limit={2}'
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

    async def _fetch_quran(self, surah_num: int, ayah_num: int, ayah_end=None):
        limit = ayah_end - (ayah_num - 1) if ayah_end is not None else 1
        link = self.quran_api_link.format(surah_num, ayah_num - 1, limit)
        async with self.client_session.get(link) as r:
            return await r.json()

    async def get_quran(self, surah_num: int, ayah_num: int, ayah_end=None):
        resp = await self._fetch_quran(surah_num, ayah_num, ayah_end)

        ar = RecursiveAttrDict(resp['data'][0])
        en = RecursiveAttrDict(resp['data'][1])

        ar_embed = self._make_quran_embed('تفسير', ar.name, ar.number, ar.ayahs, 'تذكرة')
        en_embed = self._make_quran_embed('Tafsir', en.englishName, en.number, en.ayahs, 'Reminder')

        return ar_embed, en_embed

    async def _fetch_hadith(self, book_name, book_num, hadith_num):
        pass

    async def get_hadith(self, book_name: str, book_num: int, hadith_num=None):
        resp = await self._fetch_hadith(book_name, book_num, hadith_num)
