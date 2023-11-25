from nextcord.ext.commands import Bot, Cog, Context
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio

class Voice(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    '''
    Nếu không có ai join sẵn vào một voice channel, channel đó xem như không tồn tại.
    '''
    @commands.command(pass_context=True)
    async def join(self, ctx: Context):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('songs/song_2018.mp3')
            voice.play(source)
            await ctx.send('Hello mấy cưng.')
        else:
            await ctx.send('M vào trước t mới vào.')

    @commands.command()
    async def leave(self, ctx: Context):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send('Bố đi đây.')
        else:
            await ctx.send('Có trong voice đéo đâu mà rời.')

    @commands.command()
    async def add(self, ctx: Context, a: int, b: int):
        await ctx.send(a + b)

def setup(bot: Bot):
    bot.add_cog(Voice(bot))
