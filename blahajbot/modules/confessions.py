import discord
from discord.ext import commands
import json
from datetime import datetime, timezone
import random
import os
import requests
import shutil

class Confessions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.path = "./data/confess.json"
        self.colors = ["ff0000", "00ff00", "0000ff", "ffff00", "ff00ff", "00ffff", "ffffff"]
        if not os.path.exists(self.path):
            with open(self.path, 'w') as file:
                data = {
                        "0": {
                            "users": {
                            "635278883192832031": {
                                "color": "00ff00",
                                "reported": 0
                            },
                            "974169668287881316": {
                                "color": "ff0000",
                                "reported": 1
                            }
                            },
                            "colors": ["00ff00", "ff0000"],
                            "start": "0000000001",
                            "last": "0000000020"
                            }
                        }
                json.dump(data, file, indent=2)

        print("confessions initialized")

    def now(self):
        return int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
    
    @commands.slash_command(name="confess", description="Send an anonymous confession.")
    async def confess_cmd(self, ctx, confession : discord.Option(str, description="The confession you want to make"), attachment : discord.Option(discord.Attachment, description="The image you want to attach") = None):
        f = open("./data/confessions.txt", "a")
        f.write(f"{ctx.user.name} ({ctx.user.id}) - {confession}\n")
        f.close()

        if not "confess" in ctx.channel.name:
            await ctx.respond("You can't send messages in this channel. Go to a channel meant for confessions instead.", ephemeral=True)
            return
            
        with open(self.path, 'r') as file:
            data = json.load(file)
        if data[list(data.keys())[-1]]["last"]+600 < self.now():
            color = self.colors[random.randint(0, len(self.colors) - 1)]
            data[str(int(list(data.keys())[-1])+1)] = {"users": {ctx.user.id: {"color": color, "reported": 0}}, "colors": [color], "start": self.now(), "last": self.now()}

            session = int(list(data.keys())[-1])

            embed = discord.Embed(title=f"Anonymous Confession Session #{session}", description=f'"{confession}"', color=int(color, 16))
            embed.set_footer(text="⚠️ If this confession is too over the top, you can report it using the /report command.")

            if attachment != None:
                res = requests.get(attachment, stream = True)
                if res.status_code == 200:
                    with open(f"./data/images/{confession}.jpg",'wb') as f:
                        shutil.copyfileobj(res.raw, f)

                embed.set_image(url=f"attachment:///data/images/{confession}.jpg")
            
            await ctx.respond(f":white_check_mark: Your confession has been added to {ctx.channel.mention}!", ephemeral=True)
            await ctx.send(embed=embed)

        else:
            key = list(data.keys())[-1]
            users = data[key]["users"]
            if str(ctx.user.id) not in list(users.keys()):
                colors = [item for item in self.colors if item not in data[key]["colors"]]
                color = colors[random.randint(0, len(colors)-1)]
                data[key]["colors"].append(color)
                data[key]["users"][ctx.user.id] = {"color": color, "reported": 0}
                data[key]["last"] = self.now()
                
                session = int(list(data.keys())[-1])

                embed = discord.Embed(title=f"Anonymous Confession Session #{session}", description=f'"{confession}"', color=int(color, 16))
                embed.set_footer(text="⚠️ If this confession is too over the top, you can report it using the /report command.")

                if attachment != None:
                    res = requests.get(attachment, stream = True)
                    if res.status_code == 200:
                        with open(f"./data/images/{confession}.jpg",'wb') as f:
                            shutil.copyfileobj(res.raw, f)

                    embed.set_image(url=f"attachment:///data/images/{confession}.jpg")

                await ctx.respond(f":white_check_mark: Your confession has been added to {ctx.channel.mention}!", ephemeral=True)
                await ctx.send(embed=embed)
            else:
                color = users[str(ctx.user.id)]["color"]
                data[key]["last"] = self.now()

                session = int(list(data.keys())[-1])

                embed = discord.Embed(title=f"Anonymous Confession Session #{session}", description=f'"{confession}"', color=int(color, 16))
                embed.set_footer(text="⚠️ If this confession is too over the top, you can report it using the /report command.")

                if attachment != None:
                    res = requests.get(attachment, stream = True)
                    if res.status_code == 200:
                        with open(f"./data/images/{confession}.jpg",'wb') as f:
                            shutil.copyfileobj(res.raw, f)

                    embed.set_image(url=f"attachment:///data/images/{confession}.jpg")

                await ctx.respond(f":white_check_mark: Your confession has been added to {ctx.channel.mention}!", ephemeral=True)
                await ctx.send(embed=embed)

        with open(self.path, 'w') as file:
            json.dump(data, file, indent=2)
def setup(client):
    client.add_cog(Confessions(client))