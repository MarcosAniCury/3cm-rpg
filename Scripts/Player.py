#Meus arquivos .py
from discord import channel
from Armazenamento import CRUD
from Armazenamento import Embeds3cm
from Main import checkNotExistPlayer

#Bibliotecas python
import discord
import asyncio
import random
from discord.ext import commands

class Player(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.banco = CRUD.Crud()

    #Evento
    @commands.Cog.listener()
    async def on_ready(self):
        print("Modulo Player Carregado") 
        print("----------------------")

    @commands.Cog.listener()
    async def on_disconnect():
        print("Modulo Player desconectado")
        print("---------------------")

    @commands.command()
    @commands.has_permissions(administrator = True)
    #@commands.check(checkNotExistPlayer)
    async def createPlayer(self, ctx): #Criar player
        #Sortear uma classe
        classesDict = self.banco.readColection("classes")
        classesDict.pop('_id') #remover id
        classeSorteada = random.choice(list(classesDict)) #pegar aleatoriamente uma classe

        #Sortear estrelas
        numeroEstrelas = random.uniform(1,100)
        numeroEstrelas = int(numeroEstrelas)

        #Pegar estrela 
        # Tabela de Porcentagem
        # 0-40 - 40%
        # 41-70 - 30%
        # 71-90 - 20%
        # 91-99 - 9%
        # 100 - 1%

        if numeroEstrelas <= 40:
            Estrelas = 1
        elif numeroEstrelas <= 70:
            Estrelas = 2
        elif numeroEstrelas <= 90:
            Estrelas = 3
        elif numeroEstrelas <= 99:
            Estrelas = 4
        else:
            Estrelas = 5

        await ctx.send("Digite o nome do seu personagem:")
        nomePersonagem = await self.client.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=60)

        Player = {
            "idPlayer": ctx.author.id,
            "name": nomePersonagem.content,
            "classe": classeSorteada,
            "estrelas": Estrelas,
            "atributosFixos": {
                "for": 0,
                "des": 0,
                "con": 0,
                "int": 0,
                "car": 0,
                "sor": 0
            },
            "atibutosVariaveis": {
                "mana": 20,
                "estamina": 20,
                "vida": 20,
                "evasao": 0,
                "sorte": 0,
                "pontosAtributos": 0
            },
            "pontos": {
                "total": 0
            },

            "morto": False
        }
                    
#------------Rpg Class Fim-----------------

def setup(client): #Ativa o Cog
    client.add_cog(Player(client))

#-----------Funcoes do Cog Inicio-----------


#-----------Funcoes do Cog Fim-----------