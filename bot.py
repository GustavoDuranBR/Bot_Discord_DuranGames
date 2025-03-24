import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from database import connect_db


# Carrega as variáveis do .env
load_dotenv()
TOKEN = os.getenv("BOT_KEY")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.command()
async def teste(ctx):
    await ctx.send("Comando de teste funcionando!")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# Função para carregar as extensões de forma assíncrona
async def load_cogs():
    extensions = [
        'cogs.moderacao',
        'cogs.reaction_roles',
        'cogs.logs',
        'cogs.auto_roles',
        'cogs.tags',
        'cogs.comandos',
        'cogs.setup_server',
        'cogs.voice_manager',
        'cogs.welcome'  
    ]
    
    for ext in extensions:
        try:
            await bot.load_extension(ext)  # Usar await aqui para garantir a execução assíncrona
            print(f"{ext} carregada com sucesso!")
        except Exception as e:
            print(f"Erro ao carregar {ext}: {e}")

# Inicializador principal
async def main():
    await load_cogs()  # Agora usamos await para chamar a função assíncrona de carregar cogs
    
    try:
        await bot.start(TOKEN)  # Inicia o bot de forma assíncrona
    except KeyboardInterrupt:
        print("Bot desconectado com sucesso.")
        await bot.close()

# Roda o bot corretamente
if __name__ == "__main__":
    connect_db()  # Cria tabela se não existir
    asyncio.run(main())
