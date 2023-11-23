from nextcord.ext.commands import Bot, Cog, Context
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio

class Voice(Cog):
    def __init__(self, client: Bot):
        self.client = client

    '''
    Nếu không có ai join sẵn vào một voice channel, channel đó xem như không tồn tại.
    '''
    @commands.command()
    async def join(self, ctx: Context):
        if ctx.author.voice:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            await ctx.send('Hello mấy cưng.')
            source = FFmpegPCMAudio('songs/song_2018.mp3')
            player = voice.play(source)
        else:
            await ctx.send('Đéo vào được.')

    @commands.command()
    async def leave(self, ctx: Context):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send('Bố đi đây.')
        else:
            await ctx.send('Có trong voice đéo đâu mà rời.')

def setup(client: Bot):
    client.add_cog(Voice(client))
