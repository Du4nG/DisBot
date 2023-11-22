import discord
from discord.ext.commands import Bot
from secret import TOKEN, TEST_CHANNEL_ID
import asyncio

intents = discord.Intents.all()
intents.members = True
intents.messages = True

client = Bot(command_prefix='!', intents=intents)
extensions = ['cogs.Greet']

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name='máy ảo'))
    print('Bot is ready.')

async def main():
    async with client:
        for extension in extensions:
            await client.load_extension(extension)
        await client.start(TOKEN)

asyncio.run(main())