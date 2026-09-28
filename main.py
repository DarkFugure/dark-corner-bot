import os
import threading
import urllib.parse
import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask

# Your Discord Server ID
GUILD_ID = 1461507856023945230  

# 1. Background web server for Render port scan
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord bot is online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

# 2. Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"Bot logged in as {bot.user} and synced commands instantly to guild {GUILD_ID}!")

# 3. Slash Command with Defer
@bot.tree.command(name="generate", description="Generate an image using A Dark Corner Generator")
async def generate(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()

    try:
        # Encode prompt safely for URL format
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 999999)
        
        # Reliable Pollinations Image API Endpoint
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"

        embed = discord.Embed(title="A Dark Corner Image", description=f"**Prompt:** {prompt}")
        embed.set_image(url=image_url)
        
        await interaction.followup.send(embed=embed)

    except Exception as e:
        print(f"Exception during generation: {e}")
        await interaction.followup.send(f"An error occurred: `{e}`")

bot.run(os.getenv("DISCORD_TOKEN"))
