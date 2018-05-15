from framework import command
from framework.cog import Cog
from framework.embed import CoolEmbed


class MiscCommands(Cog):
    invite_url = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0"
    server_invite = 'https://discord.gg/abHDUU6'
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1ApLbdkjcMv2-mPB5FzWd2gz3fSjMQzEjOvfl5HiUo3o"
    doc_url = "https://docs.google.com/document/d/1sXlGqsRYCHpM8gtm21E6uXdNe9DFYTI8KL-vcv8pjJA"
    github_url = "https://github.com/ChemicalInk/Mudhakkir"

    def __init__(self, bot):
        super().__init__(bot)
        self.default_config['enabled'] = True
        self.configurable = False

    @command()
    async def invite(self, ctx):
        app_info = await self.bot.application_info()
        url = self.invite_url.format(app_info.id)
        await ctx.send(url)

    @command()
    async def support(self, ctx):
        await ctx.send("For support, join this server and drop ala#2941 a mention: " + self.server_invite)

    @command()
    async def contribute(self, ctx):
        s = (
            "You can help us in numerous ways:\n"
            "  1) Making dua that Allah accepts this project and rewards everyone involved.\n"
            "  2) Suggesting a reminder in [this doc]({0}).\n"
            "  3) Contributing code and ideas on the bot's [GitHub repository]({1}) and [Discord server]({2})."
        ).format(self.doc_url, self.github_url, self.server_invite)
        embed = CoolEmbed(description=s)
        await ctx.send(embed=embed)

    @command()
    async def sheet(self, ctx):
        await ctx.send('View the sheet whence this bot gets its reminders here: ' + self.spreadsheet_url)
