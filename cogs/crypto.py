import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord import Member, Interaction, SlashOption

from decimal import Decimal
import requests 
  

class Crypto(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(description='Lấy tỷ giá coin.')
    async def price(self, interaction: Interaction,
                      base: str = SlashOption(description='Chọn đồng Base.'),
                      quote: str = SlashOption(description='Chọn đồng Quote.')
                      ):
        
        key = f'https://api.binance.com/api/v3/ticker/price?symbol={base.upper()+quote.upper()}'
  
        data = requests.get(key)   
        data = data.json() 
        price = Decimal(data['price']).normalize()
        
        await interaction.send(f'Giá {base.upper()} hiện tại là ${price}')


def setup(bot: Bot):
    bot.add_cog(Crypto(bot))
