import random
from datetime import datetime

import discord
from discord.embeds import EmptyEmbed

from model.recursive_attr_dict import RecursiveAttrDict


class CoolEmbed(discord.Embed):
    def __init__(self, **kwargs):
        if isinstance(kwargs.get('colour'), str):
            kwargs['colour'] = int('0x{}'.format(kwargs.get('colour')), 16)

        super().__init__(**kwargs)
        if self.timestamp is EmptyEmbed:
            self.timestamp = datetime.now()
        if self.colour is EmptyEmbed:
            self.colour = random.randint(0, 16777215)


def get_embed(data):
    data = RecursiveAttrDict({k: v or EmptyEmbed for k, v in data.items()})

    embed = CoolEmbed(
        title=data.title,
        description=data.description,
        url=data.url,
        colour=data.colour
    ).set_footer(
        text=data.footer_text,
        icon_url=data.footer_icon_url
    )

    if data.author_name is not EmptyEmbed:
        embed.set_author(
            name=data.author_name,
            url=data.author_url,
            icon_url=data.author_icon_url
        )
    if data.image_url is not EmptyEmbed:
        embed.set_image(url=data.image_url)
    if data.thumbnail_url is not EmptyEmbed:
        embed.set_thumbnail(url=data.thumbnail_url)

    return embed
