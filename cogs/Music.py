import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord import FFmpegPCMAudio, Interaction, SlashOption

class Music(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(description='Nhập tên bài hát, bot sẽ phát kết quả tìm thấy đầu tiên trên Youtube.')
    async def play(self, interaction: Interaction, *, song: str = SlashOption(description='Nhập tên bài hát.')):
        user = interaction.user
        voice_channel = user.voice.channel

        if not voice_channel:
            await interaction.send("Bạn cần vào một voice channel trước.")
            return

        youtube_url = f"https://www.youtube.com/results?search_query={nextcord.utils.escape_markdown(song)}"

        voice_client = await voice_channel.connect()
        print(youtube_url)
        source = FFmpegPCMAudio(youtube_url,
                                options={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'},
                                executable=r'bin\ffmpeg.exe')
        voice_client.play(source)

def setup(bot: Bot):
    bot.add_cog(Music(bot))
