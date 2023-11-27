import nextcord
from nextcord import Member, Interaction
from nextcord.ext import commands
from nextcord.ext.commands import Bot, Cog, Context
from secret import SERVER_ID


class test(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def spoof(self, ctx: Context, member: Member, *, message):
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=member.display_name)
        await webhook.send(message, username=member.display_name, avatar_url=member.avatar.url)
        await webhook.delete()

    # @nextcord.slash_command(description='Giả mạo ai đó.', guild_ids=[SERVER_ID])
    # async def spoof(self, ctx: Interaction, member: Member, *, message):
    #     # await ctx.message.delete()
    #     webhook = await ctx.channel.create_webhook(name=member.display_name)
    #     await webhook.send(message, username=member.display_name, avatar_url=member.avatar.url)
    #     await webhook.delete()

def setup(bot: Bot):
    bot.add_cog(test(bot))
