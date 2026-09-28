import os
import threading
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask

# 1. Background web server for Render port scan
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord bot is online!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Start Flask in a background thread
threading.Thread(target=run_web, daemon=True).start()

# 2. Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Sync slash commands globally across Discord
    await bot.tree.sync()
    print(f"Bot is logged in as {bot.user}")

# 3. Slash Command with Defer (Fixes "Application did not respond")
@bot.tree.command(name="generate", description="Generate an image using A Dark Corner Generator")
async def generate(interaction: discord.Interaction, prompt: str):
    # Tells Discord "Bot is thinking..." immediately (prevents 3-second timeout)
    await interaction.response.defer()

    url = "https://image-generation-perchance.hf.space/api/predict"
    
    payload = {
        "data": [
            prompt,
            "",       # negative prompt
            "random", # seed
            7.5,      # guidance scale
        ]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    image_url = result["data"][0]
                    
                    embed = discord.Embed(title="A Dark Corner Image", description=f"**Prompt:** {prompt}")
                    embed.set_image(url=image_url)
                    
                    # Send result after deferring using followup
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("⚠️ Failed to generate image from Perchance. Please try again.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
