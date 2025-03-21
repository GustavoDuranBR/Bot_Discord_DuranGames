import discord
from discord.ext import commands
import json
import os

data_file = 'data/auto_roles.json'

# Se o arquivo não existir ou estiver vazio, cria um JSON básico
if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
    with open(data_file, 'w') as f:
        json.dump({"role_id": None}, f)  # Inicializa o arquivo com um objeto vazio com a chave 'role_id'

class AutoRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Carrega o cargo automático ao iniciar
        self.load_data()

    def load_data(self):
        """Carregar os dados do arquivo JSON"""
        try:
            with open(data_file, 'r') as f:
                self.data = json.load(f)
        except json.JSONDecodeError:
            # Caso o JSON esteja corrompido ou vazio, inicializa novamente
            self.data = {"role_id": None}
            with open(data_file, 'w') as f:
                json.dump(self.data, f)

    def save_data(self):
        """Salvar os dados no arquivo JSON"""
        with open(data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    # Listener: Quando alguém entra, recebe o cargo automático
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role_id = self.data.get("role_id")
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                # Verifica se o bot tem permissão para adicionar o cargo
                if member.guild.me.guild_permissions.manage_roles:
                    await member.add_roles(role)
                    print(f"Cargo {role.name} atribuído a {member.mention}.")
                else:
                    print(f"Permissão negada para atribuir o cargo {role.name}.")
            else:
                print(f"Cargo com ID {role_id} não encontrado.")

    # COMANDO 1: Definir cargo automático
    @commands.command(name="definir_auto_role")
    @commands.has_permissions(manage_roles=True)
    async def definir_auto_role(self, ctx, cargo: discord.Role):
        """Comando para definir o cargo automático"""
        # Verifica se o cargo existe no servidor
        if cargo not in ctx.guild.roles:
            await ctx.send(f"❌ O cargo `{cargo.name}` não existe no servidor.")
            return
        
        self.data["role_id"] = cargo.id
        self.save_data()  # Salva os dados após a alteração
        await ctx.send(f"✅ Cargo automático configurado: `{cargo.name}`")

    # COMANDO 2: Remover configuração de cargo automático
    @commands.command(name="remover_auto_role")
    @commands.has_permissions(manage_roles=True)
    async def remover_auto_role(self, ctx):
        """Comando para remover o cargo automático"""
        self.data["role_id"] = None
        self.save_data()  # Salva os dados após a alteração
        await ctx.send("❌ Cargo automático removido!")

    # COMANDO 3: Ver cargo automático atual
    @commands.command(name="ver_auto_role")
    async def ver_auto_role(self, ctx):
        """Comando para ver o cargo automático atual"""
        role_id = self.data.get("role_id")
        if role_id:
            role = ctx.guild.get_role(role_id)
            await ctx.send(f"🔍 Cargo automático atual: `{role.name}`")
        else:
            await ctx.send("Nenhum cargo automático configurado no momento.")
    
    # Comando 4: Listar todos os cargos do servidor
    @commands.command(name="listar_cargos")
    async def listar_cargos(self, ctx):
        """Comando para listar todos os cargos do servidor"""
        cargos = ctx.guild.roles
        if cargos:
            cargos_list = "\n".join([role.name for role in cargos])
            await ctx.send(f"📜 Cargos existentes no servidor:\n{cargos_list}")
        else:
            await ctx.send("❌ Não há cargos no servidor.")

async def setup(bot):
    await bot.add_cog(AutoRoles(bot))
