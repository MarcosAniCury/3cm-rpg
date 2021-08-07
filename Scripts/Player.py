#Meus arquivos .py
from discord import channel
from Armazenamento import CRUD
from Armazenamento import Embeds3cm
from Main import check_not_exist_player

#Bibliotecas python
import discord
import asyncio
import random
from discord.ext import commands

class player(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.banco = CRUD.crud()

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
    @commands.has_permissions(administrator = True)
    #@commands.check(check_not_exist_player)
    async def createplayer(self, ctx): #Criar player
        #Sortear uma classe
        classesDict = self.banco.read_chose_random_one("classes")
        classesDict.pop('_id') #remover id
        classe_sorteada = random.choice(list(classesDict)) #pegar aleatoriamente uma classe

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

        await ctx.send("Digite o nome do seu personagem:")
        nome_personagem = await self.client.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)

        habilidade_sorteada = self.banco.read_chose_random_one("skills")

        habilidades = {}

        for x in range(1,estrelas+1):
            habilidades[x] = None

        habilidades[1] = random.choice(list(habilidade_sorteada))

        await ctx.send("**SPOILER ALERT:** Nome:"+nome_personagem.content+" classe:"+classe_sorteada+" estrelas:"+str(estrelas)+" habilidade:"+habilidades[1]+" morto:False")

        player = {
            "id_player": ctx.author.id,
            "name": nome_personagem.content,
            "classe": classe_sorteada,
            "estrelas": estrelas,
            "habilidades": habilidades,
            "atributos_fixos": {
                "for": 0,
                "des": 0,
                "con": 0,
                "int": 0,
                "car": 0,
                "sor": 0
            },
            "atibutos_variaveis": {
                "mana": 20,
                "estamina": 20,
                "vida": 20,
                "evasao": 0,
                "sorte": 0,
                "pontos_atributos": 0
            },
            "pontos": {
                "morte": 0,
                "sobreviver": 0,
                "especial_evento": 0,
                "total": 0
            },

            "morto": False
        }
                    
#------------Rpg Class Fim-----------------

def setup(client): #Ativa o Cog
    client.add_cog(player(client))

#-----------Funcoes do Cog Inicio-----------


#-----------Funcoes do Cog Fim-----------