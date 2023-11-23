from nextcord.ext.commands import Bot, Cog, Context
from nextcord import Message, Embed
from nextcord.ext import commands

class Handle(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command đéo tồn tại.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Đéo có quyền.')

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.client.user:
            return
        
        if 'lon' in message.content.lower():
            # ~~Gạch bỏ~~
            edited_content  = message.content.replace('lon', '~~lon~~')
            await message.delete()
            await message.channel.send(edited_content)

        if 'gay' in message.content.lower():
            emoji = '🏳️‍🌈'
            await message.add_reaction(emoji)
            embed = Embed()
            embed.set_image(url='https://scontent.fsgn5-5.fna.fbcdn.net/v/t1.15752-9/401345615_703251725074261_1105250454797496483_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=r1N30PADqjMAX8Of0M2&_nc_ht=scontent.fsgn5-5.fna&oh=03_AdS0tJdqIzcxcFbteIhypn59r-2E-eiSWLfVAMxu646jzQ&oe=6586D14E')
            await message.channel.send(embed=embed)

    @commands.command()
    async def send_dm(self, ctx: Context, user_id: int, *, message):
        # Fetch the user based on their ID
        user = await self.client.fetch_user(user_id)
        if user:
            # Send a direct message to the user
            print(user.id)
            await user.send(message)
            await ctx.send(f'Đã gửi cho {user.name}#{user.discriminator}')
        else:
            await ctx.send(f'Đéo tìm ra thằng {user_id}.')

def setup(client: Bot):
    client.add_cog(Handle(client))
