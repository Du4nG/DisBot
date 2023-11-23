import nextcord
from nextcord.ext.commands import Bot
from secret import TOKEN, TEST_CHANNEL_ID
import asyncio

intents = nextcord.Intents.all()

client = Bot(command_prefix='!', intents=intents)
extensions = ['cogs.Greet',
              'cogs.Voice',
              'cogs.Handle',]

@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.competing, name='máy ảo'))
    print('Bot is ready.')


async def main():
    for extension in extensions:
        client.load_extension(extension)
    await client.start(TOKEN)

asyncio.run(main())