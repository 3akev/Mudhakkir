from discord.ext import commands


class ConfigContext(commands.Context):
    @property
    def config(self):
        return self.bot.configs.get(self.guild.id)

    @property
    def all_commands(self):
        return [conf.commands for conf in self.config.values()]

    @property
    def cog_config(self):
        return self.config.get(self.cog.name)

    @property
    def cmd_config(self):
        return self.cog_config.commands.get(self.command.name)
