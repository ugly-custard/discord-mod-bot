import discord
import pytz
from discord.ext import commands
from datetime import datetime
from CONSTANTS import MEMBER_LOGS, SERVER_LOGS, MUTED

class logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.red())
        e.set_author(name=f'{message.author}', icon_url=message.author.avatar_url)
        e.description=f"**Message sent by {message.author.mention} deleted in {message.channel.mention}.**"
        if len(message.content) > 1024:
            content = message.content[:1021] + "..."
            e.add_field(name="Message Content:", value=f"{content}")
        else:
            e.add_field(name="Message Content:", value=f"{message.content} \u200b")
        if len(message.attachments) > 0:
            e.add_field(name="Number of attachments in the mesage:", value=f"{len(message.attachments)}", inline=False)
        e.set_footer(text=f"User ID: {message.author.id} | Message ID: {message.id}")
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        guild = messages[0].channel.guild
        e=discord.Embed(color=discord.Color.red())
        e.set_author(name=f"{guild.name}", icon_url=guild.icon_url)
        e.description=f"**Bulk messages deleted in {messages[0].channel.mention}, {len(messages)} messages deleted.**"
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name=f"{before.author}", icon_url=f"{before.author.avatar_url}")
        e.set_footer(text=f"User ID: {after.author.id}")
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
        if before.content != after.content:
            e.description=f"**Message edited in {before.channel.mention}. [Jump to message](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}/)**"
            if len(before.content) > 1024:
                content = before.content[:1021] + "..."
                e.add_field(name="Before:", value=f"{content}")
            else:
                e.add_field(name="Before:", value=f"{before.content} \u200b")
            if len(after.content) > 1024:
                content = after.content[:1021] + "..."
                e.add_field(name="After:", value=f"{content}")
            else:
                e.add_field(name="After:", value=f"{after.content} \u200b")
            await log_channel.send(embed=e)
        else:
            if before.pinned == True and after.pinned == False:
                e.description=f"**Message unpinned in {after.channel.mention}. [Jump to message](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}/)**"
                await log_channel.send(embed=e)
            elif before.pinned == False and after.pinned == True:
                e.description=f"**Message was pinned in {after.channel.mention}. [Jump to message](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}/)**"
                await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.green())
        e.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon_url)
        e.description=f"**Channel created: {channel.mention} | #{channel.name}**"
        e.set_footer(text=f"Channel ID: {channel.id}")
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.red())
        e.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon_url)
        e.description=f"**Channel deleted: #{channel.name}**"
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name=f"{before.guild.name}", icon_url=before.guild.icon_url)
        e.description=f"**Channel {before.mention} updated.**"
        e.set_footer(text=f"Channel ID: {before.id}")
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
        if before.name != after.name:
            e.add_field(name="Channel's name changed:", value=f"**Before:** {before.name}\n**After:** {after.name}", inline=False)
            await log_channel.send(embed=e)
        if before.category != after.category:
            e.add_field(name="Channel's category changed:", value=f"**Before:** {before.category}\n**After:** {after.category}", inline=False)
            await log_channel.send(embed=e)
        if str(before.type) == 'text':
            if before.topic != after.topic or before.is_nsfw() != after.is_nsfw():
                if before.topic != after.topic:
                    e.add_field(name="Channel's topic changed:", value=f"**Before:** {before.topic}\n**After:** {after.topic}", inline=False)
                if before.is_nsfw() == True and after.is_nsfw() == False:
                    e.add_field(name="NSFW settings changed:", value=f"{after.mention} is not an NSFW channel now.", inline=False)
                if before.is_nsfw() == False and after.is_nsfw() == True:
                    e.add_field(name="NSFW settings changed:", value=f"{after.mention} is an NSFW channel now.", inline=False)
                await log_channel.send(embed=e)

        if str(before.type) == 'voice':
            if before.bitrate != after.bitrate:
                e.add_field(name="Channel's bitrate changed:", value=f"**Before:** {before.bitrate}\n**After:** {after.bitrate}", inline=False)
                await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.green())
        e.set_author(name="Member joined", icon_url=member.avatar_url)
        e.description=f"{member.mention} | {member.name}#{member.discriminator}"
        e.set_thumbnail(url=member.avatar_url)
        e.add_field(name="Account age:", value=member.created_at)
        e.set_footer(text=f"User ID: {member.id}")
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.red())
        e.set_author(name="Member left", icon_url=member.avatar_url)
        e.description=f"{member.mention} | {member.name}#{member.discriminator}"
        e.set_thumbnail(url=member.avatar_url)
        e.set_footer(text=f"User ID: {member.id}")
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name="Member Updated", icon_url=after.avatar_url)
        e.set_footer(text=f"User ID: {after.id}")
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
        x = MUTED
        r_before = [role.id for role in before.roles]
        r_after = [role.id for role in after.roles]
        if before.nick != after.nick:
            e.description=f"{after.mention} Nickname changed."
            e.add_field(name="Before:", value=f"{before.nick}", inline=False)
            e.add_field(name="After:", value=f"{after.nick}", inline=False)
            await log_channel.send(embed=e)
        if before.roles != after.roles:
            r = list(set(r_before) ^ set(r_after))
            if x not in r_before and x not in r_after:
                if len(before.roles) < len(after.roles):
                    e.description=f"**{after.mention} was given the <@&{r[0]}> role.**"
                elif len(before.roles) > len(after.roles):
                    e.description=f"**{after.mention} was removed from the <@&{r[0]}> role.**"
                await log_channel.send(embed=e)
            else:
                e2=discord.Embed(color=discord.Color.red())
                e2.set_author(name=f"{after.name}", icon_url=after.avatar_url)
                e2.set_footer(text=f"User ID: {after.id}")
                e2.timestamp = datetime.now()
                if x in r_before and x not in r_after:
                    e2.description=f"**{after.mention} | {after.name}#{after.discriminator} was just unmuted.**"
                    await log_channel.send(embed=e2)
                if x not in r_before and x in r_after:
                    e2.description=f"**{after.mention} | {after.name}#{after.discriminator} was just muted.**"
                    await log_channel.send(embed=e2)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name="Server Updated", icon_url=after.icon_url)
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
        if before.name != after.name or before.region != after.region or before.afk_timeout != after.afk_timeout or before.afk_channel != after.afk_channel or before.icon != after.icon or before.owner_id != after.owner_id or before.banner != after.banner:
            if before.name != after.name:
                e.add_field(name="Server's name changed:", value=f"**Before:** {before.name}\n**After:** {after.name}", inline=False)
            if before.region != after.region:
                e.add_field(name="Server's region changed:", value=f"**Before:** {before.region}\n**After:** {after.region}", inline=False)
            if before.afk_timeout != after.afk_timeout:
                e.add_field(name="Server's afk timeout changed:", value=f"**Before:** {before.afk_timeout}\n**After:** {after.afk_timeout}", inline=False)
            if before.afk_channel != after.afk_channel:
                e.add_field(name="Server's afk channel changed:", value=f"**Before:** {before.afk_channel}\n**After:** {after.afk_channel}", inline=False)
            if before.icon != after.icon:
                e.add_field(name="Server's icon changed:", value=f"**Before:** {before.icon_url_as(static_format='png')}\n**After:** {after.icon_url_as(static_format='png')}", inline=False)
            if before.owner_id != after.owner_id:
                e.add_field(name="Server's owner changed:", value=f"**Before:** <@{before.owner_id}>\n**After:** <@{after.owner_id}>", inline=False)
            if before.banner != after.banner:
                e.add_field(name="Server's banner changed:", value=f"**Before:** {before.banner_url_as(format='png')}\n**After:** {after.banner_url_as(format='png')}", inline=False)
            await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.green())
        e.set_author(name="Role Created", icon_url=role.guild.icon_url)
        e.description=f"{role.mention} | {role.name}"
        e.set_footer(text=f"Role ID: {role.id}")
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.red())
        e.set_author(name="Role Deleted", icon_url=role.guild.icon_url)
        e.description=f"@{role.name}"
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name="Role Updated", icon_url=after.guild.icon_url)
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
        if before.name != after.name or before.color != after.color:
            if before.name != after.name:
                e.add_field(name="Role's name changed:", value=f"**Before:** {before.name}\n**After:** {after.name}", inline=False)
            if before.color != after.color:
                e.add_field(name="Role's color changed:", value=f"**Before:** {before.color.value}\n**After:** {after.color.value}", inline=False)
            await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed()
        e.set_author(name=f"{member}", icon_url=member.avatar_url)
        e.timestamp = datetime.now(pytz.timezone('Asia/Kolkata'))
        if before.channel != after.channel:
            if before.channel == None and after.channel != None:
                e.description=f"{member.mention} **joined voice channel {after.channel.mention}**"
                e.color = discord.Color.green()
                e.set_footer(text=f"Channel ID: {after.channel.id}")
            elif before.channel != None and after.channel == None:
                e.description=f"{member.mention} **left voice channel {before.channel.mention}**"
                e.color = discord.Color.red()
                e.set_footer(text=f"Channel ID: {before.channel.id}")
            elif before.channel != None and after.channel != None and before.channel != after.channel:
                e.description=f"{member.mention} **moved to {after.channel.mention}**"
                e.color = discord.Color.blue()
                e.set_footer(text=f"Channel ID before: {before.channel.id} | Channel ID after: {after.channel.id}")
            await log_channel.send(embed=e)


def setup(bot):
    bot.add_cog(logs(bot))
