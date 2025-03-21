import discord
from discord.ext import commands

class VoiceManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = []

    @commands.command(name="criarsala")
    @commands.has_permissions(manage_channels=True)  # Garantir que o usuário tenha permissão
    async def criar_sala(self, ctx, *, nome: str = "Nova Sala"):
        # Verificar se a categoria "Salas de Voz" existe
        category = discord.utils.get(ctx.guild.categories, name="Salas de Voz")
        if not category:
            # Criar categoria se não existir
            try:
                category = await ctx.guild.create_category("Salas de Voz")
                await ctx.send("Categoria 'Salas de Voz' criada com sucesso!")
            except discord.Forbidden:
                await ctx.send("Não tenho permissão para criar a categoria 'Salas de Voz'.")
                return
            except discord.HTTPException:
                await ctx.send("Ocorreu um erro ao tentar criar a categoria.")
                return

        # Verificar se já existe uma sala com o mesmo nome
        existing_channel = discord.utils.get(category.voice_channels, name=nome)
        if existing_channel:
            await ctx.send(f"Já existe uma sala de voz com o nome `{nome}`.")
            return

        # Criar o canal de voz
        try:
            channel = await ctx.guild.create_voice_channel(nome, category=category)
            self.temp_channels.append(channel.id)
            await ctx.send(f"Sala de voz `{nome}` criada! ✅")
        except discord.Forbidden:
            await ctx.send("Não tenho permissão para criar canais de voz.")
        except discord.HTTPException:
            await ctx.send("Ocorreu um erro ao tentar criar o canal de voz.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Deletar sala temporária vazia
        if before.channel and before.channel.id in self.temp_channels:
            if len(before.channel.members) == 0:
                try:
                    await before.channel.delete()
                    self.temp_channels.remove(before.channel.id)
                except discord.Forbidden:
                    print(f"Permissão negada para deletar a sala: {before.channel.name}")
                except discord.HTTPException:
                    print(f"Erro ao tentar deletar a sala: {before.channel.name}")

    # Função para limpar as salas temporárias quando o cog for descarregado
    async def cog_unload(self):
        for channel_id in self.temp_channels:
            channel = self.bot.get_channel(channel_id)
            if channel:
                try:
                    await channel.delete()
                except discord.Forbidden:
                    print(f"Permissão negada para deletar a sala {channel.name}")
                except discord.HTTPException:
                    print(f"Erro ao tentar deletar a sala {channel.name}")

# Função para adicionar o cog ao bot
async def setup(bot):
    await bot.add_cog(VoiceManager(bot))
