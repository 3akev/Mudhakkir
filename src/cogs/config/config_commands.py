from framework import command
from framework.cog import Cog
from framework.permissions import perms


class ConfigCommands(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.default_config['enabled'] = True
        self.configurable = False

    def _enable_disable_conf(self, ctx, cog_or_command, value):
        if self.bot.get_cog(cog_or_command):
            if self.bot.get_cog(cog_or_command).configurable:
                setattr(self.bot.get_cog(cog_or_command).config_for(ctx.guild.id), 'enabled', value)
                self.bot.configs.save(ctx.guild.id)
                return True
            else:
                return "This cog isn't configurable."

        elif self.bot.get_command(cog_or_command):
            setattr(self.bot.get_command(cog_or_command).config_for(ctx.guild.id), 'enabled', value)
            self.bot.configs.save(ctx.guild.id)
            return True

        else:
            return "Invalid cog or command name."

    @perms(kick_members=True)
    @command()
    async def enable(self, ctx, cog_or_command):
        """
        Enable a command or a category

        The name you give is case-sensitive.
        Note that some commands(such as this one) can not be configured.
        """
        ret = self._enable_disable_conf(ctx, cog_or_command, True)
        if ret is True:  # success
            await ctx.send("Enabled {} successfully.".format(cog_or_command))
        else:
            await ctx.send(ret)

    @perms(kick_members=True)
    @command()
    async def disable(self, ctx, cog_or_command):
        """
        Disable a command or a category

        The name you give is case-sensitive.
        Note that some commands(such as this one) can not be configured.
        """
        ret = self._enable_disable_conf(ctx, cog_or_command, False)
        if ret is True:  # success
            await ctx.send("Disabled {} successfully.".format(cog_or_command))
        else:
            await ctx.send(ret)
