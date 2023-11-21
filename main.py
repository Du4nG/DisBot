import discord
from discord.ext.commands import Bot
from secret import TOKEN, TEST_CHANNEL_ID

intents = discord.Intents.all()
intents.members = True
intents.messages = True

client = Bot(command_prefix='!', intents=intents)
extensions = ['cogs.Greet']

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='máy ảo'))
    print('Bot is ready.')

if __name__ == '__main__':
    for extension in extensions:
        client.load_extension(extension)

client.run(TOKEN, bot=True, reconnect=True)
