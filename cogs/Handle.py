import nextcord
from nextcord import Message, File, errors, Interaction, SlashOption, Member
from nextcord.ext import commands
from nextcord.ext.commands import Bot, Cog, Context
from random import randint
import os

gay_image_dir = r'image/gay'

class Handle(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.file_cnt = len(os.listdir(gay_image_dir))

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command cặc gì vậy.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Đéo có quyền.')

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return

        # bad_words = ['lon', 'lồn', 'cac', 'cặc', 'deo', 'đéo']
        # if any(bad_word in message.content.lower() for bad_word in bad_words):
        #     edited_content = message.content
        #     for bad_word in bad_words:
        #         edited_content = edited_content.replace(bad_word, f'~~{bad_word}~~')

        #     await message.delete()
        #     await message.channel.send(edited_content)

        if 'gay' in message.content.lower():
            try:
                await message.add_reaction('❓')
            except errors.NotFound:
                pass

            numb = randint(1, self.file_cnt)
            gay_image_path = f'image/gay/{numb}.jpg'

            await message.channel.send(file=File(gay_image_path))

        if 'stonk' in message.content.lower():
            image_path = 'image/stonk.jpg'
            await message.channel.send(file=File(image_path))

        if 'stink' in message.content.lower():
            image_path = 'image/stink.jpg'
            await message.channel.send(file=File(image_path))

    @nextcord.slash_command(description='Nhờ bot gửi tin nhắn riêng.')
    async def dm(self, interaction: Interaction,
                      member: Member = SlashOption(description='Lưu ý: Không thể gửi cho một bot.'),
                      message: str = SlashOption(description='Nhập nội dung message.')
                      ):
        user = await self.bot.fetch_user(member.id)
        await user.send(message)
        await interaction.response.send_message(f'Đã gửi cho **{user.name}**', ephemeral=True)

def setup(bot: Bot):
    bot.add_cog(Handle(bot))
