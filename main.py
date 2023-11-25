import nextcord
from nextcord import Interaction
from nextcord.ext.commands import Bot
from secret import TOKEN, SERVER_ID
import asyncio

intents = nextcord.Intents.all()
intents.members = True
intents.messages = True

bot = Bot(command_prefix='!', intents=intents)
extensions = ['cogs.Greet',
              'cogs.Voice',
              'cogs.Handle',
              'cogs.Ui',
              'cogs.MusicCog',]

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.competing, name='máy ảo'))
    print('Lên sóng.')

# async def main():
#     for extension in extensions:
#         bot.load_extension(extension)
#     await bot.start(TOKEN, bot=True)

# asyncio.run(main())

for extension in extensions:
    bot.load_extension(extension)

bot.run(TOKEN)