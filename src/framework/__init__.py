from discord.ext.commands import command as old_command

from framework.command import ArgCommand


def command(name=None, conf=None, **attrs):
    return old_command(
        name,
        ArgCommand,
        default_config=conf or {'enabled': True},
        **attrs
    )
