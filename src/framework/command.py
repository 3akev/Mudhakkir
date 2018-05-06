import discord
from discord.ext import commands
from discord.ext.commands import CommandError, BadArgument, DisabledCommand

from model import argparser


class ArgCommand(commands.Command):
    def __init__(self, name, callback, **kwargs):
        super().__init__(name, callback, **kwargs)
        self.default_config = kwargs.get('default_config')

    async def _verify_checks(self, ctx):
        if not ctx.config[ctx.cog].enabled:
            raise DisabledCommand("Cog {} is disabled.".format(ctx.cog))
        elif not ctx.config[ctx.cog].commands[self].enabled:
            raise DisabledCommand("Command {} is disabled.".format(self))
        else:
            super()._verify_checks(ctx)

    async def _parse_arguments(self, ctx):
        ctx.args = [ctx] if self.instance is None else [self.instance, ctx]
        ctx.kwargs = {}
        args = ctx.args
        kwargs = ctx.kwargs

        iterator = iter(self.params.items())

        if self.instance is not None:
            # we have 'self' as the first parameter so just advance
            # the iterator and resume parsing
            try:
                next(iterator)
            except StopIteration:
                fmt = 'Callback for {0.name} command is missing "self" parameter.'
                raise discord.ClientException(fmt.format(self))

        # next we have the 'ctx' as the next parameter
        try:
            next(iterator)
        except StopIteration:
            fmt = 'Callback for {0.name} command is missing "ctx" parameter.'
            raise discord.ClientException(fmt.format(self))

        raw_args, raw_kwargs = argparser.parse(ctx.view.buffer)

        for name, param in iterator:
            if param.kind is param.POSITIONAL_OR_KEYWORD:  # i.e: normal args
                is_required = param.default is param.empty
                if name in raw_kwargs:
                    kwargs[name] = await self.convert_arg(ctx, param, raw_kwargs[name])
                elif len(raw_args) > 0:  # there's still some args
                    args.append(await self.convert_arg(ctx, param, raw_args.pop(0)))
                elif not is_required:  # it's neither in kwargs nor args, but there's a default value
                    args.append(param.default)
                else:
                    raise BadArgument(f'Required argument {name} not supplied')

            elif param.kind is param.KEYWORD_ONLY:  # i.e: after *,
                is_required = param.default is param.empty
                if name in raw_kwargs:
                    kwargs[name] = await self.convert_arg(ctx, param, raw_kwargs[name])
                elif not is_required:
                    kwargs[name] = param.default
                else:
                    raise BadArgument(f'Required keyword only argument {name} not supplied')

            elif param.kind is param.VAR_POSITIONAL:  # i.e: *args
                for arg in raw_args:
                    if arg != '':
                        args.append(await self.convert_arg(ctx, param, arg))

            elif param.kind is param.VAR_KEYWORD:  # i.e: **kwargs
                for k, v in raw_kwargs.items():
                    if k not in kwargs:
                        kwargs[k] = await self.convert_arg(ctx, param, v)

    async def convert_arg(self, ctx, param, arg):
        converter = self._get_converter(param)

        try:
            return await self.do_conversion(ctx, converter, arg)
        except CommandError as e:
            raise e
        except Exception as e:
            try:
                name = converter.__name__
            except AttributeError:
                name = converter.__class__.__name__

            raise BadArgument('Converting to "{}" failed for parameter "{}".'.format(name, param.name)) from e
