import discord
import asyncio
import psycopg2
import pytz
import CONSTANTS as consts
from CONSTANTS import KAMI, EMPEROR, FIREWALL, WARDEN, BAN_LOGS
from discord.ext import commands, tasks
from datetime import datetime

class mutes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = psycopg2.connect(consts.DB_URL)
        self.cur = self.conn.cursor()
        self.cur.execute("create table if not exists mute(caseID serial primary key, userID bigint not null, modID bigint not null, time timestamp with time zone, reason varchar(250));")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.mute_check()

    async def user_check(self, ctx, user):
        user = str(user)
        if user[:1]=="<":
            user=int(''.join([i for i in user if i.isdigit()]))
            user = await ctx.guild.fetch_member(user)
            return user
        else:
            try:
                user = await ctx.guild.fetch_member(int(user))
                return user
            except:
                return None

    @commands.command()
    @commands.has_any_role(KAMI, EMPEROR, FIREWALL, WARDEN)
    async def mute(self, ctx, user=None, time=None, *, reason="No reason specified."):
        """
m:mute <user mention>/<userID> <time> [reason]
Mute a member for specified amount of time (or indefinitely) so they can't chat (cause trouble)"""
        log_channel = self.bot.get_channel(BAN_LOGS)
        if user == None:
            await ctx.send(f"Kisko mute karna wo to batao yaar {ctx.author.mention}")

        else:
            user = await self.user_check(ctx, user)
            roles = [role.id for role in user.roles]
            if KAMI in roles:
                await ctx.send("You can't mute a moderator!")
                return
            elif EMPEROR in roles:
                await ctx.send("You can't mute a moderator!")
                return
            elif FIREWALL in roles:
                await ctx.send("You can't mute a moderator!")
                return
            elif WARDEN in roles:
                await ctx.send("You can't mute a moderator!")
                return
            role = ctx.guild.get_role(consts.MUTED)
            if user is not None:
                try:
                    if time is not None:
                        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
                        def timeco(time):
                            try:
                                return int(time[:-1]) * time_convert[time[-1]]
                            except:
                                return time
                        jikan = timeco(time)
                        self.cur.execute(f"insert into mute(userID, modID, time, reason) values({user.id}, {ctx.author.id}, now() + interval '{jikan} seconds', '{reason}');")
                        await user.add_roles(role, reason=reason)
                        e2=discord.Embed(color=discord.Color.red())
                        e2.description=f"User {user.mention} was muted by moderator {ctx.author.mention}"
                        await ctx.send(embed=e2)
                    else:
                        self.cur.execute(f"insert into mute(userID, modID, time, reason) values({user.id}, {ctx.author.id}, null, '{reason}');")
                        await user.add_roles(role, reason=reason)
                        e2=discord.Embed(color=discord.Color.red())
                        e2.description=f"User {user.mention} was muted by moderator {ctx.author.mention}"
                        await ctx.send(embed=e2)
                    self.conn.commit()
                    e=discord.Embed(color=discord.Color.red())
                    e.set_author(name=f'User {user} was muted', icon_url=user.avatar_url)
                    e.add_field(name="User:", value=f"{user.mention}")
                    e.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                    e.add_field(name="Length:", value=f"{time}")
                    e.add_field(name="Reason:", value=f"{reason}", inline=False)
                    e.set_footer(text=f"User ID: {user.id}")
                    e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
                    await log_channel.send(embed=e)
                except Exception as e:
                    print(e)
                    await ctx.send(str(e))
                    success=False
            else:
                await ctx.send("No such user found")

    @commands.command()
    @commands.has_any_role(KAMI, EMPEROR, FIREWALL, WARDEN)
    async def unmute(self, ctx, user=None):
        """
m:unmute <user mention>/<userID>
Unmute a user so that they can chat again"""
        log_channel = self.bot.get_channel(BAN_LOGS)
        if user == None:
            await ctx.send(f"Kisko unmute karna wo to batao yaar {ctx.author.mention}")
        else:
            user = await self.user_check(ctx, user)
            role = ctx.guild.get_role(consts.MUTED)
            if user is not None:
                try:
                    await user.remove_roles(role)
                    self.cur.execute(f"delete from mute where userID={user.id};")
                    self.conn.commit()
                    e2=discord.Embed(color=discord.Color.green())
                    e2.description=f"User {user.mention} was unmuted by moderator {ctx.author.mention}"
                    await ctx.send(embed=e2)
                    e=discord.Embed(color=discord.Color.green())
                    e.set_author(name=f'User {user} was unmuted', icon_url=user.avatar_url)
                    e.add_field(name="User:", value=f"{user.mention}")
                    e.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                    e.set_footer(text=f"User ID: {user.id}")
                    e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
                    await log_channel.send(embed=e)
                except Exception as e:
                    print(e)
                    await ctx.send(str(e))
            else:
                await ctx.send("No such user found")

    @commands.command(name="mutes", aliases=['displaymute', 'displaymutes'])
    @commands.has_any_role(KAMI, EMPEROR, FIREWALL, WARDEN)
    async def display(self, ctx, user=None):
        """
m:mutes [user mention]/[userID]
Check the muted members and get info on the mute"""
        if user==None:
            self.cur.execute("select * from mute")
            bruh = self.cur.fetchall()
            muted_users=[]
            for b in bruh:
                user=f'<@{b[1]}>'
                muted_users.append(user)
            if len(muted_users) == 0:
                value='No users muted rn'
            else:
                value='\n'.join(muted_users)
            e=discord.Embed(color=discord.Color.blue())
            e.description="**Muted Users:** \n"+value
            e.set_footer(text="Mention/use the user's ID for more info on a mute")
            e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
            await ctx.send(embed=e)
        else:
            user = await self.user_check(ctx, user)
            if user is not None:
                try:
                    self.cur.execute("select * from mute")
                    bruh = self.cur.fetchall()
                    e=discord.Embed(color=discord.Color.blue())
                    for b in bruh:
                        if b[1] == user.id:
                            e.add_field(name="User:", value=f"{user.mention}")
                            e.add_field(name="Moderator:", value=f"<@{b[2]}>")
                            e.add_field(name="Unmute time:", value=f"{b[3]}")
                            e.add_field(name="Reason:", value=f"{b[4]}", inline=False)
                    e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
                    await ctx.send(embed=e)
                except Exception as e:
                    print(e)
                    await ctx.send(str(e))

    async def mute_check(self):
        log_channel = self.bot.get_channel(BAN_LOGS)
        while True:
            try:
                self.cur.execute("select * from mute")
                bruh = self.cur.fetchall()
                for b in bruh:
                    tz = b[3].tzinfo
                    if datetime.now(tz) > b[3]:
                        guild = self.bot.get_guild(consts.GUILD_ID)
                        user = await guild.fetch_member(b[1])
                        role = guild.get_role(consts.MUTED)
                        try:
                            await user.remove_roles(role)
                            self.cur.execute(f"delete from mute where userID={b[1]};")
                            e=discord.Embed(color=discord.Color.green())
                            e.set_author(name=f'User {user} was unmuted', icon_url=user.avatar_url)
                            e.add_field(name="User:", value=f"{user.mention}")
                            e.add_field(name="Moderator:", value=f"{self.bot.user.mention}")
                            e.add_field(name="Reason:", value="Auto")
                            e.set_footer(text=f"User ID: {user.id}")
                            e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
                            await log_channel.send(embed=e)
                        except Exception as e:
                            print(e)
                            await asyncio.sleep(30)
                await asyncio.sleep(30)
            except Exception as e:
                if str(e) == "'NoneType' object has no attribute 'tzinfo'":
                    pass
                else:
                    print(e)
                    await asyncio.sleep(30)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.cur.execute("select * from mute")
        bruh = self.cur.fetchall()
        for b in bruh:
            try:
                if b[1] == member.id:
                    role = guild.get_role(consts.MUTED)
                    await member.add_roles(role)
            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(mutes(bot))
