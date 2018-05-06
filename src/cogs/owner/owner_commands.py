from framework import command
from framework.cog import Cog


class OwnerCommands(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.default_config['enabled'] = True
        self.configurable = False

    @command()
    async def kill(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.close()
