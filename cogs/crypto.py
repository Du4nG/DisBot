import redis
import requests 
import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord import Interaction, SlashOption
from decimal import Decimal
  
import json
import websockets

class Crypto(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.r = redis.Redis(
                    host='redis.cngthnh.io.vn',
                    port=6379,
                    username='queostn',
                    password='B0HNbCgY5j9u7s6Vz',
                )

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


    @nextcord.slash_command(description='Tạo thông báo giá coin.')
    async def alert(self, interaction: Interaction,
                    coin: str = SlashOption(description='Chọn coin.'),
                    symbol: str = SlashOption(description='>, <, >=, <=.'),
                    target_price: float = SlashOption(description='Chọn giá.')
                    ):
        async with websockets.connect('wss://stream.binance.com:9443/ws') as websocket:
            user = interaction.user
            channel = interaction.channel.id
            coin = coin.upper()

            await websocket.send(json.dumps({'method': 'SUBSCRIBE', 'params': [f'{coin.lower()}usdt@ticker'], 'id': 1}))
            await interaction.send(f'{user.name} vừa tạo một ALERT khi giá {coin.upper()} {symbol} ${target_price}')

            self.r.set(f'queo:{target_price}', f'{coin},{channel}')

            while True:
                message = await websocket.recv()
                data = json.loads(message)
                if 'c' in data:
                    price = float(data['c'])

                    if symbol == '>=' or symbol == '>':
                        if price >= target_price:
                            await interaction.send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                            break
                    elif symbol == '<=' or symbol == '<':
                        if price <= target_price:
                            await interaction.send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                            break

def setup(bot: Bot):
    bot.add_cog(Crypto(bot))

