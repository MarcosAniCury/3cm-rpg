#Meus arquivos .py
#Bibliotecas python
import discord
from discord.ext.commands.help import HelpCommand

from Scripts import TOKENs


def get_embed_help_commands(client):  #Embed Command help

  prefix = TOKENs.get_prefix()[0]

  embed_help_commands = discord.Embed(
    title="Comandos",
    description="Bot feito para o Rpg 3CM\n\u200b",
    colour=0xBF00FF,
  )

  embed_help_commands.add_field(
    name="📄Server Comandos📄",
    value="`" + prefix + "ping` - para testar a latência\n"
    "`" + prefix +
    "helpadm || hadm` - comando help para adms **Apenas ADMs**\n\u200b",
    inline=False)

  embed_help_commands.add_field(
    name="🏹RPG de Mesa Comandos⚔️",
    value=
    "`rd<numero de lados> <quantidades de vezes>` - Rodar um dado de n lados m vezes\n"
    "`" + prefix + "criar_ficha` - Criar um profile no rpg\n"
    "`" + prefix + "perfil` - Pode olhar seu profile no rpg\n"
    "`" + prefix +
    "descrição` - Olhar a descrição de algo (substituir o espaço por _ no nome)\n"
    "`" + prefix +
    "distribuir_pontos` - distribuir os pontos que você possui\n"
    "\nBot em construção, mais comandos serão adicionados no futuro",
    inline=False)

  embed_help_commands.set_footer(
    text="Develop by:Miko#9331",
    icon_url=f'{client.get_user(239498713347653633).avatar.url}')
  embed_help_commands.set_author(
    name="3cm Rpg",
    icon_url=f'{client.get_user(869952210979663883).avatar.url}')

  return embed_help_commands


def get_help_adm_command(client):  #Emd Commnad helpadm

  prefix = TOKENs.get_prefix()[0]

  help_adm_command = discord.Embed(
    title="Comandos Adms",
    description="Bot feito para ajudar os jogadores do rpg epic\n\u200b",
    colour=0xBF00FF,  #laranja
  )

  help_adm_command.add_field(
    name="📄Server Comandos📄",
    value="`" + prefix + "ativar_modulo <modulo>` - ativar um modulo do bot\n"
    "`" + prefix + "desativar_modulo <modulo>` - desativar um modulo do bot\n"
    "`" + prefix +
    "reiniciar_modulo <modulo>` - reiniciar um modulo do bot\n\u200b",
  )

  help_adm_command.add_field(
    name="🏹RPG de Mesa Comandos ADM⚔️",
    value="`" + prefix +
    "atualizar_status <mention player> <status> <value>` - alterar o status de um jogador Ex:Vida\n"
    "`" + prefix +
    "add_xp <mention player> <value>` - adiciona ou remove xp de um player\n"
    "`" + prefix +
    "atualizar_pontos <mention player> <value>` - alterar os pontos de um player\n"
    "`" + prefix + "add_skill` - Criar uma nova skill\n"
    "\nBot em construção, mais comandos serão adicionados no futuro",
    inline=False)

  help_adm_command.set_footer(
    text="Develop by:Miko#9331",
    icon_url=f'{client.get_user(239498713347653633).avatar.url}')
  help_adm_command.set_author(name="3cm Rpg",
                              icon_url=f'{client.user.avatar.url}')

  return help_adm_command
