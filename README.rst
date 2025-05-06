.. image:: https://i.imgur.com/OO3QuEw.png
   :alt: wavecord
   :align: center

A modern, typed Lavalink wrapper for Pycord bots.

================================================================================
.
================================================================================

.. raw:: html

   <p align="center">
     <img src="https://img.shields.io/pypi/v/wavecord?style=for-the-badge&color=blueviolet&logo=pypi&logoColor=white" />
     <img src="https://img.shields.io/pypi/pyversions/wavecord?style=for-the-badge&logo=python&logoColor=white" />
     <img src="https://img.shields.io/github/actions/workflow/status/error44s/wavecord/ci.yml?label=build&style=for-the-badge&logo=github" />
     <img src="https://img.shields.io/github/license/error44s/wavecord?style=for-the-badge" />
     <img src="https://img.shields.io/badge/typing-checked-blue?style=for-the-badge" />
   </p>

================================================================================
.
================================================================================

.. raw:: html

   <h3>Features</h3>

- **Full Music Support** – play, pause, resume, stop, skip, volume, shuffle  
- **Reconnect & Session Restore** – handles node disconnects gracefully  
- **Track Metadata** – title, author, duration, description  
- **Plugin Support** – Spotify, Deezer, Apple Music (via Lavalink plugins)  
- **Modern Python** – fully typed, Black + Ruff + Pyright ready  
- **Performance-focused** – scalable across large bots

.. raw:: html

   <h3>Installation</h3>

Install from ``PyPI``

.. code-block:: bash

   pip install wavecord

Install from source (``latest dev version``)

.. code-block:: bash

   $ git clone https://github.com/error44s/wavecord
   $ cd wavecord
   $ pip install -e .

Requires Python ``3.13``

.. raw:: html

   <h3>Quick Example</h3>

.. code-block:: python

   from discord.ext import commands
   from wavecord import WaveClient, Node

   bot = commands.Bot(command_prefix="!")

   @bot.event
   async def on_ready():
       node = Node(host="localhost", port=2333, password="youshallnotpass")
       await WaveClient.initialize(bot, node)
       print("✅ Wavecord ready.")

   @bot.command()
   async def play(ctx, *, query):
       player = WaveClient.get_player(ctx.guild.id)
       await player.connect(ctx.author.voice.channel)
       tracks = await player.node.search_tracks(query)
       await player.play(tracks[0])
       await ctx.send(f"🎶 Now playing: {tracks[0].title}")

.. raw:: html

   <h3>Documentation</h3>

Full documentation will be available soon on: https://wavecord.dev

In the meantime, see the `examples/` folder.

.. raw:: html

   <h3>Contributing</h3>

Contributions are welcome!

- Fork the project  
- Use a branch format like: ``feature/your-feature``  
- Ensure your code passes:
  - **Black** for formatting
  - **Ruff** for linting
  - **Pyright** for type-checking  
- All PRs require review by a maintainer

Read the full guidelines in ``CONTRIBUTING.md``.

.. raw:: html

   <h3>License – MIT</h3>

This project is licensed under the MIT License.

You are **free to use, modify, and distribute** this software —  
but **without any warranty**. See the LICENSE file for full terms.

.. raw:: html

   <h3>Made with passion for the Discord & Python community</h3>

Maintained by the **wavecord** team and contributors.
