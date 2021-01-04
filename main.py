import discord
import time
import asyncio
import sys
import CONSTANTS as consts
from discord.ext import commands
from Implementation import YouTuber

token = consts.BOT_TOKEN
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('m:'), intents=intents)
#bot.remove_command('help')

client = discord.Client()
GOOGLE_API = consts.YOUTUBE_API_KEY
pingEveryXMinutes = consts.PING_TIME
processes = []
temp_list = []

temp_list.append(consts.YOUTUBE_CHANNEL_NAME)
temp_list.append(consts.YOUTUBE_CHANNEL_ID)
temp_list.append('')
processes.append(YouTuber(GOOGLE_API, temp_list[1]))

async def update():
    while True:
        try:
            waittime = pingEveryXMinutes * 60
            item = 0
            while item < 1:
                data = processes[item].update()
                print('Checking for new videos from {}'.format(temp_list[0]))
                if processes[item].isNewVideo():
                    print(f'{temp_list[0]} HAS UPLOADED A NEW VIDEO! PUSHING UPDATE ON DISCORD.')
                    announce = bot.get_channel(consts.ANNOUNCEMENT)
                    newvideo = f"Hey @everyone! **{temp_list[0]} HAS UPLOADED A NEW VIDEO! GO CHECK IT OUT!** \n{processes[item].getVideoLink(processes[item].videosData[0][1])}"
                    await announce.send(newvideo)
                item += 1
        except:
            pass
        while waittime > 0:
            mins, secs = divmod(waittime, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            waittime -= 1
            await asyncio.sleep(1)

@bot.event
async def on_ready():
    print(f'{bot.user} is online~')
    loadfunction()
    asyncio.ensure_future(update())

@bot.command()
async def load(ctx):
    if ctx.message.author.id == consts.ME:
        channel = await ctx.message.author.create_dm()
        loadfunction()
        await channel.send('Cogs loaded')

@bot.command()
async def unload(self, ctx):
    if ctx.message.author.id == consts.ME:
        channel = await ctx.message.author.create_dm()
        unloadfunction()
        await channel.send('Cogs unloaded')

@bot.command()
async def reload(self, ctx):
    if ctx.message.author.id == consts.ME:
        channel = await ctx.message.author.create_dm()
        try:
            unloadfunction()
            loadfunction()
        except Exception as e:
            await channel.send(e)
        finally:
            await channel.send('Cogs reloaded')

def loadfunction():
    cogs = ['Moderation', 'AutoReply', 'Welcome_leave_messages', 'logs', 'error_handler']
    for cog in cogs:
        bot.load_extension(f'cogs.{cog}')
        print(f'{cog} cog loaded')

def unloadfunction():
    cogs = ['Moderation', 'AutoReply', 'Welcome_leave_messages', 'logs', 'error_handler']
    for cog in cogs:
        bot.unload_extension(f'cogs.{cog}')
        print(f'{cog} cog unloaded')

bot.run(token)
