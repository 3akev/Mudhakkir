from cogs.owner.owner_commands import OwnerCommands


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
