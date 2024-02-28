import discord
from discord.ext import commands
import json
from datetime import datetime, timezone
import os
import requests
import shutil


class Reportpm(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.path = "./data/confess.json"
        self.colors = ["ff0000", "00ff00", "0000ff", "ffff00", "ff00ff", "00ffff", "ffffff"]

        print("report/pm initialized")

    def now(self):
        return int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
        
    @commands.slash_command(name="pm", description="Send a private message to a confessor.")
    async def pm_cmd(self, ctx, 
                    session : discord.Option(int, description="The session to get a user from"), 
                    color : discord.Option(str, description="The color to send a message to", autocomplete=discord.utils.basic_autocomplete(("red", "green", "blue", "white", "black", "magenta", "yellow", "cyan"))), 
                    message : discord.Option(str, description="The message you want to send"), 
                    attachment : discord.Option(discord.Attachment, description="The attachment you want to upload") = None, 
                    anonymous : discord.Option(bool, description="Whether the message should be anonymous or not") = True):
        
        f = open("./data/responses.txt", "a")
        f.write(f"{ctx.user.name} ({ctx.user.id}) - {message}\n")
        f.close()

        with open(self.path, 'r') as file:
            data = json.load(file)

        found = False

        if session > len(data):
            await ctx.respond(f"No session with id '{session}' found.", ephemeral=True)
            return
        
        for user in list(data[str(session)]["users"]):

            if color == "red": 
                color = "ff0000"
            if color == "green":
                color = "00ff00"
            if color == "blue":
                color = "0000ff"
            if color == "white":
                color = "ffffff"
            if color == "black":
                color = "000000"
            if color == "magenta":
                color = "ff00ff"
            if color == "cyan":
                color = "00ffff"
            if color == "yellow":
                color = "ffff00"

            if data[str(session)]["users"][user]["color"] == color:
                member = self.client.get_user(int(user))
                found = True

        if not found:
            await ctx.respond(f"No user with color '{color}' found in session #{session}.", ephemeral=True)

        embed = discord.Embed(title=f"Response to Confession Session #{int(list(data.keys())[-1])}", description=f'"{message}"', color=int(color, 16))
        if not anonymous:
            embed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar.url)
        else:
            embed.set_author(name="Anonymous")

        if attachment != None:
            res = requests.get(attachment, stream = True)
            if res.status_code == 200:
                with open(f"./data/images/{message}.jpg",'wb') as f:
                    shutil.copyfileobj(res.raw, f)

            embed.set_image(url=f"attachment:///data/images/{message}.jpg")

        await ctx.respond(f":white_check_mark: Your message has been sent!", ephemeral=True)

        dm = await member.create_dm()
        await dm.send(embed=embed)

    @commands.slash_command(name="report", description="Report an anonymous confession.")
    async def confess_cmd(self, ctx, session : discord.Option(int, description="The session to"), color : discord.Option(str, autocomplete=discord.utils.basic_autocomplete(("red", "green", "blue", "white", "black", "magenta", "yellow", "cyan")))):

        if not os.path.exists(path=self.path):
            await ctx.respond("There are no confessions yet.", ephemeral=True)
            return
        
        colorold = color
        
        if color == "red": 
            color = "ff0000"
        if color == "green":
            color = "00ff00"
        if color == "blue":
            color = "0000ff"
        if color == "white":
            color = "ffffff"
        if color == "black":
            color = "000000"
        if color == "magenta":
            color = "ff00ff"
        if color == "cyan":
            color = "00ffff"
        if color == "yellow":
            color = "ffff00"
        
        with open(self.path, 'r') as file:
            data = json.load(file)

        found = False

        if session > len(data):
            await ctx.respond(f"No session with id '{session}' found.", ephemeral=True)
            return

        for user in list(data[str(session)]["users"]):
            if data[str(session)]["users"][user]["color"] == color:
                member = self.client.get_user(int(user))
                if ctx.user.guild_permissions.administrator and not ctx.user.id in data[str(session)]["users"][user]["reported"]:
                    data[str(session)]["users"][user]["reported"].append(ctx.user.id)
                    await ctx.respond(f"Success! You have reported {colorold} in session #{session}.", ephemeral=True)
                if ctx.user.guild_permissions.administrator and ctx.user.id in data[str(session)]["users"][user]["reported"]:
                    await ctx.respond(f"You have already reported this confession.", ephemeral=True)
                if not ctx.user.guild_permissions.administrator:
                    for channel in ctx.guild.channels:
                        if channel.name == "m-and-i-chat":
                            await channel.send(f"{colorold} from Confession Session #{session} has been reported by {ctx.user.mention}")
                    await ctx.respond(f"Success! You have reported {colorold} in session #{session}.", ephemeral=True)

                found = True
        
        if not found:
            await ctx.respond(f"No user with color '{colorold}' found in session #{session}.", ephemeral=True)

        if len(data[str(session)]["users"][user]["reported"]) >= 3:
            await ctx.send(f"The user was... {member.mention}")
        
        with open(self.path, 'w') as file:
            json.dump(data, file, indent=2)

    @commands.slash_command(name="report", description="Report an anonymous confession.")
    async def confess_cmd(self, ctx, session : discord.Option(int, description="The session to"), color : discord.Option(str, autocomplete=discord.utils.basic_autocomplete(("red", "green", "blue", "white", "black", "magenta", "yellow", "cyan")))):
        if not os.path.exists(path=self.path):
            await ctx.respond("There are no confessions yet.", ephemeral=True)
            return
        
        if color == "red": 
            colorhex = "ff0000"
        if color == "green":
            colorhex = "00ff00"
        if color == "blue":
            colorhex = "0000ff"
        if color == "white":
            colorhex = "ffffff"
        if color == "black":
            colorhex = "000000"
        if color == "magenta":
            colorhex = "ff00ff"
        if color == "cyan":
            colorhex = "00ffff"
        if color == "yellow":
            colorhex = "ffff00"
        
        with open(self.path, 'r') as file:
            data = json.load(file)

        found = False

        if session > len(data):
            await ctx.respond(f"No session with id '{session}' found.", ephemeral=True)
            return

        for user in list(data[str(session)]["users"]):
            if data[str(session)]["users"][user]["color"] == colorhex:
                member = self.client.get_user(int(user))
                if ctx.user.guild_permissions.administrator and not ctx.user.id in data[str(session)]["users"][user]["reported"]:
                    data[str(session)]["users"][user]["reported"].append(ctx.user.id)
                    await ctx.respond(f"Success! You have reported {color} in session #{session}.", ephemeral=True)
                if ctx.user.guild_permissions.administrator and ctx.user.id in data[str(session)]["users"][user]["reported"]:
                    await ctx.respond(f"You have already reported this confession.", ephemeral=True)
                if not ctx.user.guild_permissions.administrator:
                    for channel in ctx.guild.channels:
                        if channel.name == "m-and-i-chat":
                            await channel.send(f"{color} from Confession Session #{session} has been reported by {ctx.user.mention}")
                    await ctx.respond(f"Success! You have reported {color} in session #{session}.", ephemeral=True)

                found = True
        
        if not found:
            await ctx.respond(f"No user with color '{color}' found in session #{session}.", ephemeral=True)

        if len(data[str(session)]["users"][user]["reported"]) >= 3:
            await ctx.send(f"The user was... {member.mention}")
        
        with open(self.path, 'w') as file:
            json.dump(data, file, indent=2)

def setup(client):
    client.add_cog(Reportpm(client))