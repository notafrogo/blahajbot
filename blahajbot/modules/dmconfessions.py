import discord
from discord.ext import commands
import json
import random
from datetime import datetime, timezone
import os
import requests
import shutil

class DMconfessions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.path = "./data/DMconfess.json"
        if not os.path.exists(self.path):
            with open(self.path, 'w') as file:
                data = {
                        "0": {
                            "user": "635278883192832031",
                            "reported": 0,
                            "start": "0000000001",
                            "last": "0000000020"
                            }
                        }
                json.dump(data, file, indent=2)

        print("DMconfessions initialized")

    def now(self):
        return int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())

    @commands.slash_command(name="confessto", description="Confess in DMs to prevent accidentally leaking yourself")
    @commands.dm_only()
    async def confessto(self, ctx, confession : discord.Option(str, description="The confession you want to make"), attachment : discord.Option(discord.Attachment, description="The image you want to attach") = None):
        f = open("./data/registered.txt", 'r')
        f2 = f.read()
        f.close()
        confessChan = self.client.get_channel(int(f2))

        f = open("./data/dmconfess.txt", "a")
        f.write(f"{ctx.user.name} ({ctx.user.id}) - {confession}\n")
        f.close()

        with open(self.path, 'r') as file:
            data = json.load(file)
        
        if int(data[list(data.keys())[-1]]["last"])+600 < self.now():
            data[str(int(list(data.keys())[-1]))]["last"] = self.now()
            embed = discord.Embed(title=f"Anonymous Confession Session #{int(list(data.keys())[-1])+1}", description=f'"{confession}"', color=discord.Color.blurple())
            embed.set_footer(text="⚠️ If this confession is too over the top, you can report it using the /report command.")

            if attachment != None:
                res = requests.get(attachment, stream = True)
                if res.status_code == 200:
                    with open(f"./data/images/dm {confession}.jpg",'wb') as f:
                        shutil.copyfileobj(res.raw, f)

                embed.set_image(url=f"attachment:///data/images/dm {confession}.jpg")
            
            await ctx.respond(f":white_check_mark: Your confession has been added to {confessChan.mention}!", ephemeral=True)
            await confessChan.send(embed=embed)


        elif str(ctx.user.id) == data[list(data.keys())[-1]]["user"]:
                data[str(int(list(data.keys())[-1])+1)]["last"] = self.now()
                embed = discord.Embed(title=f"Anonymous Confession Session #{str(int(list(data.keys())[-1])+1)}", description=f'"{confession}"', color=discord.Color.blurple())
                embed.set_footer(text="⚠️ If this confession is too over the top, you can report it using the /report command.")

                if attachment != None:
                    res = requests.get(attachment, stream = True)
                    if res.status_code == 200:
                        with open(f"./data/images/dm {confession}.jpg",'wb') as f:
                            shutil.copyfileobj(res.raw, f)

                    embed.set_image(url=f"attachment:///data/images/dm {confession}.jpg")
                
                await ctx.respond(f":white_check_mark: Your confession has been added to {confessChan.mention}!", ephemeral=True)
                await confessChan.send(embed=embed)


        elif str(ctx.user.id) != data[list(data.keys())[-1]["user"]]:
                await ctx.respond("Someone else is already using confessions. Try again later.")
                return

    @commands.slash_command(name="confesschan", description="Assign a channel to DM confessions")
    @commands.has_permissions(administrator=True)
    async def confesschan(self, ctx):
        f = open("./data/registered.txt", "w")
        f.write(str(ctx.channel.id))
        await ctx.respond(f":white_check_mark: {ctx.channel.mention} is now the DM confessions channel.", ephemeral=True)

def setup(client):
    client.add_cog(DMconfessions(client))