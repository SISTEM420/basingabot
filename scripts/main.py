#Basinga bot 
#Made by Arturo Jorge
#Version: 1.1.0

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
memids = []

class VoteButtons(discord.ui.View):

    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.value = True
        self.votes_event = asyncio.Event()

    @discord.ui.button(label="KICK", style=discord.ButtonStyle.green, emoji="👍")
    async def positive_vote(self, interaction: discord.Interaction, button: discord.ui.Button):
        global positive_votes
        global negative_votes
        positive_votes += 1
        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name="Votes:")
        embed.add_field(name=f"F1: {positive_votes} | F2: {negative_votes}", value="------------")
        await interaction.response.edit_message(embed=embed)
        self.votes_event.set()

    @discord.ui.button(label="DON'T KICK", style=discord.ButtonStyle.red, emoji="👎")
    async def negative_vote(self, interaction: discord.Interaction, button: discord.ui.Button):
        global negative_votes
        global positive_votes
        negative_votes += 1
        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name="Votes:")
        embed.add_field(name=f"F1: {positive_votes} | F2: {negative_votes}", value="------------")
        await interaction.response.edit_message(embed=embed)
        self.votes_event.set()

    async def on_timeout(self):
        self.value = False
        self.stop()

    async def wait(self):
        global positive_votes
        global negative_votes
        while positive_votes < len(memids) / 2 and negative_votes <= len(memids) / 2:
            await self.votes_event.wait()
            self.votes_event.clear()

@client.command()
async def vtk(ctx, *, member: discord.Member):
    global negative_votes
    global positive_votes
    global memids

    negative_votes = 0
    positive_votes = 0
    memids = []

    channel_id = ctx.message.author.voice.channel.id
    v_channel = client.get_channel(channel_id)
    members = v_channel.members

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

@client.event
async def on_ready():
    print("The bot is ready!")
    print("-----------------")

@client.command()
async def fishreact(ctx):
    fishes = ('🐟', '🎣', '🐠', '🐡', '🦈', '🐬', '🐳', '🐋', '🦐', '🦑', '🐙')

    target_id = ctx.message.reference.message_id
    target_message = await ctx.fetch_message(target_id)
    for fish in fishes:
        await target_message.add_reaction(fish)

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

