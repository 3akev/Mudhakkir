import discord
from discord.ext.commands import group

from deprecated.sqlite_manager import SQLiteManager
from deprecated.tadhkeer_backend import TadhkeerBackend
from framework.cog import Cog


class TadhkeerCommands(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.db = SQLiteManager()
        self.backend = TadhkeerBackend()

        self.default_config['enabled'] = True
        self.default_config['channel_id'] = None
        self.default_config['interval_in_seconds'] = 86400

    @group()
    async def tadhkirah(self, ctx):
        if ctx.invoked_subcommand is not None:
            return

        data = self.db.get_hadith()
        # if table_name == 'quran':
        embeds = await self.backend.get_hadith(*data)
        # else:
        #     embed = await self.backend.get_hadith(*data)

        for embed in embeds:
            await ctx.send(embed=embed)

    @tadhkirah.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        self.default_config['channel_id'] = channel.id
        self.bot.configs.save(ctx.guild.id)
        await ctx.send("Alright, I'll be posting reminders in {} from now on.".format(channel.mention))

    @tadhkirah.command()
    async def quran(self, ctx):
        for embed in await self.backend.get_quran(*self.db.get_quran()):
            await ctx.send(embed=embed)

    @tadhkirah.command()
    async def hadith(self, ctx):
        for embed in await self.backend.get_hadith(*self.db.get_hadith()):
            await ctx.send(embed=embed)

    # submission
    @tadhkirah.group()
    async def submit(self, ctx):
        pass

    @submit.command()
    async def quran(self, ctx, surah_num: int, ayah_num: int, ayah_end=None):
        pass

    @submit.command()
    async def hadith(self, ctx, book_name: str, book_num: int, hadith_num=None):
        pass
