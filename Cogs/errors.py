import discord
from discord import app_commands
from discord.ext import commands

class Errors(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        command_logs = self.bot.get_channel(976519708096467025)
        
        if isinstance(error, commands.CommandNotFound):
            if not ctx.guild:
                await ctx.send(f"That command doesn't exist")
            else:
                channel = self.bot.get_channel(976345658644631623)
                embed = discord.Embed(description=f"That command doesn't exist.\n {ctx.message.content}", colour=0xFF0000)
                embed.set_author(name=(f"{ctx.author.nick}'s Error"), icon_url=ctx.author.display_avatar)
                if not ctx.channel.id == 976345658644631623:
                    await ctx.message.delete()
                    await channel.send(f"{ctx.author.mention} error message below", delete_after=5)
                await channel.send(embed=embed, delete_after=5); await command_logs.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            if not ctx.guild:
                await ctx.send(f"Your command is missing some required information")
            else:
                channel = self.bot.get_channel(976345658644631623)
                embed = discord.Embed(description=f"Your command is missing some required information.", colour=0xFF0000)
                embed.set_author(name=(f"{ctx.author.nick}'s Error"), icon_url=ctx.author.display_avatar)
                if not ctx.channel.id == 976345658644631623:
                    await ctx.message.delete()
                    await channel.send(f"{ctx.author.mention} error message below", delete_after=5)
                await channel.send(embed=embed, delete_after=5); await command_logs.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            if not ctx.guild:
                await ctx.send(f"You don't have permission to use this command")
            else:
                channel = self.bot.get_channel(976345658644631623)
                embed = discord.Embed(description=f"You don't have permission to use this command.", colour=0xFF0000)
                embed.set_author(name=(f"{ctx.author.nick}'s Error"), icon_url=ctx.author.display_avatar)
                if not ctx.channel.id == 976345658644631623:
                    await ctx.message.delete()
                    await channel.send(f"{ctx.author.mention} error message below", delete_after=5)
                await channel.send(embed=embed, delete_after=5); await command_logs.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            if not ctx.guild:
                await ctx.send(f"User not found")
            else:
                channel = self.bot.get_channel(976345658644631623)
                embed = discord.Embed(description=f"Member not found", colour=0xFF0000)
                embed.set_author(name=(f"{ctx.author.nick}'s Error"), icon_url=ctx.author.display_avatar)
                if not ctx.channel.id == 976345658644631623:
                    await ctx.message.delete()
                    await channel.send(f"{ctx.author.mention} error message below", delete_after=5)
                await channel.send(embed=embed, delete_after=5); await command_logs.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            if not ctx.guild:
                await ctx.send(f"That command doesn't work in DMS")
            else:
                channel = self.bot.get_channel(976345658644631623)
                embed = discord.Embed(description=f"That command doesn't work in <#{ctx.channel.id}>. Trying using the command in here, and if that doesn't work try it in the bot's direct messages!", colour=0xFF0000)
                embed.set_author(name=(f"{ctx.author.nick}'s Error"), icon_url=ctx.author.display_avatar)
                if not ctx.channel.id == 976345658644631623:
                    await ctx.message.delete()
                    await channel.send(f"{ctx.author.mention} error message below", delete_after=5)
                await channel.send(embed=embed, delete_after=5); await command_logs.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            if not ctx.guild:
                await ctx.send(f"Slow down, you can use that command again in {round(error.retry_after)} seconds")
            else:
                channel = self.bot.get_channel(976345658644631623)
                embed = discord.Embed(description=f"This command is on cooldown, try again after {round(error.retry_after)} seconds.", colour=0xFF0000)
                embed.set_author(name=(f"{ctx.author.nick}'s Error"), icon_url=ctx.author.display_avatar)
                if not ctx.channel.id == 976345658644631623:
                    await ctx.message.delete()
                    await channel.send(f"{ctx.author.mention} error message below", delete_after=5)
                await channel.send(embed=embed, delete_after=5); await command_logs.send(embed=embed)
        
async def setup(bot: commands.Bot):
    print("Error Cog Ready")
    await bot.add_cog(Errors(bot))

"""from discord import Interaction
from discord.app_commands import CommandTree, AppCommandError, Command
from discord.errors import NotFound, HTTPException, Forbidden

from log import log


class CmdTree(CommandTree):

    async def on_error(self, interaction: Interaction, command: Command, error: AppCommandError) -> None:
        # Per usual, getting the original error
        error = getattr(error, 'original', error)

        log.debug("Reached error_handler")

        if isinstance(error, (NotFound, HTTPException, Forbidden)):
            log.warn(f"'{interaction.command.name}' command raised {error.status} {error.__class__}")
            raise error
        else:
            raise error"""