import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord import Member, Interaction
from secret import TEXT_CHANNEL_ID, SERVER_ID


class Greet(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # @Cog.listener()
    # async def on_ready(self):
    #     channel = self.bot.get_channel(TEXT_CHANNEL_ID)
    #     await channel.send('Bố m đã online.')

    @Cog.listener()
    async def on_member_join(self, member: Member):
        channel = self.bot.get_channel(TEXT_CHANNEL_ID)
        await channel.send(f'Chào mừng con gà {member}!')

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        channel = self.bot.get_channel(TEXT_CHANNEL_ID)
        await channel.send(f'Cút mẹ m đi {member}.')

    @nextcord.slash_command(description='Gửi lời chào.', guild_ids=[SERVER_ID])
    async def hello(self, interaction: Interaction):
        await interaction.send('Lô con cặ')

def setup(bot: Bot):
    bot.add_cog(Greet(bot))
