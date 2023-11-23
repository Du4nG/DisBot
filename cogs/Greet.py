from nextcord.ext.commands import Bot, Cog, Context
from nextcord.ext import commands
from nextcord import Member
from secret import TEST_CHANNEL_ID


class Greet(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send('Bố m đã online.')

    @Cog.listener()
    async def on_member_join(self, member: Member):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send(f'Chào mừng con gà {member}!')

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send(f'Cút mẹ m đi {member}.')

    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = self.client.get_channel(TEST_CHANNEL_ID)
        await channel.send(f'{user} bảo là {reaction}.')

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send('Lô con cặ')

def setup(client: Bot):
    client.add_cog(Greet(client))
