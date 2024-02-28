import discord
from discord.ext import commands
import requests
import random

class Tord(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("tord initialized")
    
    tod_channels = [1161025884044669128]

    class RandomQ(discord.ui.View):
        @discord.ui.button(label=f"Random Question", style=discord.ButtonStyle.blurple)
        async def q(self, button, ctx):
            await ctx.message.edit(view=None)
            rand = ["DARE", "NHIE", "TRUTH", "WYR", "PARANOIA"]
            url = f"https://api.truthordarebot.xyz/v1/{rand[random.randint(0,4)]}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
            if data["type"] == "DARE":
                color = discord.Color.red()
            if data["type"] == "NHIE":
                color = discord.Color.blue()
            if data["type"] == "TRUTH":
                color = discord.Color.blurple()
            if data["type"] == "WYR":
                color = discord.Color.default()
            if data["type"] == "PARANOIA":
                color = discord.Color.greyple()
            embed = discord.Embed(title=data["question"], color = color)
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomQ(timeout=3600)

            await ctx.response.send_message(embed=embed, view=view)

    @commands.slash_command(name="random", description="Get a random question.")
    async def random_cmd(self, ctx):
        if ctx.channel.id in self.tod_channels:
            rand = ["DARE", "NHIE", "TRUTH", "WYR", "PARANOIA"]
            url = f"https://api.truthordarebot.xyz/v1/{rand[random.randint(0,4)]}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
            if data["type"] == "DARE":
                color = discord.Color.red()
            if data["type"] == "NHIE":
                color = discord.Color.blue()
            if data["type"] == "TRUTH":
                color = discord.Color.blurple()
            if data["type"] == "WYR":
                color = discord.Color.default()
            if data["type"] == "PARANOIA":
                color = discord.Color.greyple()
            embed = discord.Embed(title=data["question"], color = color)
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomQ(timeout=3600)

            msg = await ctx.respond(embed=embed, view=view)
            view.msg = msg
        else:
            await ctx.respond("You can't use this channel for TOD.", ephemeral=True)

    class RandomD(discord.ui.View):
        @discord.ui.button(label=f"Random Dare", style=discord.ButtonStyle.blurple)
        async def d(self, button, ctx):
            await ctx.message.edit(view=None)
            url = f"https://api.truthordarebot.xyz/v1/DARE"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.red())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomD(timeout=3600)

            await ctx.response.send_message(embed=embed, view=view)
    
    @commands.slash_command(name="dare", description="Get a random dare.")
    async def dare_cmd(self, ctx):
        if ctx.channel.id in self.tod_channels:
            url = f"https://api.truthordarebot.xyz/v1/DARE"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.red())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomD(timeout=3600)

            msg = await ctx.respond(embed=embed, view=view)
            view.msg = msg
        else:
            await ctx.respond("You can't use this channel for TOD.", ephemeral=True)

    class RandomN(discord.ui.View):
        @discord.ui.button(label=f"Random NHIE", style=discord.ButtonStyle.blurple)
        async def n(self, button, ctx):
            await ctx.message.edit(view=None)
            url = f"https://api.truthordarebot.xyz/v1/NHIE"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.blue())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomN(timeout=3600)

            await ctx.response.send_message(embed=embed, view=view)

    @commands.slash_command(name="nhie", description="Get a random never have I ever question.")
    async def nhie_cmd(self, ctx):
        if ctx.channel.id in self.tod_channels:
            url = f"https://api.truthordarebot.xyz/v1/NHIE"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.blue())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomN(timeout=3600)

            msg = await ctx.respond(embed=embed, view=view)
            view.msg = msg
        else:
            await ctx.respond("You can't use this channel for TOD.", ephemeral=True)

    class RandomT(discord.ui.View):
        @discord.ui.button(label=f"Random Truth", style=discord.ButtonStyle.blurple)
        async def t(self, button, ctx):
            await ctx.message.edit(view=None)
            url = f"https://api.truthordarebot.xyz/v1/TRUTH"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.blurple())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomT(timeout=3600)

            await ctx.response.send_message(embed=embed, view=view)

    @commands.slash_command(name="truth", description="Get a random truth.")
    async def truth_cmd(self, ctx):
        if ctx.channel.id in self.tod_channels:
            url = f"https://api.truthordarebot.xyz/v1/TRUTH"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.blurple())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomT(timeout=3600)

            msg = await ctx.respond(embed=embed, view=view)
            view.msg = msg
        else:
            await ctx.respond("You can't use this channel for TOD.", ephemeral=True)

    class RandomW(discord.ui.View):
        @discord.ui.button(label=f"Random WYR", style=discord.ButtonStyle.blurple)
        async def w(self, button, ctx):
            await ctx.message.edit(view=None)
            url = f"https://api.truthordarebot.xyz/v1/WYR"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.default())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomW(timeout=3600)

            await ctx.response.send_message(embed=embed, view=view)
    
    @commands.slash_command(name="wyr", description="Get a random would you rather question.")
    async def wyr_cmd(self, ctx):
        if ctx.channel.id in self.tod_channels:
            url = f"https://api.truthordarebot.xyz/v1/WYR"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.default())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomW(timeout=3600)

            msg = await ctx.respond(embed=embed, view=view)
            view.msg = msg
        else:
            await ctx.respond("You can't use this channel for TOD.", ephemeral=True)


    class RandomP(discord.ui.View):
        @discord.ui.button(label=f"Random Paranoia", style=discord.ButtonStyle.blurple)
        async def p(self, button, ctx):
            await ctx.message.edit(view=None)
            url = f"https://api.truthordarebot.xyz/v1/PARANOIA"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.greyple())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomP(timeout=3600)

            await ctx.response.send_message(embed=embed, view=view)

    @commands.slash_command(name="paranoia", description="Get a random paranoia question.")
    async def paranoia_cmd(self, ctx):
        if ctx.channel.id in self.tod_channels:
            url = f"https://api.truthordarebot.xyz/v1/PARANOIA"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
            embed = discord.Embed(title=data["question"], color = discord.Color.greyple())
            embed.set_footer(text=f"Type: {data['type']} | Rating: {data['rating']} | ID: {data['id']}")
            embed.set_author(name=f"Requested by {ctx.user.name}", icon_url=ctx.user.avatar)

            view = self.RandomP(timeout=3600)

            msg = await ctx.respond(embed=embed, view=view)
            view.msg = msg
        else:
            await ctx.respond("You can't use this channel for TOD.", ephemeral=True)

def setup(client):
    client.add_cog(Tord(client))