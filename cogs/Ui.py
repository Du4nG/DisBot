import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord import Interaction, ui, ButtonStyle
from secret import SERVER_ID


class Subscription(ui.View):
    def __init__(self):
        super().__init__()#timeout=None)
        self.value = None

    @ui.button(label='Subcribe', style=ButtonStyle.red)
    async def click_to_subscribe(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_message('Đã subcribe.', ephemeral=True)
        self.value = True
        self.stop()  


class Ui(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @nextcord.slash_command(description='Subcribe chen nồ', guild_ids=[SERVER_ID])
    async def subcribe(self, interaction: Interaction):
        view = Subscription()
        await interaction.response.send_message(view=view)
        
def setup(client: Bot):
    client.add_cog(Ui(client))
