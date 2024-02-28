import discord
from discord.ext import commands
import os
from email.message import EmailMessage
import ssl, smtplib

class Botutils(commands.Cog):
    def __init__(self, client):
        self.client = client
        print("botutils initialized")

    def send_email(self, subject, body):
        email_sender = "ayarai304@gmail.com"
        email_password = "ixea ezmf xfdd iegt"
        email_reciever = "ayarai304@gmail.com"

        subject = subject
        body = body
        
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_reciever
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_reciever, em.as_string())
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.client.user}')

    # @commands.Cog.listener()
    # async def on_connect(self):
    #     self.send_email("blahajbot has connected", f"{self.client.user} has gone online with {round(self.client.latency, 3)*1000} ms ping.")

    # @commands.Cog.listener()
    # async def on_disconnect(self):
    #     self.send_email("blahajbot has disconnected", f"{self.client.user} has gone offline.")

    
    @commands.slash_command(name="ping", description="Get the ping of the bot.")
    async def ping(self, ctx):
        await ctx.respond(f"Pong! {round(self.client.latency, 3)*1000} ms", ephemeral=True)

def setup(client):
    client.add_cog(Botutils(client))