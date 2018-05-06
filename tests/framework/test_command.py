from unittest.mock import MagicMock

import pytest
from discord.ext.commands import Context, BadArgument
from discord.ext.commands.view import StringView

from framework import ArgCommand


def get_ctx(string):
    return Context(
        prefix='.',
        message=MagicMock(),

        view=StringView(string)
    )


def cb_positional(ctx, num: int, x: str = 'stuff', *args):
    pass


def cb_keyword_only(ctx, num: int, *, cool, very_cool: bool = True, **kwargs):
    pass


test_table = (
    (
        cb_positional, (".test 30 thing", [30, 'thing'], {})
    ),
    (
        cb_positional, (".test 40", [40, 'stuff'], {})
    ),
    (
        cb_positional, ('.test num=40 x="cool stuff"', [], {'num': 40, 'x': "cool stuff"})
    ),
    (
        cb_positional, ('.test 40 stuff magic lots of args here dude', [40, "stuff", "magic", "lots", "of", "args", "here", "dude"], {})
    ),
    (
        cb_keyword_only, ('.test 90 cool=yep very_cool=False test_driven=True', [90], {'cool': 'yep', 'very_cool': False, 'test_driven': 'True'})
    ),
    (
        cb_keyword_only, ('.test 40 cool=yep', [40], {'cool': 'yep', 'very_cool': True})
    )
)


@pytest.mark.asyncio
async def test_parse_arguments_parses_arguments(event_loop):
    for callback, (string, result_args, result_kwargs) in test_table:
        ctx = get_ctx(string)

        cmd = ArgCommand('test', callback)
        await cmd._parse_arguments(ctx)

        assert ctx.args == [ctx, *result_args]
        assert ctx.kwargs == result_kwargs

        callback(*ctx.args, **ctx.kwargs)


broken_test_table = (
    (
        cb_positional, '.test word'
    ),
    (
        cb_positional, '.test word "another word" keyword=argument'
    ),
    (
        cb_keyword_only, '.test word another'
    )
)


@pytest.mark.asyncio
async def test_parse_arguments_raises_badargument_if_argument_bad(event_loop):
    for callback, string in broken_test_table:
        ctx = get_ctx(string)

        cmd = ArgCommand('test', callback)

        with pytest.raises(BadArgument):
            await cmd._parse_arguments(ctx)
