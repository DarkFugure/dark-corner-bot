import os
import threading
import aiohttp
import discord
from discord.ext import commands
from flask import Flask

# 1. Fake web server to satisfy Render's port check
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
    print(f"Bot is logged in as {bot.user}")

@bot.command(name="generate")
async def generate(ctx, *, prompt: str):
    await ctx.send(f"🎨 Generating image for prompt: **{prompt}**...")

    # Perchance API Endpoint for A Dark Corner Generator
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
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("⚠️ Failed to generate image from Perchance. Please try again.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
