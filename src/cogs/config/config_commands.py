from framework import command
from framework.cog import Cog


class ConfigCommands(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.default_config['enabled'] = True
        self.configurable = False

    def _enable_disable_conf(self, ctx, cog_or_command, value):
        if cog_or_command in ctx.config:  # it's a cog
            if self.bot.cogs.get(cog_or_command).configurable:
                ctx.config[cog_or_command].enabled = value
                self.bot.configs.save(ctx.guild.id)
                return True
            else:
                return "This cog isn't configurable."

        elif cog_or_command in ctx.all_commands:  # it's a command
            ctx.all_commands[cog_or_command].enabled = value
            self.bot.configs.save(ctx.guild.id)
            return True

        else:
            return "Invalid cog or command name."

    @command()
    async def enable(self, ctx, cog_or_command):
        ret = self._enable_disable_conf(ctx, cog_or_command, True)
        if ret is True:  # success
            await ctx.send("Enabled {} successfully.".format(cog_or_command))
        else:
            await ctx.send(ret)

    @command()
    async def disable(self, ctx, cog_or_command):
        ret = self._enable_disable_conf(ctx, cog_or_command, False)
        if ret is True:  # success
            await ctx.send("Disabled {} successfully.".format(cog_or_command))
        else:
            await ctx.send(ret)
