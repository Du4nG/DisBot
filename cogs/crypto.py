import requests 
import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord import Interaction, SlashOption
from decimal import Decimal
  

class Crypto(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(description='Lấy giá coin theo USDT.')
    async def price(self, interaction: Interaction,
                      coin: str = SlashOption(description='Nhập mã coin: ETH, SOL, XRP, FDUSD, ...')
                      ):
        coin = coin.upper()
        key = f'https://api.binance.com/api/v3/ticker/24hr?symbol={coin}USDT'
        data = requests.get(key)   
        data = data.json()
        try:
            price = data['lastPrice']
            price = Decimal(price).normalize()
            price =  '{:,}'.format(price)
        except KeyError:
            await interaction.send(f'Mã coin {coin} không tồn tại.')
            return
        await interaction.send(f'Giá [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) hiện tại là **${price}**')
        # await interaction.send(f'Giá {coin} hiện tại là || **${price}** ||') # Che giá

    @nextcord.slash_command(description='Lấy tỷ giá một cặp coin.')
    async def rate(self, interaction: Interaction,
                      base: str = SlashOption(description='Chọn coin base.'),
                      quote: str = SlashOption(description='Chọn coin quote.')
                      ):
        key = f'https://api.binance.com/api/v3/ticker/price?symbol={base.upper()+quote.upper()}'
        data = requests.get(key)   
        data = data.json() 
        try:
            price = data['price']
            price = Decimal(price).normalize()
            price =  '{:,}'.format(price)
        except KeyError:
            await interaction.send(f'Cặp coin {base.upper()}/{quote.upper()} không tồn tại.\n\
`❗Lưu ý: Không phải cặp coin nào cũng được hỗ trợ. *Ví dụ: Chỉ có ETH/BTC chứ không có BTC/ETH.*`')
            return
        await interaction.send(f'**1** {base.upper()} = **{price}** {quote.upper()}')

def setup(bot: Bot):
    bot.add_cog(Crypto(bot))
