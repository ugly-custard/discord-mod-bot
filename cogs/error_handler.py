import discord
import sys
import traceback
from discord.ext import commands

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        ignored = (commands.CommandNotFound, )

        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send('Bad argument passed')

        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send("You can't use that command!")

        else:
            print(f'Ignoring Exception in Command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
