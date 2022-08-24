# Meus arquivos .py
from Armazenamento import TOKENs
from Armazenamento import Embeds3cm
from Armazenamento import CRUD

# Bibliotecas python
import discord
import os
import discord.ext.commands
from discord.ext import commands

client = commands.Bot(command_prefix=TOKENs.get_prefix(), intents=discord.Intents.all())

embeds_obj = Embeds3cm.epic_3cm(client)
banco = CRUD.crud()


# ----------Bot Status Inicio------------

@client.event
async def on_ready():
    print("BOT ONLINE")
    print(client.user.name)
    print(client.user.id)
    print("----------------------")

    await client.change_presence(activity=discord.Game("\"3cm h\" alias \"cm h\""))  # Alterar status do bot
    await load_all_cogs()


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

    await client.change_presence(activity=discord.Game("\"3cm h\" alias \"cm h\""))  # Alterar status do bot


# ----------Bot Status Fim------------

# -----------Modulos Inicio-------------

@client.command()
@commands.has_permissions(administrator=True)
async def ativar_modulo(ctx, extension):
    await ctx.send("modulo " + extension + " ativado")
    await client.load_extension(f'Scripts.Cogs.{extension}')


@client.command()
@commands.has_permissions(administrator=True)
async def desativar_modulo(ctx, extension):
    await ctx.send("modulo " + extension + " desativado")
    await client.unload_extension(f'Scripts.Cogs.{extension}')


@client.command()
@commands.has_permissions(administrator=True)
async def reiniciar_modulo(ctx, ext):
    await desativar_modulo(ctx, ext)
    await ativar_modulo(ctx, ext)


async def load_all_cogs():
    for filename in os.listdir('Scripts/Cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'Scripts.Cogs.{filename[:-3]}')  # Load cortando o .py do arquivo


# -----------Modulos Fim-------------

# -------------Comandos Help Inicio-----------

class MyHelp(commands.HelpCommand):  # Overwrite help
    def __init__(self):
        super().__init__(command_attrs={
            'aliases': ['h'],
        })

    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        HelpEmbed = embeds_obj.get_embed_help_commands()
        await channel.send(embed=HelpEmbed)


client.help_command = MyHelp()  # Quando digitar <prefix> help vai chamar a funcao


# -------------Comandos Help Fim-----------

# ------------Comandos Importantes Inicio-----------

@client.command()
async def ping(ctx):  # Comando para testar a latencia
    await ctx.send(f'Pong, {round(client.latency * 1000)}ms')


@client.command(aliases=["hadm"])
@commands.has_permissions(administrator=True)
async def helpadm(ctx):  # Help para administradores
    HelpAdmEmbed = embeds_obj.get_help_adm_command()
    await ctx.send(embed=HelpAdmEmbed)

    # ------------Comandos Importantes Fim-----------

    # -------------Tratamento de exceção Inicio-------------------

    @client.event
    async def on_command_error(ctx, error):  # Tratamento de exceções
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Por favor passe todos os argumentos necessários", delete_after=20)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Comando não encontrado, digite 3cm help para ver os comandos ativos", delete_after=20)
            await ctx.message.delete()
        elif isinstance(error, commands.NotOwner):
            await ctx.send("Apenas o dono do server pode executar esse comando", delete_after=20)
        elif isinstance(error, commands.CheckFailure):
            pass
        else:
            await ctx.send("Erro encontrado, reporte a algum adm urgente:erro \"" + error.args[0] + "\"",
                           delete_after=60)
            print(error)
            print("--------------------------------")


# -------------Tratamento de exceção Fim-------------------

client.run(TOKENs.get_token())  # Token do bot
