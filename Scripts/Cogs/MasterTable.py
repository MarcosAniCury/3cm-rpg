#Meus arquivos .py
from Scripts.Database.CRUD import CRUD

#Bibliotecas python
from discord.ext import commands
import discord
from Scripts.Utils.UtilsFunctions import find_player_by_id, update_status, add_XP, update_pontos


class master_table(commands.Cog):

  def __init__(self, client):
    self.client = client

  #Evento
  @commands.Cog.listener()
  async def on_ready(self):
    print("Modulo master_table Carregado")
    print("----------------------")

  @commands.Cog.listener()
  async def on_disconnect(self):
    print("Modulo master_table desconectado")
    print("---------------------")

  @commands.command(aliases=["as"])
  @commands.is_owner()
  async def atualizar_status(self, ctx, player: discord.Member, status, valor):
    status = status.lower()
    dict_player = find_player_by_id(player.id)
    dict_player_update = update_status(dict_player.copy(), status, valor)

    #Canal de log
    canal_log = self.client.get_channel(873616219700334622)
    if dict_player_update == None:
      await ctx.send(
        "Operação inválida, o player não pode ultrapassar o valor maximo/minimo de status ",
        delete_after=60)
      await canal_log.send(
        "Ouve uma tentativa invalida de alteração nos status do jogador **" +
        player.name + "**")
    else:
      CRUD.update_item("players", dict_player_update[0])
      status_string = status + " do jogador **" + player.name + "** atualizado:__**" + dict_player_update[
        1] + "/" + dict_player_update[2] + "**__"
      await ctx.send(status_string)
      await canal_log.send(status_string)

  @commands.command(aliases=["ap"])
  @commands.is_owner()
  async def atualizar_pontos(self, ctx, player: discord.Member, valor):
    dict_player = find_player_by_id(player.id)
    dict_player_update = update_pontos(dict_player.copy(), int(valor))

    #Canal de log
    canal_log = self.client.get_channel(873616219700334622)
    if dict_player_update == None:
      await ctx.send(
        "Operação inválida, o player não pode ter menos que 0 de pontos",
        delete_after=60)
      await canal_log.send(
        "Ouve uma tentativa invalida de alteração nos status do jogador **" +
        player.name + "**")
    else:
      print(str(dict_player_update))
      CRUD.update_item("players", dict_player_update)
      status_string = "Pontos do jogador **" + player.name + "** atualizado de __**" + str(
        dict_player['pontos_de_conquista']) + "**__ para __**" + str(
          dict_player_update['pontos_de_conquista']) + "**__"
      await ctx.send(status_string)
      await canal_log.send(status_string)

  @commands.command(aliases=["ax"])
  @commands.is_owner()
  async def add_xp(self, ctx, player: discord.Member, valor):
    dict_player = find_player_by_id(player.id)
    level_anterior = dict_player['atributos_variaveis']['xp']['level']

    add_XP(ctx, dict_player.copy(), int(valor))

    #Confirmação
    mensagem_confirmacao = "Tem certeza que irá adicionar " + valor + " de XP para o usuário " + player.name + "(S/N):"

    level_atual = dict_player['atributos_variaveis']['xp']['level']
    if level_anterior < level_atual:
      mensagem_confirmacao += "\n__O player irá passar de nível__"

    await ctx.send(mensagem_confirmacao, delete_after=10)
    confirmacao = await self.client.wait_for(
      'message', check=lambda msg: msg.author == ctx.author, timeout=60)
    confirmacao = confirmacao.content.lower()

    #Canal Log
    canal_log = self.client.get_channel(873616219700334622)
    if confirmacao == 's':
      CRUD.update_item("players", dict_player)
      await ctx.send("XP atualizado com sucesso", delete_after=20)
      await canal_log.send("Foi adicionado ao player " + player.mention + " " +
                           valor + " de xp")
      if level_anterior < level_atual:
        await canal_log.send("O player " + player.mention +
                             " __passou de level__ seu lv atual é **" +
                             level_atual + "**")
        await player.send(
          "__**Parabéns você passou de nível**__ agora seu level é **" +
          level_atual + "**",
          delete_after=50)
    else:
      await ctx.send("Operação cancelada", delete_after=20)


#------------Rpg Class Fim-----------------


async def setup(client):  #Ativa o Cog
  await client.add_cog(master_table(client))


#-----------Funcoes do Cog Inicio-----------

#-----------Funcoes do Cog Fim-----------
