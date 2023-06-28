# Meus arquivos .py
from Armazenamento import CRUD
from Armazenamento import Embeds3cm

# Bibliotecas python
import asyncio
import random
from discord.ext import commands
from Scripts.Utils.UtilsFunctions import check_not_exist_player, check_exist_player, find_player_by_id


class player(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.banco = CRUD.crud()
    self.embeds_obj = Embeds3cm.epic_3cm(client)

  # Evento
  @commands.Cog.listener()
  async def on_ready(self):
    print("Modulo player Carregado")
    print("----------------------")

  @commands.Cog.listener()
  async def on_disconnect(self):
    print("Modulo player desconectado")
    print("---------------------")

  @commands.command()
  @commands.check(check_not_exist_player)
  async def criar_ficha(self, ctx):  # Criar player
    # Sortear uma classe
    classe_sorteada = gerar_random(self.banco, "classes")

    # Sortear estrelas
    numero_estrelas = random.uniform(1, 100)
    numero_estrelas = int(numero_estrelas)

    # Pegar estrela
    # Tabela de Porcentagem
    # 0-40 - 40%
    # 41-70 - 30%
    # 71-90 - 20%
    # 91-99 - 9%
    # 100 - 1%

    if numero_estrelas <= 40:
      estrelas = 1
    elif numero_estrelas <= 70:
      estrelas = 2
    elif numero_estrelas <= 90:
      estrelas = 3
    elif numero_estrelas <= 99:
      estrelas = 4
    else:
      estrelas = 5

    # Entrada de nome pelo player
    await ctx.send("Digite o nome do seu personagem:")
    nome_personagem = await self.client.wait_for(
      'message', check=lambda msg: msg.author == ctx.author, timeout=60)

    # sortear habilidade inicial
    habilidades = {}

    for x in range(1, estrelas + 1):
      habilidades[str(x)] = "None"

    habilidades["1"] = {
      "habilidade": gerar_random(self.banco, "skills"),
      "nivel": '1'
    }

    player = {
      "id_player": str(ctx.author.id),
      "nome": nome_personagem.content,
      "level": '0',
      "classe": classe_sorteada,
      "estrelas": str(estrelas),
      "habilidades": habilidades,
      "atributos_fixos": {
        "for": '0',
        "des": '0',
        "con": '0',
        "int": '0',
        "car": '0',
        "sor": '0'
      },
      "atributos_variaveis": {
        "mana": {
          "maxima": '20',
          "atual": '20'
        },
        "estamina": {
          "maxima": '20',
          "atual": '20'
        },
        "vida": {
          "maxima": '20',
          "atual": '20'
        },
        "xp": {
          "atual": '0',
          "maximo": '100',
          "level": '0'
        },
        "evasao": '0',
        "sorte": '0',
        "pontos_atributos": '0'
      },
      "pontos": {
        "morte": '0',
        "sobreviver": '0',
        "especial_evento": '0',
        "total": '0'
      },
      "morto": str(False)
    }

    # Armazenar no data base
    self.banco.create("players", player)

    # "Animacoes" presentes na tela
    cooldown_comandos = 4
    await ctx.send("Encolhendo jogador __**" + nome_personagem.content +
                   "**__",
                   delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)
    await ctx.send("Gerando classe...", delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)
    await ctx.send("Classe gerada:__**" + classe_sorteada + "**__",
                   delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)
    await ctx.send("Gerando número de estrelas...",
                   delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)
    await ctx.send("Número de estrelas gerada:__**" + str(estrelas) + "**__",
                   delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)
    await ctx.send("Gerando Habilidade __**Lendária**__...",
                   delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)
    await ctx.send("**FALHA ENCONTRADA**, Gerando habilidade padrão...",
                   delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)
    await ctx.send("Habilidade gerada:__**" + habilidades['1']["habilidade"] +
                   "**__",
                   delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)
    await ctx.send("Inicializando todos os atributos com valor **0**",
                   delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)
    await ctx.send(
      "**PLAYER CRIADO COM SUCESSO, SEU PROFILE IRÁ APARECER NA SUA FRENTE**",
      delete_after=cooldown_comandos)
    await asyncio.sleep(cooldown_comandos)

    player_profile = self.embeds_obj.player_profile(player)

    # Enviar para o privado
    await ctx.author.send(embed=player_profile, delete_after=60)
    # Enviar para o canal privado
    canal_log = self.client.get_channel(873616219700334622)
    await canal_log.send("Player criado\n")
    await canal_log.send(embed=player_profile)

  @commands.command(aliases=["p"])
  @commands.check(check_exist_player)
  async def perfil(self, ctx):  # Criar player
    id = ctx.author.id
    player = find_player_by_id(id, self.banco)
    embed_player = self.embeds_obj.player_profile(player)
    await ctx.send(
      "__Aparece em sua frente uma tela, acessando perfil do player__",
      delete_after=10)
    await ctx.author.send(embed=embed_player, delete_after=60)

    # Canal de log
    canal_log = self.client.get_channel(873616219700334622)
    await canal_log.send("Player acessou seu profile")
    await canal_log.send(embed=embed_player)

  @commands.command(aliases=["ds"])
  @commands.check(check_exist_player)
  async def descrição(self, ctx):
    await ctx.send(
      "Você procura a descrição de uma classe ou uma habilidade (classe/habilidade)?",
      delete_after=60)
    input_colecao = await self.client.wait_for(
      'message', check=lambda msg: msg.author == ctx.author, timeout=60)
    input_colecao = input_colecao.content.lower()

    if input_colecao == "classe" or input_colecao == "c":
      await ctx.send("Digite o nome da classe:", delete_after=60)
      input_objeto = await self.client.wait_for(
        'message', check=lambda msg: msg.author == ctx.author, timeout=60)
      input_objeto = input_objeto.content.lower().capitalize()

      input_colecao = "classes"

      dict_objeto = self.banco.read_colection(input_colecao)
      await ctx.send("**" + input_objeto + "** : " +
                     dict_objeto[input_objeto]["descricao"])

      # Canal de log
      canal_log = self.client.get_channel(873616219700334622)
      await canal_log.send("O usuário " + ctx.author.mention +
                           " pesquisou a descricao de " + input_objeto)
    elif input_colecao == "habilidade" or input_colecao == "h":
      await ctx.send("Digite o nome da habilidade:", delete_after=60)
      input_objeto = await self.client.wait_for(
        'message', check=lambda msg: msg.author == ctx.author, timeout=60)
      input_objeto = input_objeto.content.lower().capitalize()

      input_colecao = "skills"

      dict_objeto = self.banco.read_colection(input_colecao)
      await ctx.send("**" + input_objeto + "** : " +
                     dict_objeto[input_objeto]["descricao"])

      # Canal de log
      canal_log = self.client.get_channel(873616219700334622)
      await canal_log.send("O usuário " + ctx.author.mention +
                           " pesquisou a descricao de " + input_objeto)

    else:
      await ctx.send("Valor inválido, cancelando operação.")

  @commands.command(aliases=["dp"])
  @commands.check(check_exist_player)
  async def distribuir_pontos(self, ctx):
    id = ctx.author.id
    player = find_player_by_id(id, self.banco)
    pontos_distribuir = int(player['atributos_variaveis']['pontos_atributos'])
    if pontos_distribuir <= 0:
      await ctx.send("Você não possui pontos para distribuir", delete_after=20)

    # Canal de Log
    canal_log = self.client.get_channel(873616219700334622)

    while pontos_distribuir > 0:
      await ctx.send(
        "Você possui **" + str(pontos_distribuir) +
        "** pontos para distribuir, digite qual o atributo e quantos pontos você deseja colocar (Digite **não** para cancelar):\nEX:**For 5**",
        delete_after=60)
      input_pontos = await self.client.wait_for(
        'message', check=lambda msg: msg.author == ctx.author, timeout=60)
      input = input_pontos.content.lower().split()
      if input_pontos.content.lower() == 'não' or input_pontos.content.lower(
      ) == 'n':
        await ctx.send("Cancelando operação", delete_after=10)
        pontos_distribuir = 0
      elif int(input[1]) <= pontos_distribuir:
        player['atributos_fixos'][input[0]] = str(
          int(player['atributos_fixos'][input[0]]) + int(input[1]))
        player['atributos_variaveis']['pontos_atributos'] = str(
          int(player['atributos_variaveis']['pontos_atributos']) -
          int(input[1]))
        pontos_distribuir = int(
          player['atributos_variaveis']['pontos_atributos'])
        await ctx.send("__Tem certeza que você vai adicionar **" + input[1] +
                       "** pontos em **" + input[0] + "** (S/N):__",
                       delete_after=60)
        input_confirmacao = await self.client.wait_for(
          'message', check=lambda msg: msg.author == ctx.author, timeout=60)
        input_confirmacao = input_confirmacao.content.lower()
        if input_confirmacao == 's' or input_confirmacao == 'sim':
          self.banco.update_item("players", player)
          await ctx.send(
            "distribuição de pontos bem sucedida, digite `3cm perfil` para verificar",
            delete_after=30)
          await canal_log.send("O jogador " + ctx.author.mention +
                               " adicionou **" + input[1] +
                               "** pontos no atributo " + input[0])
      else:
        await ctx.send("Operação inválida, cancelando operação",
                       delete_after=10)
        pontos_distribuir = 0


# ------------Rpg Class Fim-----------------


async def setup(client):  # Ativa o Cog
  await client.add_cog(player(client))


# -----------Funcoes do Cog Inicio-----------


def gerar_random(banco, Colecao):
  item_gerado = banco.read_chose_random_one(Colecao)
  # Copy do item para atualizar
  item_atualizado = item_gerado.copy()

  item_gerado.pop('_id')
  item_aleatorio = random.choice(list(item_gerado))
  while item_gerado[item_aleatorio]['utilizado'] == "True":
    item_aleatorio = random.choice(list(item_gerado))

  # Atualizado
  item_atualizado[item_aleatorio]["utilizado"] = "True"

  banco.update_item(Colecao, item_atualizado)
  return item_aleatorio


# -----------Funcoes do Cog Fim-----------
