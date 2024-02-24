import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord import Member, Interaction, File
from secret import DISBOT_WELCOME_CHANNEL_ID, HOI_VAN_HOA_SV_WELCOME_CHANNEL_ID
from PIL import Image, ImageDraw, ImageFont

class Greet(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # @Cog.listener()
    # async def on_ready(self):
    #     channel = self.bot.get_channel(TEXT_CHANNEL_ID)
    #     await channel.send('Bố m đã online.')

    @Cog.listener()
    async def on_member_join(self, member: Member):
        channel = self.bot.get_channel(DISBOT_WELCOME_CHANNEL_ID)
        channel_2 = self.bot.get_channel(HOI_VAN_HOA_SV_WELCOME_CHANNEL_ID)

        img = Image.open(r'image\pointing.jpg')
        font1 = ImageFont.truetype(r'font\PatrickHand-Regular.ttf', 50)
        font2 = ImageFont.truetype(r'font\PatrickHand-Regular.ttf', 90)

        draw = ImageDraw.Draw(img)
        draw.text((50, 85), "Á đù", (0,0,0), font=font1)
        draw.text((355 - font2.getlength(member.display_name)/2, 50), member.display_name, (0,0,0), font=font2)
        draw.text((280, 160), 'nhập hội', (0,0,0), font=font1)

        new_image_path = r'image\pointing_new.jpg'
        img.save(new_image_path)
        
        await channel.send(f'Đm, @everyone ra đây mà xem con gà {member.display_name}.')
        await channel.send(file=File(new_image_path))

        await channel_2.send(f'Đm, @everyone ra đây mà xem con gà {member.display_name}.')
        await channel_2.send(file=File(new_image_path))

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        channel = self.bot.get_channel(DISBOT_WELCOME_CHANNEL_ID)
        await channel.send(f'Cút mẹ m đi {member.display_name}.')

        channel_2 = self.bot.get_channel(HOI_VAN_HOA_SV_WELCOME_CHANNEL_ID)
        await channel_2.send(f'Cút mẹ m đi {member.display_name}.')

    @nextcord.slash_command(description='Gửi lời chào.')
    async def hello(self, interaction: Interaction):
        await interaction.send('Lô con cặ')


def setup(bot: Bot):
    bot.add_cog(Greet(bot))
