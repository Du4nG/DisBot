import redis
import requests
import hashlib
import nextcord
from nextcord.ext.commands import Bot, Cog
from nextcord.ext import tasks
from nextcord import Interaction, SlashOption
from decimal import Decimal
  
import json
import websockets

PREFIX = 'queo:'
HASH_STRING_LEN = 2**3

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

    @staticmethod
    def generate_hash_string(s: str, len=HASH_STRING_LEN):
        md5_hash = hashlib.md5(s.encode()).hexdigest()
        short_hash = md5_hash[:len]
        return short_hash

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
        hash_string = self.generate_hash_string(coin+sign+str(target_price))

        self.r.set(f'queo:{hash_string}:{channel_id}', f'{coin},{sign},{target_price}')

        await interaction.send(f'{user.display_name} vừa tạo một ALERT khi giá {coin.upper()} {sign} ${target_price}')

    @tasks.loop(seconds=0.5)
    async def fetch_prices(self):
        async with websockets.connect('wss://stream.binance.com:9443/ws') as websocket:
            for key in self.r.keys(f'{PREFIX}*'):
                channel_id = key[len(PREFIX) + HASH_STRING_LEN:]
                alert: str = self.r.get(key).decode()
                coin, sign, target_price = alert.split(',')
                target_price = float(target_price)
                
                await websocket.send(json.dumps({'method': 'SUBSCRIBE', 'params': [f'{coin.lower()}usdt@ticker'], 'id': 1}))

                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    print(data)

                    # if 'c' in data:
                    #     price = float(data['c'])

                    #     if sign == '>=' and price >= target_price:
                    #         await self.bot.get_channel(channel_id).send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                    #         # self.r.hdel(channel_key, alert_key)
                    #     elif sign == '<=' and price <= target_price:
                    #         await self.bot.get_channel(channel_id).send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                    #         # self.r.hdel(channel_key, alert_key)

                    # if symbol == '>=' or symbol == '>':
                    #     if price >= target_price:
                    #         await interaction.send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                    #         break
                    # elif symbol == '<=' or symbol == '<':
                    #     if price <= target_price:
                    #         await interaction.send(f'📢 Cả làng ra đây mà xem, [{coin}](<https://www.binance.com/en/trade/{coin}_USDT>) đã chạm ngưỡng **${target_price}**')
                    #         break



    @fetch_prices.before_loop
    async def before_fetch_prices(self):
        """
        Chờ bot lên sóng.
        """
        await self.bot.wait_until_ready()


def setup(bot: Bot):
    bot.add_cog(Crypto(bot))
