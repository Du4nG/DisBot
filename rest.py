from discord import FFmpegPCMAudio, Member
from discord.ext.commands import has_permissions, MissingPermissions, Context

from secret import TOKEN, TEST_CHANNEL_ID

queues = {}
def check_queue(ctx: Context, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)


# @client.event
# async def on_message(message: discord.Message):
#     if message.content == 'lon':
#         # Gạch bỏ
#         edited_content  = f'~~{message.content}~~'
#         await message.delete()
#         await message.channel.send(edited_content)


@client.command()
async def pause(ctx: Context):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('Đéo có gì để pause.')

@client.command()
async def resume(ctx: Context):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('Đéo có gì để resume.')

@client.command()
async def stop(ctx: Context):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send('Im mẹ mồm.')

@client.command()
async def play(ctx: Context, arg):
    voice = ctx.guild.voice_client
    song = f'songs/{arg}.mp3'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))

@client.command()
async def queue(ctx: Context, arg):
    voice = ctx.guild.voice_client
    song = f'songs/{arg}.mp3'
    source = FFmpegPCMAudio(song)

    if ctx.guild.id in queues:
        queues[ctx.guild.id].append(source)
    else:
        queues[ctx.guild.id] = [source]

    await ctx.send(f'Đã thim vào hàng chờ!')

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx: Context, member: Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Cút mẹ m đi {member}.')

@kick.error
async def kick_error(ctx: Context, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('Đéo có quyền sao kick được.')

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx: Context, member: Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Cấm vĩnh viễn con bò {member}.')

@ban.error
async def ban_error(ctx: Context, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('Đéo có quyền sao ban được.')

# @client.command()
# async def embed(ctx: Context):
#     embed = discord.Embed(title='Embed', description='Embed description', color=0x00ff00)
#     embed.add_field(name=ctx.author.display_name, value='Field Value', icon_url=ctx.author.avatar_url)
#     embed.set_footer(text='Embed footer')
#     await ctx.send(embed=embed)

