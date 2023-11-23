import nextcord
from nextcord import Interaction
from nextcord.ext.commands import Bot
from secret import TOKEN, SERVER_ID
import asyncio

intents = nextcord.Intents.all()

client = Bot(command_prefix='!', intents=intents)
extensions = ['cogs.Greet',
              'cogs.Voice',
              'cogs.Handle',
              'cogs.Ui',]

@client.slash_command(description='Mô cmn tả', guild_ids=[SERVER_ID])
async def test(interaction: Interaction):
    await interaction.response.send_message('Test thành công.')

@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.competing, name='máy ảo'))
    print('Lên sóng.')

async def main():
    for extension in extensions:
        client.load_extension(extension)
    await client.start(TOKEN)

asyncio.run(main())
