import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Listener: Quando uma mensagem for apagada
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Quando uma mensagem é apagada, envia uma notificação no canal 'logs'."""
        canal = discord.utils.get(message.guild.text_channels, name='logs')
        if canal and not message.author.bot:
            await canal.send(f"Mensagem apagada: {message.content} | Autor: {message.author}")

    # Listener: Quando uma mensagem for editada
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Quando uma mensagem for editada, envia a mudança no canal 'logs'."""
        canal = discord.utils.get(before.guild.text_channels, name='logs')
        if canal and not before.author.bot:
            # Verifica se o conteúdo da mensagem realmente mudou
            if before.content != after.content:
                await canal.send(f"Mensagem editada por {before.author}: `{before.content}` -> `{after.content}`")

# Função para adicionar o cog ao bot
async def setup(bot):
    await bot.add_cog(Logs(bot))
