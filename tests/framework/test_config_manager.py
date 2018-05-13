from copy import deepcopy
from unittest.mock import MagicMock

import pytest

from framework.command import ConfCommand
from framework.config_manager import ConfigManager

cog_conf1 = {'x': 3, 'y': 64, 'commands': {}}
cmd_conf1 = {'cool': True}
cls1 = MagicMock(default_config=cog_conf1)
type(cls1).x = ConfCommand("test1", lambda: None, default_config=cmd_conf1)
cls1.__str__ = lambda x: 'cls1'

cog_conf2 = {'x': 435, 'y': 1341, 'commands': {}}
cmd_conf2 = {'cost': 50}
cls2 = MagicMock(default_config=cog_conf2)
type(cls2).y = ConfCommand("test2", lambda: None, default_config=cmd_conf2)
cls2.__str__ = lambda x: 'cls2'

saved_conf = {
    'cls1': {
        'x': 34,
        'y': 644,
        'a': 43,
        'commands': {
            'test1': {'cool': False}
        }
    }
}


@pytest.fixture
def conf(monkeypatch):
    yamlfile = MagicMock()
    yamlfile().read = lambda: saved_conf
    monkeypatch.setattr('framework.config_manager.YamlFile', yamlfile)

    bot = MagicMock()
    cls1_def = deepcopy(cls1)
    cls1_def.default_config['z'] = 4
    bot.cogs = {
        str(cls1_def): cls1_def,
        str(cls2): cls2
    }

    yield ConfigManager(bot)


def test_init(conf):
    assert conf.configs_map == {}
    assert conf.bot is not None


def test_populate_config_populates_configs(conf):
    conf.populate_config(0)

    assert conf.get(0) == {
        'cls1': {
            'x': 34,
            'y': 644,
            'z': 4,
            'commands': {
                'test1': {'cool': False}
            }
        },
        'cls2': {
            'x': 435,
            'y': 1341,
            'commands': {
                'test2': {'cost': 50}
            }
        }
    }
