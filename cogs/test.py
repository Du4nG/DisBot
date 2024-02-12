from gtts import gTTS
import nextcord
from nextcord import Member, Interaction, Embed, ui, ButtonStyle, FFmpegPCMAudio
from nextcord.ext.commands import Bot, Cog

YOUTUBE_SUBSCRIPTION_LINK = 'https://www.youtube.com/channel/UCtVmdbgtwpI9oMQGYjezS9w'
GITHUB_LINK = 'https://github.com/Du4nG/DisBot'
FACEBOOK_LINK = 'https://www.facebook.com/queo.stn'

class Buttonsss(ui.View):
    def __init__(self):
        super().__init__()

    @ui.button(label='Dũng Học Giỏi', style=ButtonStyle.red)
    async def youtube(self,  button: ui.Button, interaction: Interaction):
        # await interaction.send(YOUTUBE_SUBSCRIPTION_LINK)
        embed = Embed(title='Dũng Học Giỏi', 
                      description='YouTube',
                      color=0xCD201F,
                      url=YOUTUBE_SUBSCRIPTION_LINK)
        embed.set_thumbnail(url='https://yt3.googleusercontent.com/DGSVJrnl0bTUZ5FLhuJYO__k0zVrLFIU8QQKi1ywItUJBsNy-AFf7mS0P4f7-RZJgGckUjJ5aA=s176-c-k-c0x00ffffff-no-rj')
        await interaction.send(embed=embed)
        


class test(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(description='Giả mạo ai đó.')
    async def spoof(self, interaction: Interaction, member: Member, *, message):
        webhook = await interaction.channel.create_webhook(name=member.display_name)
        await webhook.send(message, username=member.display_name, avatar_url=member.avatar.url)
        await webhook.delete()

    @nextcord.slash_command(description='Xem tất cả command.')
    async def help(self, interaction: Interaction):
        embed = Embed(title='Command khả dụng  📌:', color=0x2B2D31)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name='!join', value='Gọi bot vào voice channel.')
        embed.add_field(name='/spoof', value='Giả mạo một user.')
        embed.add_field(name='/drop', value='Bỏ phiếu.')
        embed.add_field(name='!leave', value='Đá bot khỏi voice channel.')
        # embed.add_field(name='/play', value='Phát nhạc trên Youtube.')
        embed.add_field(name='/say', value='Chuyển text thành voice.')
        embed.add_field(name='/send_dm', value='Gửi tin nhắn riêng.')
        embed.add_field(name='gay', value='Đừng gõ từ này.')

        view = Buttonsss()
        view.add_item(ui.Button(label='DisBot',
                                style=ButtonStyle.link,
                                url=GITHUB_LINK))
        await interaction.send(embed=embed, view=view)

    @nextcord.slash_command(description='Chuyển text thành voice.')
    async def say(self, interaction: Interaction, *, message):
        user = interaction.user
        if user.voice:
            channel = user.voice.channel
            # Nếu bot ở voice channel khác với user thì rời để theo user.
            if interaction.guild.voice_client: 
                await interaction.guild.voice_client.disconnect()

            voice = await channel.connect()
            sound = gTTS(message, lang='vi')
            sound.save('audio/tts.mp3')
            source = FFmpegPCMAudio('audio/tts.mp3',
                                     options={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'},
                                     executable='bin/ffmpeg.exe')
            voice.play(source)  
            await interaction.response.send_message(f'{user.display_name} vừa nói "{message}"') # ephemeral=True để ẩn tin nhắn
        else:
            await interaction.send('Vào voice trước thằng lồz.')


def setup(bot: Bot):
    bot.add_cog(test(bot))
