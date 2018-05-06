from collections import OrderedDict

import aiohttp
import random

import discord
from discord.ext.commands import group

from framework.cog import Cog
from model.recursive_attr_dict import RecursiveAttrDict


class TadhkeerCommands(Cog):
    ayat_in_quran = 6326
    quran_api_link = 'http://api.alquran.cloud/ayah/{0}/editions/ar,en.sahih'
    tafsir_url = 'http://quranx.com/Tafsir/Kathir/{0}.{1}'

    def __init__(self, bot):
        super().__init__(bot)
        self.client_session = aiohttp.ClientSession()
        self.default_config['enabled'] = True

    @group()
    async def tadhkirah(self, ctx):
        if ctx.invoked_subcommand is not None:
            return

        ayah_num = random.randint(1, self.ayat_in_quran)
        async with self.client_session.get(self.quran_api_link.format(ayah_num)) as r:
            resp = await r.json()

        ar = RecursiveAttrDict(resp['data'][0])
        en = RecursiveAttrDict(resp['data'][1])

        embed = discord.Embed(title='Tafsir', colour=random.randint(0, 16777215))

        fields = OrderedDict()
        fields['{0} - {1}:{2}'.format(en.surah.name, en.surah.number, en.numberInSurah)] = en.text

        embed.add_field(
            name='{0} - {1}:{2}'.format(ar.surah.name, ar.surah.number, ar.numberInSurah),
            value=ar.text,
            inline=False
        )
        embed.add_field(
            name='{0} - {1}:{2}'.format(en.surah.englishName, en.surah.number, en.numberInSurah),
            value=en.text,
            inline=False
        )

        embed.url = self.tafsir_url.format(ar.surah.number, ar.numberInSurah)
        embed.set_author(name='Tadhkirah | تذكرة')

        await ctx.send(embed=embed)
