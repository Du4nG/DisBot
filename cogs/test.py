import nextcord
from nextcord import Member, Interaction, Embed, ui, ButtonStyle
from nextcord.ext import commands
from nextcord.ext.commands import Bot, Cog

class Buttons(ui.View):
    def __init__(self):
        super().__init__()


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
        embed = Embed(title='Help', description='Xem tất cả command.', color=0x5865f2)
        embed.add_field(name='!join', value='Gọi bot vào voice channel.')
        embed.add_field(name='/spoof', value='   Giả mạo một user.')
        embed.add_field(name='/drop', value='   Xổ menu.')
        embed.add_field(name='!leave', value='   Đá bot khỏi voice channel.')
        embed.add_field(name='/play', value='   Phát nhạc trên Youtube.')

        view = Buttons()
        view.add_item(ui.Button(label='GitHub', style=ButtonStyle.link, url='https://github.com/Du4nG/DisBot'))
        await interaction.send(embed=embed, view=view)

    
def setup(bot: Bot):
    bot.add_cog(test(bot))
