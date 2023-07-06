# -----------Funcoes do Server Inicio-----------

from Scripts.Database.CRUD import CRUD


async def check_not_exist_player(ctx):
  id = ctx.author.id
  retorno = not CRUD.check_player(id)
  if not retorno:
    await ctx.send("Você já possui uma ficha de personagem")
  return retorno


async def check_exist_player(ctx):
  id = ctx.author.id
  retorno = CRUD.check_player(id)
  if not retorno:
    await ctx.send("Você não possui uma ficha de personagem")
  return retorno


def find_player_by_id(memberId):
  player = CRUD.read("players", {'id_player': str(memberId)})
  return player


def update_status(dict_player, status, valor):  # Cria uma nova Referencia
  retorno = None
  valorMaximo = dict_player['atributos_variaveis'][status]['maxima']
  valorAnterior = dict_player['atributos_variaveis'][status]['atual']
  dict_player['atributos_variaveis'][status]['atual'] = str(
    int(valor) + int(valorAnterior))
  valorAtual = dict_player['atributos_variaveis'][status]['atual']
  # Caso ultrapasse de zero
  if int(valorAnterior) + int(valor) <= 0 and status == "vida":
    valorAtual = "0"
    dict_player["morto"] = "True"
  if int(valorAtual) <= int(
      valorMaximo) and int(valorAnterior) + int(valor) >= 0:
    retorno = [dict_player, valorAtual, valorMaximo]
  return retorno


def update_pontos(dict_player, valor):
  if valor + dict_player['pontos_de_conquista'] >= 0:
    dict_player['pontos_de_conquista'] += valor
    return dict_player
  # Caso os pontos fiquem menor que 0
  return None


def add_XP(dict_player, amount_xp):  # Altera a Referencia

  xp_atual = int(dict_player['atributos_variaveis']['xp']['atual'])
  dict_player['atributos_variaveis']['xp']['atual'] = str(amount_xp + xp_atual)
  xp_atual = amount_xp + xp_atual
  xp_maximo = int(dict_player['atributos_variaveis']['xp']['maximo'])
  if xp_atual >= xp_maximo:
    dict_player['atributos_variaveis']['xp']['atual'] = str(xp_atual -
                                                            xp_maximo)
    dict_player['atributos_variaveis']['xp']['maximo'] = str(xp_maximo + 100)
    level_atual = int(dict_player['atributos_variaveis']['xp']['level']) + 1
    dict_player['atributos_variaveis']['xp']['level'] = str(level_atual)
    dict_player['atributos_variaveis']['pontos_atributos'] = int(dict_player['atributos_variaveis']['pontos_atributos']) + 2
