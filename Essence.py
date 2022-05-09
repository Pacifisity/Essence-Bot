# Discord API --------------------------------------------------
import discord
import sqlite3
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from os import getenv

# from SensitiveData import Server

# Privileged intents --------------------------------------------------
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

# Bot Config --------------------------------------------------
bot = commands.Bot(command_prefix = "$", intents = intents)

@bot.command(name="sync") # Sync Command
@commands.is_owner()
async def sync(ctx: commands.Context):
    try:
        async with ctx.typing():
            await bot.tree.sync(guild=discord.Object(id=725164114506285066))
    except Exception as e:
        await ctx.send(f"An error occured\n`{e}`")
    else:
        await ctx.send("Done!")

# Cogs --------------------------------------------------
async def loadExtensions():
    await bot.load_extension('Cogs.commands') # Misc commands
    await bot.load_extension('Cogs.user') # $profile related commands
    await bot.load_extension('Cogs.help') # Help commands
    await bot.load_extension('Cogs.parties') # $party related commands
    await bot.load_extension('Cogs.incremental') # Incremental game commands
    await bot.load_extension('Cogs.staff') # Staff commands
    await bot.load_extension('Cogs.errors') # Error Handler
    await bot.load_extension('Cogs.items') # $item related commands
    await bot.load_extension('Cogs.test') # $test related commands

# Server --------------------------------------------------
# Server.Server() WIP Server caller

# Bot Events -------------------------------------------
@bot.event # Bot status
async def on_ready():
    await loadExtensions()
    with sqlite3.connect('DB Storage/essence.db') as db:
            cursor = db.cursor()
    cursor.execute(f"SELECT status FROM server WHERE party = ?", ('spirit',))
    result = cursor.fetchone()
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(result[0]))
    print("Playing with Essence")

# Token --------------------------------------------------

load_dotenv()
Token = getenv("TOKEN")
bot.run(Token)