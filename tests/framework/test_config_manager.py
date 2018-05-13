from unittest.mock import MagicMock

import pytest

from bot import Bot
from framework.cog import Cog
from framework.command import command
from framework.config_manager import ConfigManager


class Cog1(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.default_config.update({'x': 3, 'y': 64})

    @command(conf={'enabled': True, 'cool': True})
    async def test1(self, ctx):
        pass

    @command(conf={'enabled': True, 'cool': False})
    async def test2(self, ctx):
        pass


class Cog2(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.default_config.update({'x': 435, 'y': 1341})

    @command(conf={'enabled': True, 'cost': 50})
    async def te1(self, ctx):
        pass

    @command(conf={'enabled': True, 'cost': 100})
    async def te2(self, ctx):
        pass


saved_conf = {
    'Cog1': {
        'enabled': True,
        'x': 5,
        'y': 30,
        'commands': {
            'test1': {
                'enabled': False,
                'cool': True
            }
        }
    }
}


@pytest.fixture()
def conf(monkeypatch):
    yamlfile = MagicMock()
    yamlfile().read = lambda: saved_conf
    monkeypatch.setattr('framework.config_manager.YamlFile', yamlfile)

    bot = MagicMock(Bot)
    c1 = Cog1(bot)
    c2 = Cog2(bot)
    bot.cogs = {
        c1.name: c1,
        c2.name: c2
    }
    yield ConfigManager(bot)


def test_populate_config_populates_configs(conf):
    conf.populate_config(0)

    assert conf.get(0) == {
        'Cog1': {
            'enabled': True,
            'x': 5,
            'y': 30,
            'commands': {
                'test1': {
                    'enabled': False,
                    'cool': True
                },
                'test2': {
                    'enabled': True,
                    'cool': False
                }
            }
        },
        'Cog2': {
            'enabled': False,
            'x': 435,
            'y': 1341,
            'commands': {
                'te1': {
                    'enabled': True,
                    'cost': 50
                },
                'te2': {
                    'enabled': True,
                    'cost': 100
                }
            }
        }
    }
