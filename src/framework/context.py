from discord.ext import commands

from model.recursive_attr_dict import RecursiveAttrDict


class ConfigContext(commands.Context):
    @property
    def config(self):
        return self.bot.config_for(self.guild.id)

    @property
    def all_commands(self):
        ret = RecursiveAttrDict()
        for conf in self.config.values():
            ret.update(conf.commands)
        return ret

    @property
    def cog_config(self):
        return self.cog.config_for(self.guild.id)

    @property
    def cmd_config(self):
        return self.command.config_for(self.guild.id)
