import discord
import random
from discord.ext import commands
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import CONSTANTS as consts
from CONSTANTS import GENERAL, BYE

class Welcome_leave_messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('welcome cog loaded')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(GENERAL)
        members = str(member.guild.member_count)
        if members[-1]=='1':
            suffix='st'
        elif members[-1]=='2':
            suffix='nd'
        elif members[-1]=='3':
            suffix='rd'
        else:
            suffix='th'
        text=f"""
Welcome {member.mention}! You are our {members}{suffix} member!. Remember to read the rules in <#{consts.RULES}> and follow them. Introduce yourself in <#{consts.INTRODUCTION}>, and get some self assignable roles in <#{consts.SELF_ASSIGN_ROLES}>!
"""
        images = ["yes.png", "yes2.png", "yes3.png", "yes4.png", "yes5.png", "yes6.png"]
        image = random.choice(images)
        img = Image.open(image)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("/app/MTCORSVA.TTF", 50)
        fontbig = ImageFont.truetype("/app/Fitamint Script.ttf", 60)

        draw.text((80, 25), 'Welcome To The Server!', fill='#000000', font=fontbig, stroke_width=2, stroke_fill='white')
        draw.text((150, 100), f"{member}", fill='#000000', font=font, stroke_width=2, stroke_fill='white')
        img.save('welcum.png')
        await channel.send(text, file=discord.File("welcum.png"))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(BYE)
        await channel.send(f"{member} | {member.id} just left the server")
def setup(bot):
    bot.add_cog(Welcome_leave_messages(bot))
