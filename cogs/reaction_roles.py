import discord
from discord.ext import commands
import json
import os

# Caminho para o arquivo de dados
DATA_FILE = 'data/reaction_roles.json'

# Verifica se o arquivo de dados existe; se não, cria um novo
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = self.carregar_dados()

    def carregar_dados(self):
        """Carrega os dados dos reaction roles de forma segura."""
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def salvar_dados(self):
        """Salva os dados de reaction roles no arquivo."""
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def adicionar_reaction_role(self, ctx, mensagem_id: int, emoji: str, cargo: discord.Role):
        """Adiciona um reaction role a uma mensagem específica."""
        if cargo.position >= ctx.guild.me.top_role.position:
            await ctx.send("❌ O bot não tem permissão para atribuir esse cargo.")
            return

        if str(mensagem_id) not in self.data:
            self.data[str(mensagem_id)] = {}

        self.data[str(mensagem_id)][emoji] = cargo.id
        self.salvar_dados()

        # Adiciona a reação à mensagem especificada
        canal = ctx.channel
        mensagem = await canal.fetch_message(mensagem_id)
        await mensagem.add_reaction(emoji)

        await ctx.send(f"✅ Reaction Role configurado: {emoji} -> {cargo.name}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def remover_reaction_role(self, ctx, mensagem_id: int, emoji: str):
        """Remove um reaction role específico de uma mensagem."""
        if str(mensagem_id) in self.data and emoji in self.data[str(mensagem_id)]:
            del self.data[str(mensagem_id)][emoji]
            if not self.data[str(mensagem_id)]:
                del self.data[str(mensagem_id)]
            self.salvar_dados()
            await ctx.send(f"✅ Reaction Role removido para o emoji {emoji} na mensagem {mensagem_id}.")
        else:
            await ctx.send("❌ Nenhuma configuração encontrada para esse emoji nessa mensagem.")

    @commands.command(name="listar_reaction_roles")
    async def listar_reaction_roles(self, ctx):
        """Lista todos os Reaction Roles configurados."""
        if not self.data:
            await ctx.send("❌ Nenhum Reaction Role configurado.")
            return

        msg = "**Reaction Roles configurados:**\n"
        for msg_id, emojis in self.data.items():
            msg += f"📌 **Mensagem ID:** `{msg_id}`\n"
            for emoji, role_id in emojis.items():
                role = ctx.guild.get_role(role_id)
                msg += f"   - Emoji: `{emoji}` | Cargo: `{role.name if role else 'Cargo não encontrado'}`\n"

        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Atribui o cargo baseado na reação do usuário."""
        if str(payload.message_id) in self.data:
            if payload.emoji.name in self.data[str(payload.message_id)]:
                guild = self.bot.get_guild(payload.guild_id)
                role_id = self.data[str(payload.message_id)][payload.emoji.name]
                role = guild.get_role(role_id)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member and not member.bot:
                        await member.add_roles(role)
                        print(f"{member.name} recebeu o cargo {role.name}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Remove o cargo quando a reação é retirada."""
        if str(payload.message_id) in self.data:
            if payload.emoji.name in self.data[str(payload.message_id)]:
                guild = self.bot.get_guild(payload.guild_id)
                role_id = self.data[str(payload.message_id)][payload.emoji.name]
                role = guild.get_role(role_id)
                if role:
                    member = guild.get_member(payload.user_id)
                    if member and not member.bot:
                        await member.remove_roles(role)
                        print(f"{member.name} teve o cargo {role.name} removido")

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
