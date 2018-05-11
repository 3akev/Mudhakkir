import asyncio
import os
from datetime import datetime, timedelta

import discord
from discord.ext.commands import group

from cogs.tadhkirah.tadhkeer_backend import TadhkeerBackend
from framework import ArgCommand
from framework.cog import Cog
from model.file import YamlFile
from statics import storageDir


class TadhkeerCommands(Cog):
    data_file_name = 'tadhkeer.yaml'
    remind_interval_in_seconds = 86400

    def __init__(self, bot):
        super().__init__(bot)
        self.backend = TadhkeerBackend(bot.loop)

        self.default_config['enabled'] = True
        self.default_config['channel_id'] = None
        self.bot.loop.create_task(self.remind())

    @group()
    async def tadhkirah(self, ctx):
        if ctx.invoked_subcommand is not None:
            return

        await self.post_tadhkirah_in(ctx.channel)

    @tadhkirah.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        ctx.cog_config['channel_id'] = channel.id
        self.bot.configs.save(ctx.guild.id)
        await ctx.send("Alright, I'll be posting reminders in {}.".format(channel.mention))

    # submission
    @tadhkirah.command(cls=ArgCommand)
    async def submit(self, ctx):
        pass

    async def post_tadhkirah_in(self, channel):
        embed = await self.backend.get_random()
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

                if datetime.now() - last_tadhkirah_timestamp > timedelta(seconds=self.remind_interval_in_seconds):
                    await self.post_tadhkirah_in(guild.get_channel(conf.channel_id))
                    data_file.write({'last_tadhkirah_timestamp': datetime.now().timestamp()})

            await asyncio.sleep(900)
