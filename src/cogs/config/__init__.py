from cogs.config.config_commands import ConfigCommands


def setup(bot):
    bot.add_cog(ConfigCommands(bot))
