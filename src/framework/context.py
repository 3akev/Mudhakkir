from discord.ext import commands


class ConfigContext(commands.Context):
    @property
    def cog_config(self):
        return self.cog.config_for(self.guild.id)

    @property
    def cmd_config(self):
        return self.command.config_for(self.guild.id)
