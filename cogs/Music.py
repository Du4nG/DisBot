import nextcord
from nextcord.ext.commands import Bot, Cog, Context
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio
import youtube_dl

class Music(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # @nextcord.slash_command(description='Play a YouTube video in the voice channel.')
    @commands.command()
    async def play(self, ctx: Context, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            print(url2)

        voice_channel = ctx.voice_client
        voice_channel.play(FFmpegPCMAudio(url2))

def setup(bot: Bot):
    bot.add_cog(Music(bot))
