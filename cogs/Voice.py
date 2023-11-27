from nextcord.ext import commands
from nextcord.ext.commands import Bot, Cog, Context
from nextcord import FFmpegPCMAudio


class Voice(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx: Context):
        '''
        :   Gọi bot vào voice channel.
        '''
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            '''
            Đi theo người invoke lệnh.
            '''
            if ctx.guild.voice_client:
                await ctx.guild.voice_client.disconnect()

            voice = await channel.connect()
            source = FFmpegPCMAudio('audio/hello_may_cung.mp3',
                                    options={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'},
                                    executable=r'bin\ffmpeg.exe')
            voice.play(source)
            await ctx.send('Hello mấy cưng.')
        else:
            await ctx.send('M chưa vào sao t biết vào kênh nào.')

    @commands.command()
    async def leave(self, ctx: Context):
        '''
        :   Đá bot khỏi voice channel.
        '''
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send('Bố đi đây.')
        else:
            await ctx.send('Có trong voice đéo đâu mà rời.')


def setup(bot: Bot):
    bot.add_cog(Voice(bot))
