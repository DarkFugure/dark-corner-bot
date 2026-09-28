import os
import threading
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
    # Defer response to allow time for image generation without timing out
    await interaction.response.defer()

    # Perchance / Hugging Face Gradio Endpoint
    url = "https://image-generation-perchance.hf.space/run/predict"
    
    # Generate a numeric seed for API compatibility
    seed_val = random.randint(1, 999999999)

    payload = {
        "data": [
            prompt,
            "ugly, distorted, low quality, bad anatomy", # negative prompt
            seed_val,                                    # numeric seed
            7.5                                          # guidance scale
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        # Increased timeout to 90 seconds for heavy generation tasks
        timeout = aiohttp.ClientTimeout(total=90)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=payload, headers=headers) as response:
                print(f"API Response Status: {response.status}")
                if response.status == 200:
                    result = await response.json()
                    
                    # Gradio returns data as a list of outputs
                    if "data" in result and len(result["data"]) > 0:
                        image_data = result["data"][0]
                        
                        # Handle array/object response format from Gradio
                        if isinstance(image_data, list):
                            image_url = image_data[0]
                        elif isinstance(image_data, dict):
                            image_url = image_data.get("url") or image_data.get("name")
                        else:
                            image_url = image_data

                        embed = discord.Embed(title="A Dark Corner Image", description=f"**Prompt:** {prompt}")
                        embed.set_image(url=image_url)
                        await interaction.followup.send(embed=embed)
                    else:
                        await interaction.followup.send("⚠️ API responded, but no image data was returned.")
                else:
                    error_text = await response.text()
                    print(f"Error output: {error_text}")
                    await interaction.followup.send(f"⚠️ Failed to generate image (Status Code `{response.status}`). Please try again.")
    except Exception as e:
        print(f"Exception during generation: {e}")
        await interaction.followup.send(f"An error occurred: `{e}`")

bot.run(os.getenv("DISCORD_TOKEN"))
