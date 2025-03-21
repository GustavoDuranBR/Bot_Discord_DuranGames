import discord
from discord.ext import commands
import json
import os

warns_file = 'data/warns.json'
if not os.path.exists(warns_file):
    with open(warns_file, 'w') as f:
        json.dump({}, f)

class Moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def carregar_warns(self):
        """Função para carregar os warns de forma segura."""
        try:
            with open(warns_file, 'r') as f:
                warns = json.load(f)
                return warns
        except (json.JSONDecodeError, FileNotFoundError):
            # Se o arquivo JSON estiver vazio, corrompido ou não encontrado, inicializa com um dicionário vazio
            with open(warns_file, 'w') as f:
                json.dump({}, f)
            return {}

    def salvar_warns(self, warns):
        """Função para salvar os warns no arquivo de forma segura."""
        with open(warns_file, 'w') as f:
            json.dump(warns, f)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def avisar(self, ctx, membro: discord.Member, *, motivo=None):
        warns = self.carregar_warns()  # Carrega os warns de forma segura
        if str(membro.id) not in warns:
            warns[str(membro.id)] = []
        warns[str(membro.id)].append(motivo or "Sem motivo.")
        self.salvar_warns(warns)  # Salva os warns de forma segura
        await ctx.send(f"{membro.mention} foi advertido. Total: {len(warns[str(membro.id)])}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warns(self, ctx, membro: discord.Member):
        warns = self.carregar_warns()  # Carrega os warns de forma segura
        user_warns = warns.get(str(membro.id), [])
        if user_warns:
            msg = f"{membro.name} tem {len(user_warns)} advertências:\n"
            for i, motivo in enumerate(user_warns, 1):
                msg += f"{i}. {motivo}\n"
        else:
            msg = f"{membro.name} não tem advertências."
        await ctx.send(msg)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banir(self, ctx, membro: discord.Member, *, motivo=None):
        """Comando para banir um membro com a razão fornecida."""
        try:
            if not ctx.guild.me.guild_permissions.ban_members:
                await ctx.send("Eu não tenho permissão para banir membros.")
                return
            await membro.ban(reason=motivo)
            await ctx.send(f"{membro.name} foi banido.")
        except Exception as e:
            await ctx.send(f"Erro ao banir o membro: {e}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, membro: discord.Member, *, motivo=None):
        """Comando para expulsar um membro com a razão fornecida."""
        try:
            if not ctx.guild.me.guild_permissions.kick_members:
                await ctx.send("Eu não tenho permissão para expulsar membros.")
                return
            await membro.kick(reason=motivo)
            await ctx.send(f"{membro.name} foi expulso.")
        except Exception as e:
            await ctx.send(f"Erro ao expulsar o membro: {e}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def limpar(self, ctx, quantidade: int):
        """Comando para limpar mensagens no canal atual."""
        try:
            if quantidade <= 0:
                await ctx.send("Por favor, forneça um número válido de mensagens para apagar.")
                return

            # Limpa apenas mensagens que não sejam de bot
            mensagens_a_deletar = []
            async for msg in ctx.channel.history(limit=quantidade + 1):
                if not msg.author.bot:
                    mensagens_a_deletar.append(msg)

            # Deletando as mensagens
            await ctx.channel.delete_messages(mensagens_a_deletar)
            await ctx.send(f"Apaguei {len(mensagens_a_deletar)} mensagens.", delete_after=5)
        except Exception as e:
            await ctx.send(f"Erro ao limpar mensagens: {e}")

# A função setup agora é assíncrona
async def setup(bot):
    await bot.add_cog(Moderacao(bot))  # Agora usamos await para aguardar a corrotina
