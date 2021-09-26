#Meus arquivos .py
from Armazenamento import TOKENs
from Armazenamento import Embeds3cm
from Armazenamento import CRUD

#Bibliotecas python
import discord
import os
import discord.ext.commands
from discord.ext import commands

client = commands.Bot(intents = discord.Intents.all(), command_prefix=TOKENs.get_prefix())

embeds_obj = Embeds3cm.epic_3cm(client)
banco = CRUD.crud()

#----------Bot Status Inicio------------

@client.event
async def on_ready():
    print("BOT ONLINE") 
    print(client.user.name)
    print(client.user.id)
    print("----------------------")

    await client.change_presence(activity=discord.Game("\"3cm h\" alias \"cm h\"")) #Alterar status do bot

@client.event
async def on_disconnect(erro):
    print("Bot desconectado verifique sua conexão")

@client.event
async def on_resumed():
    print("BOT ONLINE - Bot foi reconectado") 
    print(client.user.name)
    print(client.user.id)
    print("----------------------")
    global embeds_obj 
    global banco
    embeds_obj = Embeds3cm.epic_3cm(client)
    banco = CRUD.crud()

    await client.change_presence(activity=discord.Game("\"3cm h\" alias \"cm h\"")) #Alterar status do bot

#----------Bot Status Fim------------

#-----------Funcoes do Server Inicio-----------

async def check_not_exist_player(ctx):
    id = ctx.author.id
    retorno = not banco.check_player(id)
    if not retorno:
        await ctx.send("Você já possui uma ficha de personagem")
    return retorno

async def check_exist_player(ctx):
    id = ctx.author.id
    retorno = banco.check_player(id)
    if not retorno:
        await ctx.send("Você não possui uma ficha de personagem")
    return retorno

def find_player_by_id(memberId,banco):
    player = banco.read("players", {'id_player' : str(memberId)})
    print(player)
    return player

async def update_status(dict_player, status, valor): #Cria uma nova Referencia

    retorno = None
    valorMaximo = dict_player['atributos_variaveis'][status]['maxima']
    valorAnterior = dict_player['atributos_variaveis'][status]['atual']
    dict_player['atributos_variaveis'][status]['atual'] = str(int(valor) + int(valorAnterior))
    valorAtual = dict_player['atributos_variaveis'][status]['atual']
    #Caso ultrapasse de zero
    if int(valorAnterior) + int(valor) < 0 and status == "vida":
        valorAtual = "0"
    if int(valorAtual) <= int(valorMaximo) and int(valorAnterior) + int(valor) >= 0:
        retorno = [dict_player,valorAtual,valorMaximo]
    return retorno

def add_XP(ctx, dict_player, amount_xp): #Altera a Referencia

    xp_atual = int(dict_player['atributos_variaveis']['xp']['atual'])
    dict_player['atributos_variaveis']['xp']['atual'] = str(amount_xp + xp_atual)
    xp_atual = amount_xp + xp_atual
    xp_maximo = int(dict_player['atributos_variaveis']['xp']['maximo'])
    if xp_atual >= xp_maximo:
        dict_player['atributos_variaveis']['xp']['atual'] = str(xp_atual - xp_maximo)
        dict_player['atributos_variaveis']['xp']['maximo'] = str(xp_maximo + 100) 
        level_atual = int(dict_player['atributos_variaveis']['xp']['level']) + 1
        dict_player['atributos_variaveis']['xp']['level'] = str(level_atual)

#-----------Funcoes do Server Fim-----------

#-----------Modulos Inicio-------------

@client.command()
@commands.has_permissions(administrator = True)
async def ativar_modulo(ctx, extension):
    await ctx.send("modulo "+extension+" ativado")
    client.load_extension(f'Scripts.{extension}')

@client.command()
@commands.has_permissions(administrator = True)
async def desativar_modulo(ctx, extension):
    await ctx.send("modulo "+extension+" desativado")
    client.unload_extension(f'Scripts.{extension}')

@client.command()
@commands.has_permissions(administrator = True)
async def reiniciar_modulo(ctx, ext):
    await desativar_modulo(ctx,ext)
    await ativar_modulo(ctx,ext)

for filename in os.listdir('./Scripts'):
    if filename.endswith('.py'):
        client.load_extension(f'Scripts.{filename[:-3]}') #Load cortando o .py do arquivo

#-----------Modulos Fim-------------

#-------------Comandos Help Inicio-----------

class MyHelp(commands.HelpCommand): #Overwrite help
    def __init__(self):
        super().__init__(command_attrs={
        'aliases': ['h'],
        })

    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        HelpEmbed = embeds_obj.get_embed_help_commands()
        await channel.send(embed=HelpEmbed)

client.help_command = MyHelp() #Quando digitar <prefix> help vai chamar a funcao
#-------------Comandos Help Fim-----------

#------------Comandos Importantes Inicio-----------

@client.command()
async def ping(ctx): #Comando para testar a latencia
    await ctx.send(f'Pong, {round(client.latency * 1000)}ms')

@client.command(aliases = ["hadm"])
@commands.has_permissions(administrator = True)
async def helpadm(ctx): #Help para administradores
    HelpAdmEmbed = embeds_obj.get_help_adm_command()
    await ctx.send(embed=HelpAdmEmbed)

#------------Comandos Importantes Fim-----------

#-------------Tratamento de exceção Inicio-------------------

    @client.event
    async def on_command_error(ctx, error): #Tratamento de exceções
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Por favor passe todos os argumentos necessários", delete_after = 20)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando não encontrado, digite help help para ver os comandos ativos", delete_after = 20)
            await ctx.message.delete()
        elif isinstance(error, commands.NotOwner):
            await ctx.send("Apenas o dono do server pode executar esse comando", delete_after = 20)
        elif isinstance(error, commands.CheckFailure):
            pass
        else:
            await ctx.send("Erro encontrado, reporte a algum adm urgente:erro \""+error.args[0]+"\"", delete_after = 60)
            print(error)
            print("--------------------------------")
    
#-------------Tratamento de exceção Fim-------------------

client.run(TOKENs.get_token()) #Token do bot