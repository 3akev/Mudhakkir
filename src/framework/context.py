from discord.ext import commands


class ConfigContext(commands.Context):
    @property
    def config(self):
        return self.bot.configs.get(self.guild.id)

    @property
    def cog_config(self):
        return self.config.get(str(type(self.cog)))

    @property
    def cmd_config(self):
        return self.cog_config.commands.get(self.command.name)
