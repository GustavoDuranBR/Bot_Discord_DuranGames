import discord
from discord.ext import commands
import json
import os

data_file = 'data/reaction_roles.json'

if not os.path.exists(data_file):
    with open(data_file, 'w') as f:
        json.dump({}, f)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = self.carregar_dados()

    def carregar_dados(self):
        """Carrega os dados dos reaction roles de forma segura."""
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def salvar_dados(self):
        """Salva os dados de reaction roles no arquivo."""
        with open(data_file, 'w') as f:
            json.dump(self.data, f)

    # Comando para adicionar Reaction Role
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def adicionar_reaction_role(self, ctx, mensagem_id: int, emoji, cargo: discord.Role):
        if cargo.position >= ctx.guild.me.top_role.position:
            await ctx.send("❌ O bot não tem permissão para atribuir esse cargo.")
            return

        self.data[str(mensagem_id)] = {"emoji": emoji, "role_id": cargo.id}
        self.salvar_dados()

        await ctx.send(f"✅ Reaction Role configurado: {emoji} -> {cargo.name}")

    # Comando para listar Reaction Roles configurados
    @commands.command(name="listar_reaction_roles")
    async def listar_reaction_roles(self, ctx):
        if not self.data:
            await ctx.send("❌ Nenhum Reaction Role configurado.")
            return

        msg = "**Reaction Roles configurados:**\n"
        for msg_id, info in self.data.items():
            role = ctx.guild.get_role(info['role_id'])
            msg += f"📌 **Mensagem ID:** `{msg_id}` | Emoji: `{info['emoji']}` | Cargo: `{role.name if role else 'Cargo não encontrado'}`\n"

        await ctx.send(msg)

    # Comando para remover todos os cargos de Reaction Roles do usuário
    @commands.command(name="remover_reaction_roles")
    async def remover_reaction_roles(self, ctx, member: discord.Member = None):
        member = member or ctx.author  # Se não especificar, remove os cargos do próprio autor
        cargos_removidos = []

        for info in self.data.values():
            role = ctx.guild.get_role(info['role_id'])
            if role in member.roles:
                await member.remove_roles(role)
                cargos_removidos.append(role.name)

        if cargos_removidos:
            await ctx.send(f"🚫 Cargos removidos de {member.mention}: {', '.join(cargos_removidos)}")
        else:
            await ctx.send(f"{member.mention} não possui nenhum cargo configurado com Reaction Roles.")

    # Listener para adicionar cargo ao reagir
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction, user):
        """Atribui o cargo baseado na reação do usuário"""
        if reaction.message.channel.name == '✅・cargos':  # Canal onde as reações devem ser feitas
            if reaction.emoji == '🎮':  # Emoji para o cargo "Jogador"
                role = discord.utils.get(user.guild.roles, name='Jogador')  # Nome do cargo
                if role:
                    await user.add_roles(role)
                    print(f"{user.name} recebeu o cargo {role.name}")
                else:
                    print(f"Cargo 'Jogador' não encontrado!")
            elif reaction.emoji == '🏆':  # Emoji para o cargo "Vencedor"
                role = discord.utils.get(user.guild.roles, name='Vencedor')  # Nome do cargo
                if role:
                    await user.add_roles(role)
                    print(f"{user.name} recebeu o cargo {role.name}")
                else:
                    print(f"Cargo 'Vencedor' não encontrado!")

    @commands.command()
    async def verificar_cargos(self, ctx, user: discord.Member = None):
        """Comando para verificar os cargos de um usuário"""
        if user is None:
            user = ctx.author  # Se nenhum usuário for especificado, usa o autor do comando

        cargos = [role.name for role in user.roles]
        await ctx.send(f"{user.name} tem os seguintes cargos: {', '.join(cargos)}")

    # Listener para remover cargo se o usuário tirar a reação
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return

        if str(payload.message_id) in self.data and payload.emoji.name == self.data[str(payload.message_id)]["emoji"]:
            role = guild.get_role(self.data[str(payload.message_id)]["role_id"])
            if role:
                await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
