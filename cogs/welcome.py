from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()
REGRAS_ID = os.getenv("REGRAS_ID")

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Obtendo o canal de boas-vindas pelo nome
        channel_boas_vindas = discord.utils.get(member.guild.text_channels, name="👋・boas-vindas")
        
        # ID do canal de regras, que pode ser configurado no servidor
        id_canal_regras = REGRAS_ID  
        
        # Construir a mensagem de boas-vindas
        mensagem = (
            f"🎮 Bem-vindo(a), {member.mention}! \n"
            f"🚨 Não esqueça de conferir as <#{id_canal_regras}>🚨 \n\n"
            f"▶️ Já conhece o nosso canal no YouTube? \n"
            f"(https://www.youtube.com/@DuranGames)"
        )

        # Enviar mensagem no canal de boas-vindas, se existir
        if channel_boas_vindas:
            try:
                await channel_boas_vindas.send(mensagem)
            except discord.Forbidden:
                await channel_boas_vindas.send("O bot não tem permissão para enviar mensagens neste canal.")
        else:
            # Caso o canal de boas-vindas não exista, envia no canal padrão do servidor (system_channel)
            system_channel = member.guild.system_channel
            if system_channel:
                try:
                    await system_channel.send(mensagem)
                except discord.Forbidden:
                    await system_channel.send("O bot não tem permissão para enviar mensagens no canal padrão.")
            else:
                # Caso não exista nem o canal de boas-vindas nem o system_channel, o bot não poderá enviar a mensagem
                print(f"Falha ao enviar a mensagem de boas-vindas para {member.name}. Canal de boas-vindas ou canal do sistema ausente.")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
