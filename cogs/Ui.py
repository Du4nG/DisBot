import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord import Interaction, ui, ButtonStyle, SelectOption
from secret import SERVER_ID


class Dropdown(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label='Vào', value='1'),
            SelectOption(label='Đéo', value='2'),
            SelectOption(label='Sục cặ', value='3')
        ]
        super().__init__(placeholder='Ẩm ?', options=options)

    async def callback(self, interaction: Interaction):
        match self.values[0]:
            case '1':
                await interaction.response.send_message('Vào thì nhanh mẹ m lên.', ephemeral=True)
            case '2':
                await interaction.response.send_message('Cút mẹ m.', ephemeral=True)
            case _:
                await interaction.response.send_message('Sục cặ vui vẻ.', ephemeral=True)


class DropdownView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())


class Subscription(ui.View):
    def __init__(self):
        super().__init__()#timeout=None)
        self.value = None

    @ui.button(label='Đi cắn', style=ButtonStyle.red)
    async def click_to_subscribe(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_message('Đi cắn xong đăng ký.', ephemeral=True)
        self.value = True
        self.stop()  


class Ui(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(description='Subcribe chen nồ.', guild_ids=[SERVER_ID])
    async def subcribe(self, interaction: Interaction):
        view = Subscription()
        await interaction.response.send_message(view=view)
        
    @nextcord.slash_command(description='Ẩm hay khô ?', guild_ids=[SERVER_ID])
    async def drop(self, interaction: Interaction):
        view = DropdownView()
        await interaction.response.send_message('Chọn nhanh!', view=view)


def setup(bot: Bot):
    bot.add_cog(Ui(bot))
