from bot import Bot


class Cog:
    def __init__(self, bot):
        self.bot: Bot = bot
        self.default_config = {'enabled': False, 'commands': {}}
        self.configurable = True

    @property
    def name(self):
        return type(self).__name__

    def config_for(self, guild_id):
        return self.bot.config_for(guild_id).get(self.name)
