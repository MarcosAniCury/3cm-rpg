#Meus arquivos .py
from discord import channel
from Armazenamento import CRUD

#Bibliotecas python
import random
from discord.ext import commands

class dice(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.banco = CRUD.crud()

    #Evento
    @commands.Cog.listener()
    async def on_ready(self):
        print("Modulo dice Carregado") 
        print("----------------------")

    @commands.Cog.listener()
    async def on_disconnect():
        print("Modulo dice desconectado")
        print("---------------------")

    @commands.Cog.listener()
    async def on_message(self,message):

        #Variaveis importantes
        guild = message.guild
        member = guild.get_member(message.author.id)
        channel = guild.get_channel(872118823610904596)

        if message.author.id != self.client.user.id:
            if message.content.lower().startswith("rd"):
                mensagem = message.content.split()
                number = eval(mensagem[0][2:])#Pega os numeros apos o 'rd'

                if len(mensagem) == 1: #ve quantos loops tem que dar
                    loops = 1
                else:
                    loops = int(mensagem[1])
                    if loops > 20: #para ninguem usar mais de 20 dados
                        loops = 20
                        await message.channel.send("**NÃO PODE MAIS DE 20 OTÁRIO**")

                #apenas para randomizar
                randomizar = []
                for x in range(20):
                    randomizar.append(random.randint(0,999))

                for x in range(loops):
                    #randomizar
                    result = random.randint(1, number)
                    random.seed(random.randint(random.choice(randomizar),999))

                    returnFunc = None 
                    if result == number:
                        returnFunc = "**"+str(result)+"** <- d"+str(number)+" **CRITÍCO, `dano pra carai`**"
                    elif result == 1:
                        returnFunc = "**"+str(result)+"** <- d"+str(number)+" **FALHA CRÍTICA**, `se fudeu`"
                    else:
                        returnFunc = "`"+str(result)+"` <- d"+str(number)

                    if member.id != 239498713347653633 :
                        returnFunc += " --- player:`"+member.display_name+"`"
                    else:
                        returnFunc += " --- `Inimigo`"
                    await message.channel.send(returnFunc)
                    
#------------Rpg Class Fim-----------------

def setup(client): #Ativa o Cog
    client.add_cog(dice(client))

#-----------Funcoes do Cog Inicio-----------


#-----------Funcoes do Cog Fim-----------