import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Carregar variáveis do .env
load_dotenv()

# Obter o GUILD_ID do .env
GUILD_ID = int(os.getenv('GUILD_ID'))  # Convertendo para inteiro

class SetupServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(GUILD_ID)

        if guild is None:
            print(f"Não encontrei o servidor com ID {GUILD_ID}")
            return

        print(f"Bot conectado ao servidor: {guild.name}")

        # Criação das Categorias
        categorias = ['📢・INFORMAÇÕES', '💬・GERAL', '🎮・GAMES', '🤖・BOT-COMANDOS']
        for categoria_nome in categorias:
            category = discord.utils.get(guild.categories, name=categoria_nome)
            if category is None:
                print(f"Categoria '{categoria_nome}' não encontrada. Criando...")
                category = await guild.create_category(categoria_nome)
            else:
                print(f"Categoria '{categoria_nome}' já existe.")

        # Criação dos Canais
        canais_informacoes = ['📜・regras', '📢・avisos', '✅・cargos', '👋・boas-vindas']
        canais_geral = ['💭・chat-geral', '📸・mídia-e-memes']
        canais_games = ['🎮・procura-duo', '🎤・sala-voz-1', '🎤・sala-voz-2']
        canais_bot = ['🤖・comandos-do-bot', '📊・estatísticas', '🔧・suporte', '🎮・jogos']

        # Função para criar canais
        async def criar_canais(categoria_nome, canais):
            category = discord.utils.get(guild.categories, name=categoria_nome)
            for canal_nome in canais:
                if categoria_nome == '🎮・GAMES':  # Canais de voz
                    if discord.utils.get(guild.voice_channels, name=canal_nome) is None:
                        print(f"Criando canal de voz: {canal_nome}")
                        await guild.create_voice_channel(canal_nome, category=category)
                else:  # Canais de texto
                    if discord.utils.get(guild.text_channels, name=canal_nome) is None:
                        print(f"Criando canal de texto: {canal_nome}")
                        await guild.create_text_channel(canal_nome, category=category)

        # Criando os canais nas respectivas categorias
        await criar_canais('📢・INFORMAÇÕES', canais_informacoes)
        await criar_canais('💬・GERAL', canais_geral)
        await criar_canais('🎮・GAMES', canais_games)
        await criar_canais('🤖・BOT-COMANDOS', canais_bot)

        # Criando os Reaction Roles
        await asyncio.sleep(1)  # Espera 1 segundo para garantir que os canais estejam criados
        channel_comandos = discord.utils.get(guild.text_channels, name="✅・cargos")
        
        if channel_comandos:
            print("Canal '✅・cargos' encontrado! Enviando mensagem...")
            message = await channel_comandos.send("Reaja com um emoji para obter um cargo!")

            # Emojis e cargos correspondentes
            emojis_cargos = {
                "🎮": "Jogador",
                "🏆": "VIP"
            }

            for emoji, cargo_nome in emojis_cargos.items():
                cargo = discord.utils.get(guild.roles, name=cargo_nome)
                if cargo:
                    print(f"Adicionando reação '{emoji}' ao cargo '{cargo_nome}'")
                    await message.add_reaction(emoji)
        else:
            print("Canal '✅・cargos' não encontrado.")

        print("Servidor configurado com sucesso!")

async def setup(bot):
    await bot.add_cog(SetupServer(bot)) 