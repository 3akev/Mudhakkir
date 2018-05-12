import asyncio
import os
from datetime import datetime, timedelta

import discord
from discord.ext.commands import group

from cogs.tadhkirah.tadhkeer_backend import TadhkeerBackend
from framework.cog import Cog
from model.file import YamlFile
from statics import storageDir


class TadhkeerCommands(Cog):
    data_file_name = 'tadhkeer.yaml'

    def __init__(self, bot):
        super().__init__(bot)
        self.backend = TadhkeerBackend(bot.loop)

        self.default_config['enabled'] = True
        self.default_config['channel_id'] = None
        self.default_config['interval_in_seconds'] = 86400
        self.bot.loop.create_task(self.remind())

    @group()
    async def tadhkirah(self, ctx, category: str = None):
        if ctx.invoked_subcommand is not None:
            return

        await self.post_tadhkirah_in(ctx.channel, category)

    @tadhkirah.command()
    async def channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            channel_id = ctx.cog_config['channel_id']
            if channel_id is None:
                await ctx.send("I'm not posting reminders anywhere. You should set a channel!")
            else:
                channel = ctx.guild.get_channel(channel_id)
                await ctx.send("I'm posting reminders in {}.".format(channel.mention))
        else:
            ctx.cog_config['channel_id'] = channel.id
            self.bot.configs.save(ctx.guild.id)
            await ctx.send("Alright, I'll be posting reminders in {}.".format(channel.mention))

    @tadhkirah.command()
    async def interval(self, ctx, interval_in_days: float = None):
        if interval_in_days is None:
            interval_in_days = ctx.cog_config['interval_in_seconds'] / (60 * 60 * 24)
            await ctx.send("I'm posting reminders every {} days.".format(interval_in_days))
        else:
            ctx.cog_config['interval_in_seconds'] = interval_in_days * 24 * 60 * 60
            self.bot.configs.save(ctx.guild.id)
            await ctx.send("Alright, I'll be posting reminders every {} days.".format(interval_in_days))

    async def post_tadhkirah_in(self, channel, category = None):
        if category is None:
            embed = await self.backend.get_random()
        else:
            embed = await self.backend.get_from_category(category)

        await channel.send(embed=embed)

    async def remind(self):
        await self.bot.wait_until_ready()
        while True:
            for guild in self.bot.guilds:
                conf = self.config_for(guild.id)
                if not conf.enabled or conf.channel_id is None:
                    continue

                data_file = YamlFile(os.path.join(storageDir, str(guild.id), self.data_file_name))
                if data_file.read() == {}:
                    data_file.write({'last_tadhkirah_timestamp': 0})

                last_tadhkirah_timestamp = datetime.fromtimestamp(data_file.read().last_tadhkirah_timestamp)

                if datetime.now() - last_tadhkirah_timestamp > timedelta(seconds=conf.interval_in_seconds):
                    await self.post_tadhkirah_in(guild.get_channel(conf.channel_id))
                    data_file.write({'last_tadhkirah_timestamp': datetime.now().timestamp()})

            await asyncio.sleep(900)
