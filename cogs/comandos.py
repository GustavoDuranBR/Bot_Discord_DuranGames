import discord
from discord.ext import commands
import asyncio

class ComandosBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.salvas = {}
        self.loop_ativo = False  # Variável para verificar se o loop de estatísticas está ativo

    # Comando de ajuda
    @commands.command()
    async def ajuda(self, ctx):
        print("Comando ajuda foi chamado!")  # Isso ajuda a saber se o comando está sendo chamado
        ajuda_msg = """
        **Comandos Disponíveis:**

        **.ajuda** - Mostra essa mensagem de ajuda.
        **.avisos [mensagem]** - Envia uma notificação no canal de avisos.
        **.configurar_estatisticas [intervalo em minutos]** - Envia estatísticas periodicamente no canal de estatísticas.
        **.ajuda_reaction_roles** - Mostra como usar o sistema de Reaction Roles.
        """
        await ctx.send(ajuda_msg)

    # Comando de ping
    @commands.command()
    async def ping(self, ctx):
        """Comando simples para testar a resposta do bot"""
        await ctx.send("Pong!")
    
    # Comando de notificação
    @commands.command()
    @commands.has_permissions(administrator=True)  # Apenas administradores podem usar
    async def avisos(self, ctx, *, mensagem: str):
        """Envia uma mensagem de notificação no canal '📢・avisos'"""
        canal = discord.utils.get(ctx.guild.text_channels, name='📢・avisos')
        if canal:
            await canal.send(f"**ATENÇÃO!** {mensagem}")
        else:
            await ctx.send("Canal de avisos não encontrado!")

    # Comando para configurar estatísticas
    @commands.command()
    @commands.has_permissions(administrator=True)  # Apenas administradores podem usar
    async def configurar_estatisticas(self, ctx, intervalo: int):
        """Envia estatísticas periodicamente no canal de estatísticas"""
        # Verifica se o loop já está ativo
        if self.loop_ativo:
            await ctx.send("O envio de estatísticas já está configurado. Por favor, aguarde a execução atual.")
            return

        # Marca o loop como ativo
        self.loop_ativo = True
        
        try:
            await ctx.send(f"✅ Estatísticas configuradas com sucesso! O bot enviará estatísticas a cada {intervalo} minutos.")
            
            # Um loop infinito pode ser arriscado, então vamos verificar a execução de cada intervalo
            while self.loop_ativo:
                canal = discord.utils.get(ctx.guild.text_channels, name='📊・estatísticas')
                if canal:
                    membros_online = len([member for member in ctx.guild.members if member.status != discord.Status.offline])
                    await canal.send(f"**Estatísticas:** Membros Online: {membros_online}")
                else:
                    await ctx.send("Canal de estatísticas não encontrado!")
                    break  # Se o canal não for encontrado, interrompe o loop
                
                await asyncio.sleep(intervalo * 60)  # Aguarda pelo intervalo configurado em minutos
        except Exception as e:
            await ctx.send(f"Erro ao configurar as estatísticas: {e}")
        finally:
            self.loop_ativo = False  # Garante que o loop será desativado no final

    # Comando para parar estatísticas
    @commands.command()
    @commands.has_permissions(administrator=True)  # Apenas administradores podem usar
    async def parar_estatisticas(self, ctx):
        """Para o envio de estatísticas"""
        if not self.loop_ativo:
            await ctx.send("O envio de estatísticas não está ativo.")
            return
        
        self.loop_ativo = False  # Interrompe o loop
        await ctx.send("🚫 Envio de estatísticas foi interrompido.")

    # Comando de Reaction Roles
    @commands.command()
    async def ajuda_reaction_roles(self, ctx):
        """Informa como usar o sistema de Reaction Roles"""
        ajuda_msg = """
        **Como usar os Reaction Roles:**
        
        1. Vá até o canal **✅・cargos**.
        2. Reaja à mensagem com o emoji correspondente ao cargo que você deseja ganhar.
        3. Você automaticamente receberá o cargo relacionado ao emoji escolhido.

        **Exemplo de comandos Reaction Roles configurados:**
        - React com 🎮 para ganhar o cargo de **Jogador**.
        - React com 🏆 para ganhar o cargo de **Vencedor**.
        """
        await ctx.send(ajuda_msg)

    @commands.command()
    async def verificar_todos_cargos(self, ctx, usuario: discord.Member):
        """Mostra todos os cargos do usuário mencionado."""
        print(f"Comando verificar_todos_cargos chamado por {ctx.author}")  # Debug
        
        cargos = [role.name for role in usuario.roles if role.name != "@everyone"]
        
        if cargos:
            cargos_lista = ", ".join(cargos)
            await ctx.send(f"{usuario.name} possui os seguintes cargos: {cargos_lista}")
        else:
            await ctx.send(f"{usuario.name} não possui nenhum cargo além do padrão.")

# Função para adicionar o cog ao bot
async def setup(bot):
    await bot.add_cog(ComandosBot(bot))
