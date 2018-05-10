import discord
from discord.ext.commands import group

from cogs.tadhkirah.tadhkeer_backend import TadhkeerBackend
from framework.cog import Cog


class TadhkeerCommands(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.backend = TadhkeerBackend(bot.loop)

        self.default_config['enabled'] = True
        self.default_config['channel_id'] = None
        self.default_config['interval_in_seconds'] = 86400

    @group()
    async def tadhkirah(self, ctx):
        if ctx.invoked_subcommand is not None:
            return

        embed = await self.backend.get_random()
        await ctx.send(embed=embed)

    @tadhkirah.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        self.default_config['channel_id'] = channel.id
        self.bot.configs.save(ctx.guild.id)
        await ctx.send("Alright, I'll be posting reminders in {} from now on.".format(channel.mention))

    # submission
    @tadhkirah.group()
    async def submit(self, ctx):
        pass
