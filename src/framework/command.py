from discord.ext import commands
from discord.ext.commands import DisabledCommand
from discord.ext.commands.core import hooked_wrapped_callback
from discord.ext.commands import command as old_command


def command(name=None, conf=None, **attrs):
    return old_command(
        name,
        ConfCommand,
        default_config=conf,
        **attrs
    )


def group(name=None, conf=None, **attrs):
    return old_command(
        name,
        ConfGroup,
        default_config=conf,
        **attrs
    )


class ConfCommand(commands.Command):
    def __init__(self, name, callback, **kwargs):
        super().__init__(name, callback, **kwargs)
        self.default_config = kwargs.get('default_config') or {'enabled': True}

    async def _verify_checks(self, ctx):
        if not ctx.cog_config.enabled:
            raise DisabledCommand("Cog {} is disabled.".format(ctx.cog.name))
        elif not ctx.cmd_config.enabled:
            raise DisabledCommand("Command {} is disabled.".format(self.name))
        else:
            super()._verify_checks(ctx)

    def config_for(self, guild_id):
        return self.instance.config_for(guild_id).commands.get(self.name)


class ConfGroup(commands.GroupMixin, ConfCommand):
    def __init__(self, **attrs):
        self.invoke_without_command = attrs.pop('invoke_without_command', False)
        super().__init__(**attrs)

    async def invoke(self, ctx):
        early_invoke = not self.invoke_without_command
        if early_invoke:
            await self.prepare(ctx)

        view = ctx.view
        previous = view.index
        view.skip_ws()
        trigger = view.get_word()

        if trigger:
            ctx.subcommand_passed = trigger
            ctx.invoked_subcommand = self.all_commands.get(trigger, None)

        if early_invoke:
            injected = hooked_wrapped_callback(self, ctx, self.callback)
            await injected(*ctx.args, **ctx.kwargs)

        if trigger and ctx.invoked_subcommand:
            ctx.invoked_with = trigger
            await ctx.invoked_subcommand.invoke(ctx)
        elif not early_invoke:
            # undo the trigger parsing
            view.index = previous
            view.previous = previous
            await super().invoke(ctx)

    async def reinvoke(self, ctx, *, call_hooks=False):
        early_invoke = not self.invoke_without_command
        if early_invoke:
            ctx.command = self
            await self._parse_arguments(ctx)

            if call_hooks:
                await self.call_before_hooks(ctx)

        view = ctx.view
        previous = view.index
        view.skip_ws()
        trigger = view.get_word()

        if trigger:
            ctx.subcommand_passed = trigger
            ctx.invoked_subcommand = self.all_commands.get(trigger, None)

        if early_invoke:
            try:
                await self.callback(*ctx.args, **ctx.kwargs)
            except:
                ctx.command_failed = True
                raise
            finally:
                if call_hooks:
                    await self.call_after_hooks(ctx)

        if trigger and ctx.invoked_subcommand:
            ctx.invoked_with = trigger
            await ctx.invoked_subcommand.reinvoke(ctx, call_hooks=call_hooks)
        elif not early_invoke:
            # undo the trigger parsing
            view.index = previous
            view.previous = previous
            await super().reinvoke(ctx, call_hooks=call_hooks)

    def command(self, *args, **kwargs):
        """A shortcut decorator that invokes :func:`.command` and adds it to
        the internal command list via :meth:`~.GroupMixin.add_command`.
        """
        def decorator(func):
            result = command(*args, **kwargs)(func)
            self.add_command(result)
            return result

        return decorator

    def group(self, *args, **kwargs):
        """A shortcut decorator that invokes :func:`.group` and adds it to
        the internal command list via :meth:`~.GroupMixin.add_command`.
        """
        def decorator(func):
            result = group(*args, **kwargs)(func)
            self.add_command(result)
            return result

        return decorator
