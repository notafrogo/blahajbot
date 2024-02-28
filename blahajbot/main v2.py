# import discord
# from discord.ext import commands
import os

# intents = discord.Intents.all()
# client = commands.Bot(intents=intents, command_prefix="b!")

# for cog in os.listdir("./modules"):
#     if cog.endswith(".py"):
#         client.load_extension(f"modules.{cog[:-3]}")

# token = open("./data/token.txt", "r").read()

# # tokenmain = open("./data/tokenmain.txt", "r").read()

# client.run(token)

fileList = [chan.replace(".txt", "") for chan in os.listdir("logs") if chan.endswith(".txt")]

print(fileList)