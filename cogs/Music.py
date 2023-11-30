import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord import FFmpegPCMAudio, Interaction

class Music(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(description='Nhập tên bài hát, bot sẽ phát kết quả tìm thấy đầu tiên trên Youtube.')
    async def play(self, interaction: nextcord.Interaction, *, song: str):
        # Get the user's voice channel
        user = interaction.user
        voice_channel = user.voice.channel

        if not voice_channel:
            await interaction.send("Bạn cần vào một voice channel trước.")
            return

        # Create a YouTube URL from the search query
        youtube_url = f"https://www.youtube.com/results?search_query={nextcord.utils.escape_markdown(song)}"

        # Join the user's voice channel
        voice_client = await voice_channel.connect()
        print(youtube_url)
        # Play the YouTube video directly using the URL
        source = nextcord.FFmpegPCMAudio(youtube_url,
                                         options={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'},
                                         executable=r'bin\ffmpeg.exe')
        voice_client.play(source)

def setup(bot: Bot):
    bot.add_cog(Music(bot))
