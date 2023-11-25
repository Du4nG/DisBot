import nextcord
from nextcord.ext.commands import Bot
from secret import TOKEN

intents = nextcord.Intents.all()
intents.members = True
intents.messages = True

bot = Bot(command_prefix='!', intents=intents)
extensions = ['cogs.Greet',
              'cogs.Voice',
              'cogs.Handle',
              'cogs.Ui',
              'cogs.Music',]

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.competing, name='VSCode'))
    print('Lên sóng.')

for extension in extensions:
    bot.load_extension(extension)

bot.run(TOKEN)