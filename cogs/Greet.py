from discord.ext.commands import Bot, Command, Cog, Context
from discord.ext import commands
from discord import Member
from secret import TEST_CHANNEL_ID


class Greet(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send('Lô con cặ')

    @Cog.listener()
    async def on_ready(self):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send('Bố m đây.')

    @Cog.listener()
    async def on_member_join(self, member: Member):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send(f'Chào mừng con gà {member} !')

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send(f'Cút mẹ m đi {member}.')

async def setup(client: Bot):
    await client.add_cog(Greet(client))
