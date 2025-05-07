### 🤝 Contributing to wavecord
---

First off, thanks for taking the time to contribute!  
**Wavecord** thrives thanks to passionate developers like you.  
We aim to build the best modern Lavalink wrapper for Pycord – and you can help shape it. 🚀

---

### 📐 Project Structure

This library is written in **modern Python 3.13** using

- ✅ Full type hints
- ✅ Linting with Ruff
- ✅ Auto-formatting with Black
- ✅ Static typing with Pyright
- ✅ Clean modular structure:
  - `nodes/` – Lavalink node communication
  - `players/` – Voice + queue management
  - `tracks/` – Track metadata & resolution
  - `events/` – Internal & Lavalink event system

---

### 🔧 Setup for Local Development

> ✅ Requires Python 3.13

Clone the repo and install dev dependencies
```bash
git clone https://github.com/error44s/wavecord.git
cd wavecord
pip install -e .[dev]
```

Install tooling
```bash
pip install ruff black pyright
```

---

### 🧼 Code Quality

#### Before pushing code, always run the following
```bash
ruff .         # Lint (PEP8, unused imports, etc.)
black .        # Auto-format
pyright        # Type check
```
#### Your pull request must pass all three.

---

### 🌱 Branch Naming
#### Use meaningful branch names for clarity

| Type     | Format                |
| -------- | --------------------- |
| Feature  | `feat/player-volume`  |
| Fix      | `fix/track-metadata`  |
| Docs     | `docs/readme-update`  |
| Refactor | `refactor/event-hook` |

---

### ✅ Pull Request Checklist
- [ ] My code runs without errors
- [ ] I’ve run `ruff`, `black`, and `pyright`
- [ ] My PR targets `main` or `dev`
- [ ] I’ve tested my feature/fix locally
- [ ] I’ve added docs/comments if needed

---

### 🧪 GitHub Actions
#### On each pull request, the following run automatically

- 🧼 Black – code formatting
- 🔍 Ruff – code linting
- 🧠 Pyright – static typing

> ❌ PRs that fail checks cannot be merged.
#### Maintainers must review and approve your PR before it’s merged.

---

### 💬 Need Help?
- Open a GitHub Discussion
- Or join our future Discord (planned)

---

### ❤️ Thank You
You're helping shape one of the best music bot libraries for Discord.
We appreciate every contribution – no matter how small.

Together, let's make wavecord awesome. 🌊🎧
