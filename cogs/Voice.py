from gtts import gTTS
from nextcord.ext import commands
from nextcord.ext.commands import Bot, Cog, Context
from nextcord import Member, VoiceState, FFmpegPCMAudio


class Voice(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.d = {
            'cngthnh'           : 'pặc cặc',
            '.iren3'            : 'minh',
            'nm0861'            : 'khang',
            'noodles10an2001'   : 'ân',
            'onglowf'           : 'long',
            'pmeee'             : 'my',
            'Tank_nkao_lon'     : 'tank',
            'Auditional Text'   : 'wefwefr',
        }

    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        """
        before.channel  :   voice channel trước đó của user.
        after.channel   :   voice channel mà user join vào.
        """
        guild = member.guild
        bot_voice_state = guild.voice_client

        if before.channel and after.channel is None:            # Không còn user trong voice channel.
            num_users = len(before.channel.members)
            if num_users <= 1 and bot_voice_state.channel == before.channel:  # Bot còn 1 mình trong voice channel.
                await bot_voice_state.disconnect()
        if after.channel is not None:
            if not bot_voice_state or bot_voice_state.channel != after.channel or after.channel != before.channel:
                if bot_voice_state:                              # Bot phải rời voice channel hiện tại trước khi
                    await bot_voice_state.disconnect()           # join channel mới, nếu không sẽ raise warning.      
                voice_client = await after.channel.connect()

                try:
                    sound = gTTS(f'Địt mẹ mày {self.d[member.name]}', lang='vi')
                except KeyError:
                    pass

                if member.name == 'du4zg':
                    sound = gTTS('Anh Dũng đẹp trai đã đến.', lang='vi')

                sound.save('audio/tts.mp3')
                source = FFmpegPCMAudio('audio/tts.mp3',
                                        options={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'},
                                        executable='bin/ffmpeg.exe')
                voice_client.play(source)


    @commands.command()
    async def join(self, ctx: Context):
        '''
        :   Gọi bot vào voice channel.
        '''
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            
            # Nếu bot ở voice channel khác với user thì rời để theo user.
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
