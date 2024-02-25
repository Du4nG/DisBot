import redis
import requests 
import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import tasks
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
        self.fetch_prices.start()

    @staticmethod
    def fetch(coin: str) -> str:
        key = f'https://api.binance.com/api/v3/ticker/24hr?symbol={coin}USDT'
        data = requests.get(key)   
        data = data.json()
        price = data['lastPrice']
        return price       
    
    @nextcord.slash_command(description='Lấy giá coin theo USDT.')
    async def price(self, interaction: Interaction,
                      coin: str = SlashOption(description='Nhập mã coin: ETH, SOL, XRP, FDUSD...')
                      ):
        coin = coin.upper()
        try:
            price = self.fetch(coin)
            price = Decimal(price).normalize()
            price = '{:,}'.format(price)
            await interaction.send(f'Giá [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) theo USDT hiện tại là **${price}**') # || {price} ||  Che giá
        except KeyError:
            await interaction.send(f'Mã coin *{coin}* không tồn tại.')

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
                    target_price: float = SlashOption(description='Chọn giá.')
                    ):

        coin = coin.upper()
        cur_price = float(self.fetch(coin))
        if cur_price <= target_price:
            sign = '>='
        else: sign = '<='

        user = interaction.user
        channel_id = interaction.channel.id
        coin = coin.upper()

        self.r.set(f'queo:{channel_id}', f'{coin},{sign},{target_price}')

        await interaction.send(f'{user.name} vừa tạo một ALERT khi giá {coin.upper()} {sign} ${target_price}')

    @tasks.loop(seconds=1)
    async def fetch_prices(self):
        async with websockets.connect('wss://stream.binance.com:9443/ws') as websocket:
            await websocket.send(json.dumps({'method': 'SUBSCRIBE', 'params': [f'{coin.lower()}usdt@ticker'], 'id': 1}))

            while True:
                message = await websocket.recv()
                data = json.loads(message)
                print(data)

                if 'c' in data:
                    price = float(data['c'])

                    for channel_key in self.r.scan_iter(match='queo:*'):
                        channel_id = int(channel_key.split(':')[-1])
                        alerts = self.r.hgetall(channel_key)
                        
                        # Iterate through alerts for this channel
                        for alert_key, alert_info in alerts.items():
                            coin, symbol, target_price = alert_info.decode().split(',')
                            target_price = float(target_price)

                            if symbol == '>=' and price >= target_price:
                                await self.bot.get_channel(channel_id).send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                                # Optionally, remove the alert from Redis after triggering
                                # self.r.hdel(channel_key, alert_key)
                            elif symbol == '<=' and price <= target_price:
                                await self.bot.get_channel(channel_id).send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                                # Optionally, remove the alert from Redis after triggering
                                # self.r.hdel(channel_key, alert_key)

                    # if symbol == '>=' or symbol == '>':
                    #     if price >= target_price:
                    #         await interaction.send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                    #         break
                    # elif symbol == '<=' or symbol == '<':
                    #     if price <= target_price:
                    #         await interaction.send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                    #         break


def setup(bot: Bot):
    bot.add_cog(Crypto(bot))
