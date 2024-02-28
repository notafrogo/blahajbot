import discord
from discord.ext import commands
from datetime import datetime

class Audit(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("audit initialized")
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.auditChan = self.client.get_channel(1072362080281301032)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if channel == self.auditChan:
            return
        
        embed = discord.Embed(description=f"**Channel Deleted: #{channel}**", timestamp=datetime.utcnow(), color=discord.Color.red())
        embed.set_footer(text=f"ID: {channel.id}")
        embed.set_author(icon_url=channel.guild.icon, name=channel.guild.name)
        await self.auditChan.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel == self.auditChan:
            return
        
        embed = discord.Embed(description=f"**Channel Created: #{channel}**", timestamp=datetime.utcnow(), color=discord.Color.green())
        embed.set_footer(text=f"ID: {channel.id}")
        embed.set_author(icon_url=channel.guild.icon, name=channel.guild.name)
        await self.auditChan.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(description=f"{member.mention} {member.name}", timestamp=datetime.utcnow(), color=discord.Color.green())
        embed.set_footer(text=f"ID: {member.id}")
        embed.set_author(icon_url=member.icon_url, name="Member Joined")
        await self.auditChan.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(description=f"{member.mention} {member.name}", timestamp=datetime.utcnow(), color=discord.Color.red())
        embed.set_footer(text=f"ID: {member.id}")
        embed.set_author(icon_url=member.icon_url, name="Member Left")
        await self.auditChan.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        embed = discord.Embed(description=f"{member.mention} {member.name}", timestamp=datetime.utcnow(), color=discord.Color.red())
        embed.set_footer(text=f"ID: {member.id}")
        embed.set_author(icon_url=member.icon_url, name="Member Banned")
        await self.auditChan.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        embed = discord.Embed(description=f"{member.mention} {member.name}", timestamp=datetime.utcnow(), color=discord.Color.red())
        embed.set_footer(text=f"ID: {member.id}")
        embed.set_author(icon_url=member.icon_url, name="Member Unbanned")
        await self.auditChan.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content != after.content:
            embed = discord.Embed(description=f"**Message Edited in** {after.channel.mention} [Jump to Message]({after.jump_url})", timestamp=datetime.utcnow(), color=discord.Color.blurple())
            embed.set_footer(text=f"User ID: {after.author.id}")
            embed.set_author(icon_url=after.author.avatar.url, name=after.author.name)
            embed.add_field(name="**Before**", value=before.content)
            embed.add_field(name="**After**", value=after.content, inline=False)
            if before.attachments:
                embed.set_image(url=before.attachments[0])
            await self.auditChan.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(description=f"**Message sent by {message.author.mention} Deleted in {message.channel.mention}** \n {message.content}", timestamp=datetime.utcnow(), color=discord.Color.red())
        embed.set_footer(text=f"User ID: {message.author.id} | Message ID: {message.id}")
        embed.set_author(icon_url=message.author.avatar.url, name=message.author.name)
        if message.attachments:
            embed.set_image(url=message.attachments[0])
        await self.auditChan.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        embed=discord.Embed(description=f"**Bulk Delete in {messages[0].channel.mention}, {len(messages)} messages deleted**", timestamp=datetime.utcnow(), color=discord.Color.blurple())
        embed.set_author(icon_url=messages[0].guild.icon, name=messages[0].guild.name)
        await self.auditChan.send(embed=embed)
    
    


def setup(client):
    client.add_cog(Audit(client))