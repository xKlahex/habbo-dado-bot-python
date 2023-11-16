import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import random
from PIL import Image
from io import BytesIO
import asyncio

prefix = "!"
bot = commands.Bot(command_prefix=prefix)
slash = SlashCommand(bot, sync_commands=True)

image_paths = [
    "number_images/1.png",
    "number_images/2.png",
    "number_images/3.png",
    "number_images/4.png",
    "number_images/5.png",
    "number_images/6.png"
]

spinning_dice_path = "number_images/spinning_dice.gif"

@bot.event
async def on_ready():
    print(f'Bot ready as {bot.user.name} - {bot.user.id}!')

@slash.slash(
    name="dice",
    description="Rolls a 6-sided dice with animation"
)
async def roll_dice(ctx: SlashContext):
    try:
        selected_path = random.choice(image_paths)

        result_number = int(selected_path.split("/")[-1].split(".")[0])
        await asyncio.sleep(2)

        image = Image.open(selected_path)
        with BytesIO() as image_binary:
            image.save(image_binary, format='PNG')
            image_binary.seek(0)
            
            embed = discord.Embed(description=f"Result: {result_number}")
            embed.set_image(url="attachment://dice.png")
            embed.set_footer(text=f"The dice was rolled by {ctx.author.display_name}",
                             icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed, file=discord.File(fp=image_binary, filename='dice.png'))

    except Exception as e:
        print(f"Error processing the image: {e}")
        await ctx.send("There was an error processing the dice image. Try again!")

bot.run('')
