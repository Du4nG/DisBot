from discord.ext.commands import Bot, Cog, Context
from discord.ext import commands

class Handle(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command đéo tồn tại.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Đéo có quyền.')

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

async def setup(client: Bot):
    await client.add_cog(Handle(client))
