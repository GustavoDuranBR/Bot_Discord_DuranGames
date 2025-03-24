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
                "🏆": "VIP",
                "🛠️": "Moderador"
            }

            for emoji, cargo_nome in emojis_cargos.items():
                cargo = discord.utils.get(guild.roles, name=cargo_nome)
                if cargo:
                    print(f"Adicionando reação '{emoji}' ao cargo '{cargo_nome}'")
                    await message.add_reaction(emoji)
        else:
            print("Canal '✅・cargos' não encontrado.")

        print("Servidor configurado com sucesso!")

    # Verificação de cargo ao adicionar uma reação
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Verifica se a reação foi adicionada na mensagem correta
        if reaction.message.id == 1352568323186888744:  # ID da mensagem com os Reaction Roles
            cargo_nome = ""
            if reaction.emoji == "🎮":
                cargo_nome = "Jogador"
            elif reaction.emoji == "🏆":
                cargo_nome = "VIP"
            elif reaction.emoji == "🛠️":
                cargo_nome = "Moderador"

            # Obtém o cargo do servidor
            guild = reaction.message.guild
            cargo = discord.utils.get(guild.roles, name=cargo_nome)
            
            if cargo in user.roles:
                print(f"O usuário {user.name} tem o cargo {cargo_nome}.")
            else:
                print(f"O usuário {user.name} NÃO tem o cargo {cargo_nome}.")

    # Comando para verificar se o usuário tem o cargo
    @commands.command()
    async def verificar_cargo(self, ctx, usuario: discord.Member, cargo_nome: str):
        print(f"Comando verificar_cargo chamado por {ctx.author.name} para o usuário {usuario.name} e cargo {cargo_nome}.")
        
        cargo = discord.utils.get(ctx.guild.roles, name=cargo_nome)
        
        if cargo is None:
            await ctx.send(f"O cargo {cargo_nome} não foi encontrado no servidor.")
            print(f"Cargo {cargo_nome} não encontrado.")
            return

        if cargo in usuario.roles:
            await ctx.send(f"{usuario.name} tem o cargo {cargo_nome}.")
            print(f"{usuario.name} tem o cargo {cargo_nome}.")
        else:
            await ctx.send(f"{usuario.name} NÃO tem o cargo {cargo_nome}.")
            print(f"{usuario.name} NÃO tem o cargo {cargo_nome}.")

async def setup(bot):
    await bot.add_cog(SetupServer(bot))
