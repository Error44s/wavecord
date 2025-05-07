import asyncio
from discord.ext import commands
from wavecord import WaveClient, Node, Track

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await WaveClient.initialize(bot, Node("localhost", password="youshallnotpass"))

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    player = WaveClient.get_player(ctx.guild.id)
    await player.connect(channel)
    await ctx.send(f"Joined {channel.name}")

@bot.command()
async def play(ctx, *, query):
    node = WaveClient.get_node()
    response = await node.load_tracks(query)
    track = Track.build(response["tracks"][0])
    
    player = WaveClient.get_player(ctx.guild.id)
    await player.play(track)
    await ctx.send(f"Now playing: {track.title}")

bot.run("YOUR_TOKEN")
