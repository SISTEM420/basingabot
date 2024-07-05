#Basinga bot 
#Made by Arturo Jorge
#Version: 1.0.0

#TODO add a fish react function

import discord
import asyncio
from discord import member
from discord.ext import commands
from constants import *


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = '&', intents=intents)

negative_votes = 0
positive_votes = 0

@client.command()
async def votekick(ctx, *, member: discord.Member):
    channel_id = ctx.message.author.voice.channel.id
    v_channel = client.get_channel(channel_id) 
    members = v_channel.members
    memids = []
    
    for mem in members:
        memids.append(mem.id)
        
    view = VoteButtons(ctx)
    await ctx.reply(f"{ctx.message.author} wants to kick {member}", view=view)

    await view.wait()

    if positive_votes >= len(memids) / 2:
        await member.move_to(channel=None, reason="Votekick")
        await ctx.send(f"{member} was kicked.")
    else:
        await ctx.send(f"{member} wasn't kicked.")
        

class VoteButtons(discord.ui.View):

    def __init__(self, ctx):
        super().__init__(timeout=10)
        self.ctx = ctx
        self.value = True
        self.votes_event = asyncio.Event()

    @discord.ui.button(label="KICK", style=discord.ButtonStyle.green, emoji="👍")
    async def positive_vote(self, interaction: discord.Interaction, button:discord.ui.Button):
        global positive_votes
        positive_votes += 1
        button.label = str(positive_votes)
        embed = discord.Embed(color= discord.Color.random())
        embed.set_author(name= "You voted:")
        embed.add_field(name="KICK", value="nice >:)")
        await interaction.response.send_message(embed=embed, ephemeral = True)
        self.votes_event.set()
        

    @discord.ui.button(label="DON'T KICK", style=discord.ButtonStyle.red, emoji="👎")
    async def negative_vote(self, interaction: discord.Interaction, button:discord.ui.Button):
        global negative_votes
        negative_votes += 1
        button.label = str(negative_votes)
        embed = discord.Embed(color= discord.Color.random())
        embed.set_author(name= "You voted: ")
        embed.add_field(name="DON'T KICK", value="what a nice guy")
        await interaction.response.send_message(embed=embed, ephemeral = True)
        self.votes_event.set()

    async def on_timeout(self):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        self.value = False
        self.stop()

    async def wait(self):
        await self.votes_event.wait()

@client.event
async def on_ready():
    print("bot ready to cum!")
    print("-----------------")


@client.command()
async def bazinga(ctx):
    await ctx.send("BAZINGA!")


@client.command(pass_content = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Not in a channel, can't join.")

@client.command(pass_content = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        ctx.send("Not in a voice channel.")

@client.command()
async def prueba(ctx):
    
    view = VoteButtons()
    await ctx.reply("Vota:", view=view)


client.run(BOTTOKEN)

