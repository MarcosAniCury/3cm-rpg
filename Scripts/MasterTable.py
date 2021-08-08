#Meus arquivos .py
from discord import channel
from Armazenamento import CRUD
from Armazenamento import Embeds3cm
from Main import find_player_by_id
from Main import update_status

#Bibliotecas python
from discord.ext import commands
import discord

class master_table(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.banco = CRUD.crud()
        self.embeds_obj = Embeds3cm.epic_3cm(client)

    #Evento
    @commands.Cog.listener()
    async def on_ready(self):
        print("Modulo master_table Carregado") 
        print("----------------------")

    @commands.Cog.listener()
    async def on_disconnect():
        print("Modulo master_table desconectado")
        print("---------------------")

    @commands.command(aliases=["su"])
    @commands.is_owner()
    async def statusUpdate(self, ctx, player : discord.Member, status, valor):
        status = status.lower()
        dict_player = find_player_by_id(ctx,self.banco,player.id)
        dict_player_update = await update_status(dict_player,status,valor)

        #Canal de log
        canal_log = self.client.get_channel(873616219700334622)
        if dict_player_update == None:
            await ctx.send("Operação inválida, o player não pode ultrapassar o valor maximo/minimo de status ", delete_after=60)
            await canal_log.send("Ouve uma tentativa invalida de alteração nos status do jogador **"+player.name+"**")
        else:
            self.banco.update_item("players", dict_player_update[0])
            status_string = status+" do jogador **"+player.name+"** atualizado:__**"+dict_player_update[1]+"/"+dict_player_update[2]+"**__"
            await ctx.send(status_string)
            await canal_log.send(status_string)

                    
#------------Rpg Class Fim-----------------

def setup(client): #Ativa o Cog
    client.add_cog(master_table(client))

#-----------Funcoes do Cog Inicio-----------

#-----------Funcoes do Cog Fim-----------