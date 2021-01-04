import discord
import requests
from discord.ext import commands

class AutoReply(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(name="welcome", aliases=['Welcome'])
    async def whalecum(self, ctx):
        """Sends an image, welcoming the user"""
        await ctx.send('https://cdn.discordapp.com/attachments/495430664276017163/551763491934044185/Welcome_-_Mokou.jpg')

    @commands.command(name="bully", aliases=['Bully', 'bulli', 'Bulli'])
    async def billi(self, ctx):
        """Sends an image, saying 'No bully'"""
        await ctx.send('https://i.imgur.com/IbzRlPJ.jpg')

    @commands.command(name="insult", aliases=['Insult'])
    async def insult(self, ctx):
        """Get insulted by your favorite Mirchi-chan, cuz why not"""
        res = requests.get(url='https://evilinsult.com/generate_insult.php?lang=en&type=json')
        if res.status_code == 200:
            insult = res.json()['insult']
            if 'nigga' in insult.lower():
                insult = "You're so retarded, even I, a bot, am tired of replying to you."
            if '&quot;' in insult:
                insult = insult.replace('&quot;', '"')
            if '&gt;' in insult:
                insult = insult.replace('%gt;', '>')
        else:
            insult = "You're so retarded, even I, a bot, am tired of replying to you."
        await ctx.send(insult)

def setup(bot):
    bot.add_cog(AutoReply(bot))
