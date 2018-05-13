from discord.embeds import EmptyEmbed

from framework.embed import CoolEmbed


def is_embed_valid(embed):  # TODO: add appropriate url checking
    type(EmptyEmbed).__len__ = lambda s: 0

    footer_length = (len(embed.footer.text) if embed.footer else 0)
    ret = isinstance(embed, CoolEmbed)
    ret = ret and len(embed.title) < 256
    ret = ret and len(embed.description) < 2048
    ret = ret and len(embed.author.name) < 256
    ret = ret and len(embed.fields) < 25
    for field in embed.fields:
        ret = ret and len(field.name) < 256
        ret = ret and len(field.value) < 1024
    ret = ret and footer_length < 2048
    ret = ret and (
                   len(embed.title)
                   + len(embed.description)
                   + len(embed.author.name)
                   + sum(len(field.name) + len(field.value) for field in embed.fields)
                   + footer_length
           ) < 6000

    return ret
