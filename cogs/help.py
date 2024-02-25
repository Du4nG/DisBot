import nextcord
from nextcord import Member, Interaction, Embed, ui, ButtonStyle, SlashOption
from nextcord.ext.commands import Bot, Cog

YOUTUBE_SUBSCRIPTION_LINK = 'https://www.youtube.com/channel/UCtVmdbgtwpI9oMQGYjezS9w'
GITHUB_LINK = 'https://github.com/Du4nG/DisBot'
FACEBOOK_LINK = 'https://www.facebook.com/queo.stn'

class Buttonsss(ui.View):
    def __init__(self):
        super().__init__()

    @ui.button(label='Dũng Học Giỏi', style=ButtonStyle.red)
    async def youtube(self,  button: ui.Button, interaction: Interaction):
        embed = Embed(title='Dũng Học Giỏi', 
                      description='YouTube',
                      color=0xCD201F,
                      url=YOUTUBE_SUBSCRIPTION_LINK)
        embed.set_thumbnail(url='https://yt3.googleusercontent.com/DGSVJrnl0bTUZ5FLhuJYO__k0zVrLFIU8QQKi1ywItUJBsNy-AFf7mS0P4f7-RZJgGckUjJ5aA=s176-c-k-c0x00ffffff-no-rj')
        await interaction.send(embed=embed)


class Help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(description='Xem tất cả command.')
    async def help(self, interaction: Interaction):
        embed = Embed(title='📌  Command khả dụng:', color=0x2B2D31)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name='!join', value='Gọi bot vào voice channel.')
        embed.add_field(name='!leave', value='Đá bot khỏi voice channel.')
        embed.add_field(name='/spoof', value='Giả mạo một user.')
        embed.add_field(name='/drop', value='Bỏ phiếu.')
        embed.add_field(name='/say', value='Chuyển text thành voice.')
        embed.add_field(name='/dm', value='Gửi tin nhắn riêng.')
        embed.add_field(name='/price', value='Lấy giá coin theo USDT.')
        embed.add_field(name='/rate', value='Lấy tỷ giá một cặp coin.')
        embed.add_field(name='/alert', value='Tạo thông báo giá coin.')
        embed.add_field(name='/help', value='Thay vì !help.')
        embed.add_field(name='gay', value='Đừng gõ từ này.')

        view = Buttonsss()
        view.add_item(ui.Button(label='DisBot',
                                style=ButtonStyle.link,
                                url=GITHUB_LINK))
        await interaction.send(embed=embed, view=view)

    @nextcord.slash_command(description='Giả mạo ai đó.')
    async def spoof(self, interaction: Interaction,
                    member: Member = SlashOption(description='Chọn một user để giả mạo.'),
                    message: str = SlashOption(description='Nhập nội dung message.')
                    ):
        webhook = await interaction.channel.create_webhook(name=member.display_name)
        await webhook.send(message, username=member.display_name, avatar_url=member.avatar.url)
        await webhook.delete()

def setup(bot: Bot):
    bot.add_cog(Help(bot))
