from discord.ext import commands
from discord.ext.commands import MissingPermissions

from config import OWNER_IDS


def permcheck(ctx, **perms):
    if ctx.bot.is_owner(ctx.author):
        return True
    else:
        user_perms = ctx.channel.permissions_for(ctx.author)
        if getattr(user_perms, 'administrator', False):
            return True

        missing = [
            perm
            for perm, value in perms.items()
            if getattr(user_perms, perm, None) != value
        ]

        if not missing:
            return True
        else:
            raise MissingPermissions(missing)


def is_owner():
    async def predicate(ctx):
        return (await ctx.bot.is_owner(ctx.author)) or ctx.author.id in OWNER_IDS
    return commands.check(predicate)


def perms(**perms):
    def predicate(ctx):
        return permcheck(ctx, **perms)

    return commands.check(predicate)
