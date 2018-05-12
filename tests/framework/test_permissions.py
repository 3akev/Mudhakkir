from unittest.mock import MagicMock

import pytest
from discord import Permissions
from discord.ext.commands import MissingPermissions

from framework.permissions import permcheck


@pytest.fixture()
def ctx():
    c = MagicMock()
    c.bot.is_owner.return_value = False
    return c


def test_permcheck_returns_true_if_owner(ctx):
    ctx.bot.is_owner.return_value = True
    assert permcheck(ctx) is True


def test_permcheck_returns_true_if_author_has_permissions(ctx):
    p = {
        'kick_members': True,
        'ban_members': True
    }
    perms = Permissions.none()
    perms.update(**p)
    ctx.channel.permissions_for.return_value = perms

    assert permcheck(ctx, **p) is True


def test_permcheck_returns_true_if_admin_regardless_permissions(ctx):
    p = {
        'kick_members': True,
        'ban_members': True
    }
    perms = Permissions.none()
    perms.update(administrator=True)
    ctx.channel.permissions_for.return_value = perms

    assert permcheck(ctx, **p) is True


def test_permcheck_raises_error_if_not_enough_permissions(ctx):
    p = {
        'kick_members': True,
        'ban_members': True
    }
    ctx.channel.permissions_for.return_value = Permissions.none()

    with pytest.raises(MissingPermissions):
        permcheck(ctx, **p)
