#!python3
import asyncio
import logging
import traceback
import os

import discord
from discord.ext import commands
from discord.ext.commands import DisabledCommand, UserInputError

from config import description, PREFIX
from dropboxer import DropBoxer
from framework.context import ConfigContext
from framework.config_manager import ConfigManager
from statics import cogsDir


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            description=description,
            loop=asyncio.new_event_loop(),
        )

        self.configs = ConfigManager(self)

    async def on_ready(self):
        print(self.user.name, ' : ', self.user.id)
        await self.change_presence(status='dnd')

        DropBoxer.setLoop(self.loop)
        await DropBoxer.get()

        await self.change_presence(activity=discord.Game(name="{}help".format(PREFIX)), status='online')
        self._load_cogs()
        self.populate_configs()

        await DropBoxer.uploadLoop()

    async def on_message(self, message):
        ctx = await self.get_context(message, cls=ConfigContext)
        await self.invoke(ctx)

    def _load_cogs(self):
        print('Loading cogs...')
        for i in os.listdir(cogsDir):
            cogPackage = os.path.join(cogsDir, i)
            if os.path.isdir(cogPackage):
                if os.path.isfile(os.path.join(cogPackage, '__init__.py')):
                    try:
                        self.load_extension("cogs.{0}".format(i))
                    except Exception:
                        logging.error(f'Error on loading {i}: {traceback.format_exc()}')
        print('Loaded.')

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, (DisabledCommand, UserInputError)):
            await ctx.send(str(exception))
        else:
            await super().on_command_error(ctx, exception)

    async def on_guild_join(self, guild):
        self.configs.populate_config(guild.id)

    def populate_configs(self):
        for guild in self.guilds:
            self.configs.populate_config(guild.id)

    def config_for(self, guild_id):
        return self.configs.get(guild_id)


def main():
    while True:
        try:
            Bot().run(os.environ.get('DISCORD_TOKEN'))
        except Exception:
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    main()
