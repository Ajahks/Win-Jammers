import discord
from discord.ext import commands
import music
import keep_alive

cogs = [music]

client = commands.Bot(command_prefix='+', intents = discord.Intents.all())

for i in range(len(cogs)):
  cogs[i].setup(client)

keep_alive.keep_alive()

with open('token.txt') as f:
    token = f.readline()

client.run(token)