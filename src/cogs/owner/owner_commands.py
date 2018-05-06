from framework import command
from framework.cog import Cog


class OwnerCommands(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_config['enabled'] = True

    @command()
    async def kill(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.close()
