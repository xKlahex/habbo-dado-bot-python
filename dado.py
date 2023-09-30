import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import random
from PIL import Image
from io import BytesIO
import asyncio

# Configuración del bot
prefijo = "!"
bot = commands.Bot(command_prefix=prefijo)
slash = SlashCommand(bot, sync_commands=True)

# Rutas a las imágenes locales
rutas_imagenes = [
    "numeros_imagenes/1.png",
    "numeros_imagenes/2.png",
    "numeros_imagenes/3.png",
    "numeros_imagenes/4.png",
    "numeros_imagenes/5.png",
    "numeros_imagenes/6.png"
]

# Ruta a la imagen de dado giratorio local
ruta_dado_giratorio = "numeros_imagenes/dado_giratorio.gif"

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'¡Bot listo como {bot.user.name} - {bot.user.id}!')

# Comando para lanzar un dado con animación (slash command)
@slash.slash(
    name="dado",
    description="Lanza un dado de 6 caras con animación"
)
async def lanzar_dado(ctx: SlashContext):
    try:
        # Obtener una ruta aleatoria de imagen del dado
        ruta_seleccionada = random.choice(rutas_imagenes)

        # Obtener el número correspondiente al resultado
        numero_resultado = int(ruta_seleccionada.split("/")[-1].split(".")[0])

        # Enviar el mensaje con la imagen giratoria y una descripción al mismo canal
        #mensaje_giratorio = await ctx.send(content="Lanzando el dado...", file=discord.File(ruta_dado_giratorio))

        # Esperar un tiempo para dar la apariencia de que el dado está girando
        await asyncio.sleep(2)

        # Eliminar la imagen giratoria
        #await mensaje_giratorio.delete()

        # Obtener la imagen seleccionada y enviarla en un mensaje Embed con descripción
        imagen = Image.open(ruta_seleccionada)
        with BytesIO() as image_binary:
            imagen.save(image_binary, format='PNG')
            image_binary.seek(0)

            # Crear un mensaje Embed con descripción y la imagen
            embed = discord.Embed(description=f"Resultado: {numero_resultado}")
            embed.set_image(url="attachment://dado.png")
            embed.set_footer(text=f"El dado fue lanzado por {ctx.author.display_name}",
                             icon_url=ctx.author.avatar_url)

            # Enviar el mensaje Embed con la imagen al mismo canal
            await ctx.send(embed=embed, file=discord.File(fp=image_binary, filename='dado.png'))

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        await ctx.send("¡Hubo un error al procesar la imagen del dado. Inténtalo de nuevo!")

# Ejecutar el bot con el token
bot.run('') #TOKEN AQUI
