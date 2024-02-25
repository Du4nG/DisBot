from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.commands import Bot, Cog
from .help import Help

class HelpOverride(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def help(self, interaction: Interaction):
        """
        :   Ghì đè help command.
        """
        await Help.help(self, interaction)


def setup(bot: Bot):
    bot.add_cog(HelpOverride(bot))
