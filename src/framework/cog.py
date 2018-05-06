from bot import Bot


class Cog:
    def __init__(self, bot):
        self.bot: Bot = bot

    configurable = True
    default_config = {'enabled': False, 'commands': {}}
