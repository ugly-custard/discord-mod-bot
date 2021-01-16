import discord
from discord.ext import commands
import asyncio
import psycopg2
import CONSTANTS as consts
from CONSTANTS import KAMI, EMPEROR, FIREWALL, WARDEN

class AutoReply(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        
        self.conn = psycopg2.connect(consts.DB_URL)
        self.cur = self.conn.cursor()
        self.cur.execute("create table if not exists AutoReply(trigger varchar(50), reply varchar(250));")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        self.cur.execute("select * from AutoReply")
        bruh = self.cur.fetchall()
        for b in bruh:
            if b[0].lower() in message.content.lower():
                await message.channel.send(b[1])

    @commands.command(name="ARadd", aliases=['aradd', 'ARADD', 'autoreplyadd', 'AutoReplyAdd'])
    @commands.has_any_role(KAMI, EMPEROR, FIREWALL, WARDEN)
    async def insert(self, ctx, *, msg_content):
        """
m:ARadd <trigger> | <reply>
Adds an Auto Reply trigger
seperate your trigger and replye with a '|'"""
        try:
            if '|' not in msg_content:
                await ctx.send('Wrong use of command')
                return
            else:
                values = await self.trig_reply(msg_content)
            self.cur.execute("select * from AutoReply")
            bruh = self.cur.fetchall()
            v=[]
            for b in bruh:
                if b[0] == values[0]:
                    v.append('yes')
                else: v.append('no')
            if 'yes' in v:
                await ctx.send("This trigger already exists, choose a different one.")
            else:
                self.cur.execute(f"insert into AutoReply values('{values[0]}', '{values[1]}');")
                self.conn.commit()
                await ctx.send("success")
        except Exception as e:
            await ctx.send(str(e))

    @commands.command(name="ARremove", aliases=['arremove', 'ARRemove', 'autoreplyremove', 'AutoReplyRemove'])
    @commands.has_any_role(KAMI, EMPEROR, FIREWALL, WARDEN)
    async def delete(self, ctx, *, trigger):
        """
m:ARremove <trigger>
Removes the Auto Reply trigger"""
        try:
            self.cur.execute("select * from AutoReply")
            bruh = self.cur.fetchall()
            v=[]
            for b in bruh:
                if b[0] == trigger:
                    self.cur.execute(f"delete from AutoReply where trigger='{trigger}';")
                    self.conn.commit()
                    await ctx.send("success")
                    v.append('yes')
                else: v.append('no')
            if 'yes' not in v:
                await ctx.send("No such trigger exists, check if trigger is correct")
        except Exception as e:
            print(e)
            await ctx.send(str(e))

    @commands.command(name="ARdisplay", aliases=['ardisplay', 'ardis', 'autoreplydisplay', 'AutoReplyDisplay'])
    @commands.has_any_role(KAMI, EMPEROR, FIREWALL, WARDEN)
    async def display_(self, ctx):
        """
m:ARdisplay
Displays all the Auto Replies"""
        self.cur.execute("select * from AutoReply")
        bruh = self.cur.fetchall()
        if len(bruh) == 0:
            await ctx.send("There are no Auto Reply triggers set currently.")
        else:
            e=discord.Embed(color=discord.Color.blue())
            e2=discord.Embed(color=discord.Color.blue())
            e.title="Auto Reply triggers and their values:"
            fields=0
            for b in bruh:
                if fields <= 25:
                    e.add_field(name=f"Trigger: {b[0]}", value=f"**Reply**: {b[1]}", inline=False)
                elif fields > 25:
                    e2.add_field(name=f"Trigger: {b[0]}", value=f"**Reply**: {b[1]}", inline=False)
                fields += 1
            if len(e.fields) > 25:
                await ctx.send(embed=e)
                await ctx.send(embed=e2)
            else:
                await ctx.send(embed=e)

    @commands.command(name="welcome", aliases=['Welcome'])
    async def whalecum(self, ctx):
        """
m:welcome
Sends an image, welcoming new people"""
        await ctx.send('https://cdn.discordapp.com/attachments/495430664276017163/551763491934044185/Welcome_-_Mokou.jpg')

    @commands.command(name="bully", aliases=['Bully', 'bulli', 'Bulli'])
    async def billi(self, ctx):
        """
m:bully
Sends an image, saying 'no bully'"""
        await ctx.send('https://i.imgur.com/IbzRlPJ.jpg')

    @commands.command(name="insult", aliases=['Insult'])
    async def insult(self, ctx):
        """
m:insult
Get insulted by your favorite Mirchi-chan cuz why not"""
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

    @commands.command(name="whyis", aliases=['Whyis', 'WhyIs', 'WHYIS'])
    async def whyis(self, ctx, user: discord.Member):
        """
m:whyis <user mention>
Why is you?"""
        await ctx.send("Cuz his dad didn't pull out on time :pensive:")

    async def trig_reply(self, arg):
        #arg = arg.replace("'", "\\'")
        finalArgs = []
        toAppend = ''
        index = 0
        for i in arg:
            if(i == '|'):
                finalArgs.append(toAppend.strip())
                toAppend = ''
            else:
                toAppend += i
            if(index == len(arg) - 1):
                finalArgs.append(toAppend.strip())
                toAppend = ''
            index += 1
        return finalArgs

def setup(bot):
    bot.add_cog(AutoReply(bot))
