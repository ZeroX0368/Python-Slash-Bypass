
import discord
from discord.ext import commands
import requests
import asyncio

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="bypass", description="Bypass a URL using the API")
async def bypass(interaction: discord.Interaction, url: str):
    # Send immediate processing message
    processing_embed = discord.Embed(
        title="🔄 Processando",
        description="Processando seu link...",
        color=0xffaa00,
        timestamp=interaction.created_at
    )
    await interaction.response.send_message(embed=processing_embed)
    
    try:
        # Make request to bypass API
        api_url = f"https://api.solar-x.top/free/bypass?url={url}"
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Create embed
            embed = discord.Embed(
                title="🔓 Bypass Result",
                color=0x00ff00,
                timestamp=interaction.created_at
            )
            
            # Add fields based on API response (excluding Name and Status)
            if isinstance(data, dict):
                for key, value in data.items():
                    # Skip Name and Status fields
                    if key.lower() in ['name', 'status']:
                        continue
                    if isinstance(value, (str, int, float, bool)):
                        embed.add_field(
                            name=key.title().replace('_', ' '),
                            value=str(value)[:1024],  # Discord field value limit
                            inline=True
                        )
            else:
                embed.add_field(
                    name="Result",
                    value=str(data)[:1024],
                    inline=False
                )
            
            embed.add_field(
                name="Original URL",
                value=url[:1024],
                inline=False
            )
            
            embed.set_footer(text=f"Requested by {interaction.user.display_name}")
            
        else:
            embed = discord.Embed(
                title="❌ Error",
                description=f"API returned status code: {response.status_code}",
                color=0xff0000,
                timestamp=interaction.created_at
            )
            embed.add_field(
                name="Original URL",
                value=url[:1024],
                inline=False
            )
    
    except requests.exceptions.Timeout:
        embed = discord.Embed(
            title="⏰ Timeout",
            description="The API request timed out. Please try again later.",
            color=0xffaa00,
            timestamp=interaction.created_at
        )
    
    except requests.exceptions.RequestException as e:
        embed = discord.Embed(
            title="❌ Network Error",
            description=f"Failed to connect to API: {str(e)}",
            color=0xff0000,
            timestamp=interaction.created_at
        )
    
    except Exception as e:
        embed = discord.Embed(
            title="❌ Unexpected Error",
            description=f"An error occurred: {str(e)}",
            color=0xff0000,
            timestamp=interaction.created_at
        )
    
    await interaction.edit_original_response(embed=embed)

bot.run('YOU DISCORD BOT TOKEN')
