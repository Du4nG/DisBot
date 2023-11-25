import nextcord
from nextcord.ext.commands import Bot, Cog 
import youtube_dl
from nextcord import FFmpegPCMAudio

class Music(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(description='Play a YouTube video in the voice channel.')
    async def play(self, interaction: nextcord.Interaction, query: str):
        # Check if the user is in a voice channel
        if interaction.user.voice is None:
            await interaction.response.send_message('You must be in a voice channel to use this command.')
            return

        voice_channel = interaction.user.voice.channel

        # Create a YouTubeDL object
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Search and get the first result
            info = ydl.extract_info(query, download=False)
            url = info['entries'][0]['url']

            # Connect to the voice channel
            voice_client = await voice_channel.connect()

            # Play the audio
            voice_client.play(FFmpegPCMAudio(url), after=lambda e: print('done', e))

        await interaction.response.send_message(f'Now playing: {info["entries"][0]["title"]}')

def setup(bot: Bot):
    bot.add_cog(Music(bot))
