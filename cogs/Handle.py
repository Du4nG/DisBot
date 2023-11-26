from nextcord.ext.commands import Bot, Cog, Context
from nextcord import Message, File
from nextcord.ext import commands
import os

gay_image_dir = r'image\gay'
file_count = len(os.listdir(gay_image_dir))

class Handle(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.flag = 1

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

        bad_words = ['lon', 'lồn', 'cac', 'cặc', 'deo', 'đéo']
        if any(bad_word in message.content.lower() for bad_word in bad_words):
            edited_content = message.content
            for bad_word in bad_words:
                edited_content = edited_content.replace(bad_word, f'~~{bad_word}~~')

            await message.delete()
            await message.channel.send(edited_content)

        if 'gay' in message.content.lower():
            emoji = '❓'
            gay_image_path = rf'image\gay\{self.flag}.jpg'
            self.flag += 1
            if self.flag > file_count:
                self.flag = 1
            await message.add_reaction(emoji)
            await message.channel.send(file=File(gay_image_path))

        if 'stonk' in message.content.lower():
            image_path = r'image\stonk.jpg'
            await message.channel.send(file=File(image_path))

        if 'stink' in message.content.lower():
            image_path = r'image\stink.jpg'
            await message.channel.send(file=File(image_path))
            # embed = Embed()
            # embed.set_image(url='https://scontent.fsgn5-15.fna.fbcdn.net/v/t1.15752-9/370067957_1441938516366229_8779783017758847849_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=8cd0a2&_nc_ohc=F2-vBIl5JPUAX-DHmua&_nc_ht=scontent.fsgn5-15.fna&oh=03_AdScnyu_uBdezf9rKzh-_zogyFxAFo0abwxTwey5i8QvMw&oe=6589AF64')
            # await message.channel.send(embed=embed)

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
