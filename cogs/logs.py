import discord
from discord.ext import commands
from database import set_logs_channel, get_logs_channel

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Função para buscar o canal de logs configurado no banco de dados
    def get_log_channel(self, guild):
        channel_id = get_logs_channel(guild.id)
        return guild.get_channel(channel_id) if channel_id else None

    # Comando para definir o canal de logs
    # Uso: .setlogs #nome-do-canal
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlogs(self, ctx, channel: discord.TextChannel):
        """Define o canal onde os logs serão enviados."""
        set_logs_channel(ctx.guild.id, channel.id)
        await ctx.send(f"✅ Canal de logs configurado para {channel.mention}")

    # ---------------------- LISTENERS ----------------------

    # Listener: Quando uma mensagem é apagada
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        canal = self.get_log_channel(message.guild)
        if canal and not message.author.bot:
            embed = discord.Embed(title="🗑️ Mensagem Apagada", color=discord.Color.red())
            embed.add_field(name="Autor", value=message.author.mention, inline=False)
            embed.add_field(name="Conteúdo", value=message.content or "*sem conteúdo*", inline=False)
            embed.set_footer(text=f"Canal: {message.channel}")
            await canal.send(embed=embed)

    # Listener: Quando uma mensagem é editada
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        canal = self.get_log_channel(before.guild)
        if canal and not before.author.bot and before.content != after.content:
            embed = discord.Embed(title="✏️ Mensagem Editada", color=discord.Color.orange())
            embed.add_field(name="Autor", value=before.author.mention, inline=False)
            embed.add_field(name="Antes", value=before.content or "*vazio*", inline=False)
            embed.add_field(name="Depois", value=after.content or "*vazio*", inline=False)
            embed.set_footer(text=f"Canal: {before.channel}")
            await canal.send(embed=embed)

    # Listener: Quando um membro entra no servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = self.get_log_channel(member.guild)
        if canal:
            embed = discord.Embed(title="✅ Novo Membro", description=f"{member.mention} entrou no servidor!", color=discord.Color.green())
            embed.set_footer(text=f"ID: {member.id}")
            await canal.send(embed=embed)

    # Listener: Quando um membro sai ou é expulso
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = self.get_log_channel(member.guild)
        if canal:
            embed = discord.Embed(title="❌ Membro Saiu", description=f"{member.name} saiu ou foi expulso.", color=discord.Color.red())
            embed.set_footer(text=f"ID: {member.id}")
            await canal.send(embed=embed)

    # Listener: Quando os cargos de um membro são alterados
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        canal = self.get_log_channel(before.guild)
        if canal and before.roles != after.roles:
            embed = discord.Embed(title="🔧 Alteração de Cargos", color=discord.Color.purple())
            embed.add_field(name="Membro", value=before.mention, inline=False)
            embed.add_field(name="Antes", value=", ".join([r.name for r in before.roles if r.name != "@everyone"]), inline=True)
            embed.add_field(name="Depois", value=", ".join([r.name for r in after.roles if r.name != "@everyone"]), inline=True)
            await canal.send(embed=embed)

    # Listener: Quando um membro é banido
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        canal = self.get_log_channel(guild)
        if canal:
            embed = discord.Embed(title="🚫 Membro Banido", description=f"{user} foi banido.", color=discord.Color.dark_red())
            await canal.send(embed=embed)

    # Listener: Quando um membro é desbanido
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        canal = self.get_log_channel(guild)
        if canal:
            embed = discord.Embed(title="🔓 Membro Desbanido", description=f"{user} foi desbanido.", color=discord.Color.green())
            await canal.send(embed=embed)

# Setup do Cog
async def setup(bot):
    await bot.add_cog(Logs(bot))
