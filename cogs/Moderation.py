import discord
from discord.ext import commands
from CONSTANTS import BAN_LOGS, OWNER, MODERATOR, MOD_JR, HELPER

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('mod cog loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

    async def user_check(self, user):
        if user[:1] == '<':
            user = ''.join([i for i in user if i.isdigit()])
            user = await self.bot.fetch_user(int(user))
            return user
        else:
            try:
                user = await self.bot.fetch_user(int(user))
                return user
            except:
                return None
        
    async def mod_embed(self, ctx, user, success, method, reason):
        if success:
            e=discord.Embed(color=discord.Color.red())
            e.set_thumbnail(url=user.avatar_url)
            if method == 'ban':
                e.set_author(name=f'User {user} was {method}ned', icon_url=ctx.guild.icon_url)
            elif method == 'softban':
                e.set_author(name=f'User {user} was {method}ned', icon_url=ctx.guild.icon_url)
            elif method == 'unban':
                e.set_author(name=f'User {user} was {method}ned', icon_url=ctx.guild.icon_url)
            elif method == 'kick':
                e.set_author(name=f'User {user} was {method}ed', icon_url=ctx.guild.icon_url)
            else:
                e.set_author(name=f'User {user} was {method}d', icon_url=ctx.guild.icon_url)
            e.add_field(name="Reason:", value=f"{reason}")
            e.add_field(name="Moderator:", value=f"{ctx.author}")
            e.set_footer(text=f'User ID: {user.id}')
        else:
            e = await ctx.send("Some kinda error occured")
        return e

    @commands.command()
    @commands.has_any_role(OWNER, MODERATOR, MOD_JR)
    async def ban(self, ctx, user = None, *, reason="No specified reason."):
        log_channel = self.bot.get_channel(BAN_LOGS)
        if user == None:
            await ctx.send(f"Kisko ban karna wo to batao yaar {ctx.author.mention}")

        else:
            user = await self.user_check(user)
            if user is not None:
                try:
                    await user.send(f"You've been banned from the server **{ctx.guild}** \nReason: ***{reason}***")
                    await ctx.guild.ban(user, reason=reason)
                except Exception as e:
                    print(e)
                    success=False
                else:
                    success=True
                e=await self.mod_embed(ctx, user, success, 'ban', reason)
                await log_channel.send(embed=e)
                await ctx.send(f"User {user} was banned by moderator {ctx.author}")
            else:
                await ctx.send('User not found')

    @commands.command()
    @commands.has_any_role(OWNER, MODERATOR, MOD_JR)
    async def softban(self, ctx, user = None, *, reason="No reason specified."):
        log_channel = self.bot.get_channel(BAN_LOGS)
        if user == None:
            await ctx.send(f"Kisko *soft*ban karna wo to batao yaar {ctx.author.mention}")
        else:
            user = await self.user_check(user)
            if user is not None:
                try:
                    await user.send(f"You've been *soft*banned from the server **{ctx.guild}** \nReason: ***{reason}***")
                    await ctx.guild.ban(user, reason=reason)
                    await ctx.guild.unban(user, reason=reason)
                except Exception as e:
                    print(e)
                    success=False
                else:
                    success=True
                e=await self.mod_embed(ctx, user, success, 'softban', reason)
                await log_channel.send(embed=e)
                await ctx.send(f"User {user} was *soft*banned by moderator {ctx.author}")
            else:
                await ctx.send('User not found')

    @commands.command()
    @commands.has_any_role(OWNER, MODERATOR, MOD_JR)
    async def unban(self, ctx, user: int=None, *, reason="No reason specified."):
        log_channel = self.bot.get_channel(BAN_LOGS)
        if user == None:
            await ctx.send(f"Kisko unban karna wo to batao yaar {ctx.author.mention}")

        else:
            user = await self.bot.fetch_user(user)
            try:
                await ctx.guild.unban(user, reason=reason)
            except Exception as e:
                if e == '404 Not Found (error code: 10026): Unknown Ban':
                    await ctx.send("The user you want to unban isn't banned")
                success=False
            else:
                success=True
            e=await self.mod_embed(ctx, user, success, 'unban', reason)
            await log_channel.send(embed=e)
            await ctx.send(f"User {user} was unbanned by moderator {ctx.author}")

    @commands.command()
    @commands.has_any_role(OWNER, MODERATOR, MOD_JR)
    async def kick(self, ctx, user=None, *, reason="No reason specified."):
        log_channel = self.bot.get_channel(BAN_LOGS)
        if user == None:
            await ctx.send(f"Kisko kick karna wo to batao yaar {ctx.author.mention}")

        else:
            user = await self.user_check(user)
            if user is not None:
                try:
                    await user.send(f"You've been kicked from the server **{ctx.guild}** \nReason: ***{reason}***")
                    await ctx.guild.kick(user, reason=reason)
                except Exception as e:
                    print(e)
                    success=False
                else:
                    success=True
                
                e = await self.mod_embed(ctx, user, success, 'kick', reason)
                await log_channel.send(embed=e)
                await ctx.send(f"User {user} was kicked by moderator {ctx.author}")
            else:
                await ctx.send('User not found.')

    @commands.command(name='whois')
    async def whois(self, ctx, user=None):
        if not user:
            user = ctx.message.author
        else:
            if user[:1] == '<':
                user = ''.join([i for i in user if i.isdigit()])
                user = ctx.message.guild.get_member(int(user))
            else:
                try:
                    user = ctx.message.guild.get_member(int(user))
                except:
                    await ctx.send("No member found.")
        timestamp: datetime.timestamp = user.created_at
        joined_at: datetime.timestamp = user.joined_at

        timestamp_str = timestamp.strftime('%A, %B %d %Y @ %H:%M:%S')
        joined_at_str = joined_at.strftime('%A, %B %d %Y @ %H:%M:%S')

        embed=discord.Embed(color=discord.Color.blue())
        embed.set_author(name=f"{user}", icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='**User ID**',
                        value=f'{user.id}', inline=True)
        if not user.nick:
            nick='None'
        else:
            nick=user.nick
        embed.add_field(name='**Nickname**',
                        value=f'{nick}', inline=True)
        embed.add_field(name='**Joined on**',
                        value=f'{joined_at_str}', inline=False)
        embed.add_field(name='**Account created on**',
                        value=f'{timestamp_str}', inline=False)
        user_roles=[]
        for r in user.roles:
            if r.name != "@everyone":
                user_roles.append(r.mention)
        if len(user_roles)==0: user_roles.append('None')
        embed.add_field(name=f'**Roles[{len(user.roles[::-2])}]**',
                        value=", ".join(user_roles), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='avatar', aliases=['Avatar', 'av', 'Av', 'AV'])
    async def av(self, ctx, user=None):
        if not user:
            user = ctx.message.author
        else:
            if user[:1] == '<':
                user = ''.join([i for i in user if i.isdigit()])
                user = ctx.message.guild.get_member(int(user))
            else:
                try:
                    user = ctx.message.guild.get_meember(int(user))
                except:
                    await ctx.send("No member found.")
        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name=f"{user.name}'s Avatar", icon_url=user.avatar_url)
        e.description=f"**[Avatar Link]({user.avatar_url_as(static_format='png')})**"
        e.set_image(url=user.avatar_url)
        await ctx.send(embed=e)

    @commands.command(name='purge', aliases=['Purge', 'prune', 'Prune', 'clear'])
    @commands.has_any_role(OWNER, MODERATOR, MOD_JR, HELPER)
    async def purge(self, ctx, amount: int=20, user: discord.Member=None):
        #mgs = []
        #async for x in Client.logs_from(ctx.message.channel, limit = amount):
        #    mgs.append(x)
        if amount > 200:
            await ctx.send("You can't delete more than 200 messages at a time.")

        else:
            if user:
                check = lambda msg: msg.author == user and not msg.pinned
            else:
                check = lambda msg: not msg.pinned

            await ctx.channel.purge(limit=amount, check=check)
            await ctx.send(f"{amount} messages deleted.", delete_after=5)

    @commands.command(name='roleinfo', aliases=['inforole'])
    async def role_info(self, ctx, *, role):
        if role[:1] == '<':
            role = ''.join([i for i in role if i.isdigit()])
            role = ctx.message.guild.get_role(int(role))
        else:
            try:
                role = ctx.message.guild.get_role(int(role))
            except:
                return None
        created_at: datetime.timestamp = role.created_at
        created_at_str = created_at.strftime('%A, %B %d %Y @ %H:%M:%S')

        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name=f"{role.guild.name}", icon_url=role.guild.icon_url)
        e.add_field(name='**Role ID**',
                        value=f'{role.id}', inline=True)
        e.add_field(name='**Name**',
                        value=f'{role.name}', inline=True)
        e.add_field(name='**Created on**',
                        value=f'{created_at_str}', inline=True)
        e.add_field(name='**Position**',
                        value=f'{role.position}', inline=True)
        e.add_field(name='**Color**',
                        value=f'{role.color}', inline=True)
        e.add_field(name='**Displayed seperately?**',
                        value=f'{role.hoist}', inline=True)
        e.add_field(name='**Managed by a bot or any other integration?**',
                        value=f'{role.managed}', inline=True)
        e.add_field(name='**Mentionable?**',
                        value=f'{role.mentionable}', inline=True)
        e.add_field(name='**No. of members with this role**',
                        value=f'{len(role.members)}', inline=True)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Moderation(bot))
