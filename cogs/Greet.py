from discord.ext import commands
from discord import Member
from secret import TEST_CHANNEL_ID


class Greet(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send('Lô con cặ')

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send('Bot is ready.')

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send(f'Chào mừng con gà {member} !')

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send(f'Cút mẹ m đi {member}.')

def setup(client: commands.Bot):
    client.add_cog(Greet(client))
    