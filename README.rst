.. image:: https://i.imgur.com/OO3QuEw.png
   :alt: wavecord
   :align: center

================================================================================
.
================================================================================

.. image:: https://img.shields.io/pypi/v/wavecord.svg?style=for-the-badge&color=blueviolet
   :target: https://pypi.org/project/wavecord/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/wavecord.svg?style=for-the-badge
   :target: https://pypi.org/project/wavecord/
   :alt: Supported Python versions

.. image:: https://img.shields.io/github/actions/workflow/status/error44s/wavecord/ci.yml?label=build&style=for-the-badge
   :target: https://github.com/error44s/wavecord/actions
   :alt: Build Status

.. image:: https://img.shields.io/github/license/error44s/wavecord?style=for-the-badge
   :target: https://github.com/error44s/wavecord/blob/main/LICENSE
   :alt: License

.. image:: https://img.shields.io/badge/typing-checked-blue?style=for-the-badge
   :alt: Typing Checked

wavecord is a **2025-ready**, fully typed, async Lavalink wrapper built for **Pycord bots**.  
Fast, clean, feature-rich — and made for serious music bots.

-------------------------------------------------------------------------------
✨ Features
-------------------------------------------------------------------------------

- 🎵 **Full Music Support** – play, pause, resume, stop, skip, volume, shuffle
- 🔄 **Reconnect & Session Restore** – handles node disconnects gracefully
- 🎶 **Track Metadata** – title, author, duration, description
- 📦 **Plugin Support** – Spotify, Deezer, Apple Music (via Lavalink plugins)
- 💡 **Modern Python** – fully typed, Black + Ruff + Pyright ready
- 🚀 **Performance-focused** – scalable across large bots

-------------------------------------------------------------------------------
📦 Installation
-------------------------------------------------------------------------------

Install from ``PyPI``

.. code-block:: bash

   pip install wavecord

Install from source ``(latest dev version)``

.. code-block:: bash

   git clone https://github.com/error44s/wavecord
   cd wavecord
   pip install -e .

Requires Python ``3.13``

-------------------------------------------------------------------------------
🚀 Quick Example
-------------------------------------------------------------------------------

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

-------------------------------------------------------------------------------
📘 Documentation
-------------------------------------------------------------------------------

Full documentation will be available soon on: https://wavecord.dev

In the meantime, see the `examples/` folder.

-------------------------------------------------------------------------------
🤝 Contributing
-------------------------------------------------------------------------------

Contributions are welcome!

- Fork the project
- Use a branch format like: ``feature/your-feature``
- Ensure your code passes:
  - **Black** for formatting
  - **Ruff** for linting
  - **Pyright** for type-checking
- All PRs require review by a maintainer

Read the full guidelines in ``CONTRIBUTING.md``.

-------------------------------------------------------------------------------
🛡 License – MIT
-------------------------------------------------------------------------------

This project is licensed under the MIT License.

You are **free to use, modify, and distribute** this software —  
but **without any warranty**. See the LICENSE file for full terms.

-------------------------------------------------------------------------------
💖 Made with passion for the Discord & Python community
-------------------------------------------------------------------------------

Maintained by the **wavecord** team and contributors.
