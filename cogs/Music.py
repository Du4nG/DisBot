import nextcord
from nextcord.ext.commands import Bot, Cog, Context
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio

class Music(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # @nextcord.slash_command(description='Play a YouTube video in the voice channel.')
    @commands.command()
    async def play(self, ctx: Context, url: str):
        print(ctx.author)
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()
        audio_source = FFmpegPCMAudio(url, options={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'})
        voice_channel.play(audio_source)
        await ctx.send(f'Đang phát {url}')

def setup(bot: Bot):
    bot.add_cog(Music(bot))
