from framework import command
from framework.cog import Cog


class MiscCommands(Cog):
    invite_url = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0"

    def __init__(self, bot):
        super().__init__(bot)
        self.default_config['enabled'] = True
        self.configurable = False

    @command()
    async def invite(self, ctx):
        app_info = await self.bot.application_info()
        url = self.invite_url.format(app_info.id)
        await ctx.send(url)
