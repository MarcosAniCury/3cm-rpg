#Meus arquivos .py
from discord import channel
from Armazenamento import CRUD
from Armazenamento import Embeds3cm
from Main import check_not_exist_player
from Main import check_exist_player

#Bibliotecas python
import discord
import asyncio
import random
from discord.ext import commands

class player(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.banco = CRUD.crud()
        self.embeds_obj = Embeds3cm.epic_3cm(client)

    #Evento
    @commands.Cog.listener()
    async def on_ready(self):
        print("Modulo player Carregado") 
        print("----------------------")

    @commands.Cog.listener()
    async def on_disconnect():
        print("Modulo player desconectado")
        print("---------------------")

    @commands.command()
    @commands.check(check_not_exist_player)
    async def createPlayer(self, ctx): #Criar player
        #Sortear uma classe
        classe_sorteada = gerar_random(self.banco,"classes")

        #Sortear estrelas
        numero_estrelas = random.uniform(1,100)
        numero_estrelas = int(numero_estrelas)

        #Pegar estrela 
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

        #Entrada de nome pelo player 
        await ctx.send("Digite o nome do seu personagem:")
        nome_personagem = await self.client.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)

        #sortear habilidade inicial
        habilidades = {}

        for x in range(1,estrelas+1):
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
                    "maxima":'20',
                    "atual":'20'
                },
                "estamina": {
                    "maxima":'20',
                    "atual":'20'
                },
                "vida": {
                    "maxima": '20',
                    "atual":'20'
                },
                "xp": '0',
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

        #Armazenar no data base
        self.banco.create("players", player)

        #"Animacoes" presentes na tela
        cooldown_comandos = 4
        await ctx.send("Encolhendo jogador __**"+nome_personagem.content+"**__", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)
        await ctx.send("Gerando classe...", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)
        await ctx.send("Classe gerada:__**"+classe_sorteada+"**__", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)
        await ctx.send("Gerando número de estrelas...", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)
        await ctx.send("Número de estrelas gerada:__**"+str(estrelas)+"**__", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)
        await ctx.send("Gerando Habilidade __**Lendária**__...", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)
        await ctx.send("**FALHA ENCONTRADA**, Gerando habilidade padrão...", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)
        await ctx.send("Habilidade gerada:__**"+habilidades['1']["habilidade"]+"**__", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)
        await ctx.send("Inicializando todos os atributos com valor **0**", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)
        await ctx.send("**PLAYER CRIADO COM SUCESSO, SEU PROFILE IRÁ APARECER NA SUA FRENTE**", delete_after=cooldown_comandos)
        await asyncio.sleep(cooldown_comandos)

        player_profile = self.embeds_obj.player_profile(player)

        #Enviar para o privado
        await ctx.author.send(embed=player_profile, delete_after=60)
        #Enviar para o canal privado
        canal_privado = self.client.get_channel(873616219700334622)
        await canal_privado.send("Player criado\n")
        await canal_privado.send(embed=player_profile)

    @commands.command(aliases=["p"])
    @commands.check(check_exist_player)
    async def perfil(self, ctx): #Criar player
        id = ctx.author.id
        player = self.banco.read("players", {'id_player' : str(id)})
        embed_player = self.embeds_obj.player_profile(player)
        await ctx.send("__Aparece em sua frente uma tela com o login__",delete_after=10)
        await ctx.author.send(embed=embed_player, delete_after=60)

        #Canal de log
        canal_privado = self.client.get_channel(873616219700334622)
        await canal_privado.send("Player acessou seu profile")
        await canal_privado.send(embed=embed_player)

    @commands.command(aliases=["ds"])
    @commands.check(check_exist_player)
    async def descrição(self, ctx, Colecao, objeto):
        objeto = objeto.capitalize()
        objeto = objeto.replace('_', ' ')
        dictObjeto = self.banco.read_colection(Colecao)
        await ctx.send("**"+objeto+"** : "+dictObjeto[objeto]["descricao"])

        #Canal de log
        canal_privado = self.client.get_channel(873616219700334622)
        await canal_privado.send("O usuário "+ctx.author.mention+" pesquisou a descricao de "+objeto)
                    
#------------Rpg Class Fim-----------------

def setup(client): #Ativa o Cog
    client.add_cog(player(client))

#-----------Funcoes do Cog Inicio-----------

def gerar_random(banco,Colecao):
    item_gerado = banco.read_chose_random_one(Colecao)
    #Copy do item para atualizar
    item_atualizado = item_gerado.copy()

    item_gerado.pop('_id')
    item_aleatorio = random.choice(list(item_gerado))
    while item_gerado[item_aleatorio]['utilizado'] == "True":
        item_aleatorio = random.choice(list(item_gerado))

    #Atualizado
    item_atualizado[item_aleatorio]["utilizado"] = "True"

    banco.update_item(Colecao,item_atualizado)
    return item_aleatorio

#-----------Funcoes do Cog Fim-----------