import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
bot_key = os.getenv('BOT_KEY')

print(f'BOT_KEY carregada: {bot_key}')

if not bot_key:
    raise ValueError("Token do bot não encontrado. Verifique o arquivo .env!")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

# Dicionário para armazenar as salas temporariamente
salas = {}

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

# COMANDO: Listar e fixar comandos
@bot.command()
async def comandos(ctx: commands.Context):
    ajuda = (
        "**Lista de comandos disponíveis:**\n"
        ".ola - Envia uma saudação ao usuário.\n"
        ".criar_sala <jogo> [max_jogadores] - Cria uma nova sala de jogo (máximo de 4 jogadores por padrão).\n"
        ".entrar_sala <sala_id> - Entra em uma sala de jogo existente.\n"
        ".listar_salas - Lista todas as salas de jogo ativas.\n"
        ".fechar_sala <sala_id> - Fecha uma sala de jogo existente.\n"
        ".chamar <sala_id> <@membro> - Chama um membro para entrar em uma sala de jogo (somente o dono pode chamar).\n"
        "Use `.comando <comando>` para mais detalhes sobre um comando específico."
    )

    # Envia a mensagem com a lista de comandos
    mensagem = await ctx.send(ajuda)

    # Fixar a mensagem no canal
    await mensagem.pin()
    await ctx.send("A lista de comandos foi fixada para fácil acesso!")

# COMANDO: Ola
@bot.command()
async def ola(ctx: commands.Context):
    nome = ctx.author.name
    await ctx.send(f"Olá {nome}! Tudo bem?")

@ola.error
async def ola_error(ctx, error):
    await ctx.send("Ocorreu um erro ao executar o comando 'ola'. Tente novamente!")

# COMANDO: Criar sala
@bot.command()
async def criar_sala(ctx: commands.Context, jogo: str, max_jogadores: int = 4):
    guild = ctx.guild
    sala_id = len(salas) + 1

    # Cria canal de voz
    canal = await guild.create_voice_channel(name=f"Sala-{sala_id}-{jogo}")

    # Salva informações
    salas[sala_id] = {
        "dono": ctx.author.name,
        "jogo": jogo,
        "max_jogadores": max_jogadores,
        "jogadores": [ctx.author.name],
        "canal_id": canal.id
    }

    # Tenta mover o autor para o canal
    if ctx.author.voice:  # Se a pessoa está conectada a algum canal de voz
        await ctx.author.move_to(canal)
        await ctx.send(f"Sala criada! ID: {sala_id}, Jogo: {jogo}. Canal: {canal.mention}. Você foi movido para o canal!")
    else:
        await ctx.send(f"Sala criada! ID: {sala_id}, Jogo: {jogo}. Canal criado: {canal.mention}.\n*Você não foi movido pois não está conectado a um canal de voz.*")

@criar_sala.error
async def criar_sala_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Erro: O número máximo de jogadores precisa ser um número inteiro!\nExemplo: `.criar_sala EldenRing 4`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Erro: Informe pelo menos o nome do jogo!\nExemplo: `.criar_sala EldenRing`")
    else:
        await ctx.send("Ocorreu um erro ao criar a sala. Verifique os parâmetros e tente novamente.")

# COMANDO: Entrar na sala
@bot.command()
async def entrar_sala(ctx: commands.Context, sala_id: int):
    if sala_id in salas:
        sala = salas[sala_id]
        if len(sala["jogadores"]) < sala["max_jogadores"]:
            if ctx.author.name not in sala["jogadores"]:
                sala["jogadores"].append(ctx.author.name)
                await ctx.send(f"{ctx.author.name} entrou na sala {sala_id} ({sala['jogo']}).")
            else:
                await ctx.send("Você já está na sala!")
        else:
            await ctx.send("Sala cheia!")
    else:
        await ctx.send("Sala não encontrada.")

@entrar_sala.error
async def entrar_sala_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Erro: O ID da sala precisa ser um número!\nExemplo: `.entrar_sala 1`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Erro: Você precisa informar o ID da sala.\nExemplo: `.entrar_sala 1`")
    else:
        await ctx.send("Ocorreu um erro ao tentar entrar na sala. Verifique o ID e tente novamente.")

# COMANDO: Chamar membro para sala
@bot.command()
async def chamar(ctx: commands.Context, sala_id: int, membro: discord.Member):
    if sala_id in salas:
        sala = salas[sala_id]
        
        # Verifica se o autor do comando é o dono da sala
        if sala["dono"] != ctx.author.name:
            await ctx.send("Apenas o dono da sala pode chamar membros!")
            return
        
        # Verifica se o membro está na sala
        if membro.name in sala["jogadores"]:
            await ctx.send(f"{membro.name} já está na sala {sala_id}.")
            return

        # Verifica se a sala tem espaço
        if len(sala["jogadores"]) < sala["max_jogadores"]:
            # Tenta mover o membro para o canal
            if membro.voice:
                await membro.move_to(ctx.guild.get_channel(sala["canal_id"]))
                sala["jogadores"].append(membro.name)
                await ctx.send(f"{membro.name} foi movido para a sala {sala_id} ({sala['jogo']}).")
            else:
                await ctx.send(f"{membro.name} não está conectado a um canal de voz.")
        else:
            await ctx.send("Sala cheia! Não há espaço para mais jogadores.")
    else:
        await ctx.send("Sala não encontrada.")

@chamar.error
async def chamar_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Erro: O ID da sala precisa ser um número! Exemplo: `.chamar 1 @membro`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Erro: Informe o ID da sala e mencione o membro a ser chamado. Exemplo: `.chamar 1 @membro`")
    else:
        await ctx.send("Ocorreu um erro ao chamar o membro. Verifique os parâmetros e tente novamente.")

# COMANDO: Listar salas
@bot.command()
async def listar_salas(ctx: commands.Context):
    if not salas:
        await ctx.send("Nenhuma sala aberta no momento.")
        return
    mensagem = "**Salas ativas:**\n"
    for sala_id, info in salas.items():
        mensagem += f"ID {sala_id} | Jogo: {info['jogo']} | Dono: {info['dono']} | Jogadores: {len(info['jogadores'])}/{info['max_jogadores']}\n"
    await ctx.send(mensagem)

@listar_salas.error
async def listar_salas_error(ctx, error):
    await ctx.send("Ocorreu um erro ao listar as salas. Tente novamente.")

# COMANDO: Fechar sala
@bot.command()
async def fechar_sala(ctx: commands.Context, sala_id: int):
    if sala_id in salas:
        if salas[sala_id]["dono"] == ctx.author.name:
            # Deletar o canal criado
            canal_id = salas[sala_id]["canal_id"]
            canal = ctx.guild.get_channel(canal_id)
            if canal:
                await canal.delete()
            del salas[sala_id]
            await ctx.send(f"Sala {sala_id} foi fechada e o canal removido.")
        else:
            await ctx.send("Apenas o dono da sala pode fechá-la.")
    else:
        await ctx.send("Sala não encontrada.")

@fechar_sala.error
async def fechar_sala_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Erro: O ID da sala precisa ser um número!\nExemplo: `.fechar_sala 1`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Erro: Você precisa informar o ID da sala.\nExemplo: `.fechar_sala 1`")
    else:
        await ctx.send("Ocorreu um erro ao tentar fechar a sala. Verifique o ID e tente novamente.")

# Rodar o bot
bot.run(bot_key)
