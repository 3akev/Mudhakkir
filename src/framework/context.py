from discord.ext import commands


class ConfigContext(commands.Context):
    @property
    def config(self):
        return self.bot.config_for(self.guild.id)

    @property
    def all_commands(self):
        return [conf.commands for conf in self.config.values()]

    @property
    def cog_config(self):
        return self.cog.config_for(self.guild.id)

    @property
    def cmd_config(self):
        return self.command.config_for(self.guild.id)
