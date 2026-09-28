import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# Start the web server in a background thread
threading.Thread(target=run_web_server, daemon=True).start()
import io
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image, ImageDraw

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def generate_placeholder_image(prompt: str) -> io.BytesIO:
    """Creates a placeholder image with the prompt text."""
    img = Image.new("RGB", (512, 512), color=(30, 30, 35))
    draw = ImageDraw.Draw(img)
    
    text = f"Placeholder Image\nPrompt: {prompt}"
    draw.text((20, 240), text, fill=(255, 255, 255))
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) globally.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="generate", description="Generate an image from a prompt")
@app_commands.describe(prompt="What would you like to generate?")
async def generate(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    
    image_bytes = await generate_placeholder_image(prompt)
    discord_file = discord.File(fp=image_bytes, filename="generated_image.png")
    
    await interaction.followup.send(
        content=f"**Prompt:** {prompt}",
        file=discord_file
    )

bot.run(TOKEN)