from discord.ext import commands
import json
import os

# Caminho do arquivo de tags
tags_file = 'data/tags.json'

# Verificar se o arquivo de tags existe, caso contrário, criar
if not os.path.exists(tags_file):
    with open(tags_file, 'w') as f:
        json.dump({}, f)

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, nome):
        """Comando para exibir o conteúdo de uma tag existente"""
        try:
            with open(tags_file, 'r') as f:
                tags = json.load(f)
        except json.JSONDecodeError:
            await ctx.send("Erro ao carregar as tags. O arquivo pode estar corrompido.")
            return
        
        # Verificar se a tag existe e responder com o conteúdo
        if nome in tags:
            await ctx.send(tags[nome])
        else:
            await ctx.send("Tag não encontrada.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def adicionar_tag(self, ctx, nome, *, conteudo):
        """Comando para adicionar uma nova tag"""
        if len(conteudo) > 1000:
            await ctx.send("O conteúdo da tag é muito grande. Limite de 1000 caracteres.")
            return
        
        try:
            with open(tags_file, 'r') as f:
                tags = json.load(f)
        except json.JSONDecodeError:
            await ctx.send("Erro ao carregar as tags. O arquivo pode estar corrompido.")
            return
        
        # Adicionar ou atualizar a tag
        tags[nome] = conteudo
        
        # Salvar as tags de volta no arquivo
        try:
            with open(tags_file, 'w') as f:
                json.dump(tags, f, indent=4)
        except IOError:
            await ctx.send("Erro ao salvar as tags. Tente novamente mais tarde.")
            return
        
        await ctx.send(f"Tag `{nome}` criada com sucesso!\nConteúdo: {conteudo[:100]}...")  # Mostra o início do conteúdo

    @commands.command()
    async def listar_tags(self, ctx):
        """Comando para listar todas as tags"""
        try:
            with open(tags_file, 'r') as f:
                tags = json.load(f)
        except json.JSONDecodeError:
            await ctx.send("Erro ao carregar as tags. O arquivo pode estar corrompido.")
            return

        if tags:
            tag_list = "\n".join([f"`{tag}`" for tag in tags.keys()])
            await ctx.send(f"Tags disponíveis:\n{tag_list}")
        else:
            await ctx.send("Nenhuma tag encontrada.")

# Função setup para adicionar o cog
async def setup(bot):
    await bot.add_cog(Tags(bot))
