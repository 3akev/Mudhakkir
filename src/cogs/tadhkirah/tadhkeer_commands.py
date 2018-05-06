import aiohttp

from framework.cog import Cog


class TadhkeerCommands(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.client_session = aiohttp.ClientSession()

