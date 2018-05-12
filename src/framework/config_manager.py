import os

from framework import ArgCommand
from model.file import YamlFile
from model.recursive_attr_dict import RecursiveAttrDict
from statics import storageDir


class ConfigManager:  # TODO: derive per-cog file management
    def __init__(self, bot):
        self.bot = bot
        self.configs_map = {}

    def get(self, guild_id):
        return self.configs_map.get(str(guild_id))

    def populate_config(self, guild_id):
        conf = {}
        saved_conf = YamlFile(os.path.join(storageDir, str(guild_id), 'config.yaml')).read()

        for cog_key, cog_inst in self.bot.cogs.items():

            # Populate config for each cog
            saved_cog_conf = saved_conf.get(cog_key)
            if saved_cog_conf is not None:
                conf[cog_key] = {}
                for k, v in cog_inst.default_config.items():
                    conf[cog_key][k] = saved_cog_conf.get(k) or v
            else:
                conf[cog_key] = cog_inst.default_config

            if not conf[cog_key].get('commands'):
                # Populate config for each command in cog
                conf[cog_key]['commands'] = {}
                for command in [obj for obj in type(cog_inst).__dict__.values() if isinstance(obj, ArgCommand)]:
                    conf[cog_key]['commands'][command.name] = command.default_config

        self.configs_map[str(guild_id)] = RecursiveAttrDict(conf)

    def save(self, guild_id):
        YamlFile(os.path.join(storageDir, str(guild_id), 'config.yaml')).write(self.get(guild_id))
