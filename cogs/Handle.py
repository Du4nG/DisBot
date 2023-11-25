from nextcord.ext.commands import Bot, Cog, Context
from nextcord import Message, Embed
from nextcord.ext import commands

class Handle(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command đéo tồn tại.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Đéo có quyền.')

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return
        
        if 'lon' in message.content.lower():
            # ~~Gạch bỏ~~
            edited_content  = message.content.replace('lon', '~~lon~~')
            await message.delete()
            await message.channel.send(edited_content)

        if 'gay' in message.content.lower():
            emoji = '❓'
            await message.add_reaction(emoji)
            embed = Embed()
            embed.set_image(url='https://scontent.fsgn5-2.fna.fbcdn.net/v/t1.15752-9/348379595_631546668891602_9188306257152435004_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=62SKWZjbwUgAX_7FByu&_nc_oc=AQkeAuxKah1CfqyF0g587IVwUsuCbh-3iT5qn7XIsmwr_jzoF3k6FzMemx09r7Uv1dQ&_nc_ht=scontent.fsgn5-2.fna&oh=03_AdR34hKKMOLuX7em94nwcSpJ4cMbcjIVKqvywQ0-UIHEUA&oe=6589C191')
            await message.channel.send(embed=embed)

        if 'stonk' in message.content.lower():
            embed = Embed()
            embed.set_image(url='https://scontent.fsgn5-15.fna.fbcdn.net/v/t1.15752-9/370067957_1441938516366229_8779783017758847849_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=F2-vBIl5JPUAX-DHmua&_nc_ht=scontent.fsgn5-15.fna&oh=03_AdScnyu_uBdezf9rKzh-_zogyFxAFo0abwxTwey5i8QvMw&oe=6589AF64')
            await message.channel.send(embed=embed)

    @commands.command()
    async def send_dm(self, ctx: Context, user_id: int, *, message):
        user = await self.bot.fetch_user(user_id)
        if user:
            print(user.id)
            await user.send(message)
            await ctx.send(f'Đã gửi cho {user.name}#{user.discriminator}')
        else:
            await ctx.send(f'Đéo tìm ra thằng {user_id}.')

def setup(bot: Bot):
    bot.add_cog(Handle(bot))
