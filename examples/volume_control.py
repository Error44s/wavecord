import asyncio

import discord
from discord.ext import commands

from wavecord import Node, Track, WaveClient, WavecordException

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    node = Node(host="localhost", port=2333, password="youshallnotpass")
    await WaveClient.initialize(bot, node)

@bot.command()
async def join(ctx: commands.Context):
    if not ctx.author.voice:
        return await ctx.send("🔇 You are not in a voice channel.")

    channel = ctx.author.voice.channel
    player = WaveClient.get_player(ctx.guild.id)
    await player.connect(channel)
    await ctx.send(f"🔊 Joined {channel.name}.")

@bot.command()
async def play(ctx: commands.Context, *, query: str):
    player = WaveClient.get_player(ctx.guild.id)

    # Lavalink REST API for search
    async with player.node.session.get(
        f"{player.node.base_url}/v4/loadtracks",
        params={"identifier": f"ytsearch:{query}"},
        headers={"Authorization": player.node.password},
    ) as resp:
        data = await resp.json()

    tracks = data.get("data", [])
    if not tracks:
        return await ctx.send("❌ No results found.")

    track = Track.build(tracks[0])
    await player.play(track)
    await ctx.send(f"🎶 Now playing: **{track.title}**")

@bot.command()
async def volume(ctx: commands.Context, level: int):
    player = WaveClient.get_player(ctx.guild.id)
    await player.set_volume(level)
    await ctx.send(f"🔊 Volume set to {level}/1000.")

@bot.command()
async def pause(ctx: commands.Context):
    player = WaveClient.get_player(ctx.guild.id)
    await player.pause(True)
    await ctx.send("⏸️ Paused playback.")

@bot.command()
async def resume(ctx: commands.Context):
    player = WaveClient.get_player(ctx.guild.id)
    await player.pause(False)
    await ctx.send("▶️ Resumed playback.")

bot.run("YOUR_BOT_TOKEN")
