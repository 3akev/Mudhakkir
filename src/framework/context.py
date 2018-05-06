from discord.ext import commands


class ConfigContext(commands.Context):
    @property
    def config(self):
        return self.bot.configs.get(self.guild.id)
