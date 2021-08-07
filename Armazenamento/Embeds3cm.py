#Meus arquivos .py
from discord.colour import Color
from Armazenamento import TOKENs

#Bibliotecas python
import discord
from discord import client
from discord.ext.commands.help import HelpCommand

class epic_3cm:
    
    #Construtores
    def __init__(self, client):
        self.client = client
        self.prefix = TOKENs.get_prefix()
        if type(self.prefix) is list:
            self.prefix = self.prefix[0]

    def get_embed_help_commands(self):#Embed Command help

        embed_help_commands = discord.Embed(
            title = "Comandos",
            description = "Bot feito para o Rpg 3CM\n\u200b",
            colour = 0xBF00FF,
        )

        embed_help_commands.add_field(
            name="📄Server Comandos📄", 
            value ="`"+self.prefix+"ping` - para testar a latência\n"
            "`"+self.prefix+"helpadm || hadm` - comando help para adms **Apenas ADMs**\n\u200b",
            inline = False
        )

        embed_help_commands.add_field(
            name="🏹RPG de Mesa Comandos⚔️",
            value = "`rd<numero de lados> <quantidades de vezes>` - Rodar um dado de n lados m vezes\n"
            "\nBot em construção, mais comandos serão adicionados no futuro",
            inline = False
        )

        embed_help_commands.set_footer(text="Develop by:Miko#9331", icon_url=f'{self.client.get_user(239498713347653633).avatar_url}')
        embed_help_commands.set_author(name="3cm Rpg", icon_url=f'{self.client.get_user(869952210979663883).avatar_url}')

        return embed_help_commands

    def get_help_adm_command(self): #Emd Commnad helpadm
        
        help_adm_command = discord.Embed(
            title = "Comandos Adms",
            description = "Bot feito para ajudar os jogadores do rpg epic\n\u200b",
            colour = 0xBF00FF, #laranja
        )

        help_adm_command.add_field(
            name="📄Server Comandos📄", 
            value = "`"+self.prefix+"ativar_modulo <modulo>` - ativar um modulo do bot\n"
            "`"+self.prefix+"desativar_modulo <modulo>` - desativar um modulo do bot\n"
            "`"+self.prefix+"reiniciar_modulo <modulo>` - reiniciar um modulo do bot\n\u200b",
        )

        help_adm_command.set_footer(text="Develop by:Miko#9331", icon_url=f'{self.client.get_user(239498713347653633).avatar_url}')
        help_adm_command.set_author(name="3cm Rpg", icon_url=f'{self.client.get_user(869952210979663883).avatar_url}')

        return help_adm_command

    def player_profile(self,playerdict):#Embed for players profile

        habilidades = ""
        habilidades_values = list(playerdict["habilidades"].values())
        for x in playerdict["habilidades"].keys():
            if habilidades_values[x-1] == None:
                habilidades += f'**Habilidade {str(x)}**: Slot Bloqueado'
            else:
                habilidades += f'**Habilidade {str(x)}**:{habilidades_values[x-1]["habilidade"]}(nv{habilidades_values[x-1]["nivel"]})\n'

        player_profile = discord.Embed(
            colour = 0xBF00FF
        )

        player_info = "**Player Info**"
        if playerdict["morto"]:
            player_info += " (**MORTO**)"

        player_profile.add_field(
            name=player_info, 
            value ="**Classe**:"+playerdict["classe"]+"\n"
            "**Estrelas**:"+str(playerdict["estrelas"])+"\n"+habilidades,
            inline = False
        )

        player_profile.add_field(
            name="**Status**",
            value = "❤️**Vida**:"+str(playerdict["atributos_variaveis"]["vida"]["atual"])+"/"+str(playerdict["atributos_variaveis"]["vida"]["maxima"])+"\n"
            "☄️**Mana**:"+str(playerdict["atributos_variaveis"]["mana"]["atual"])+"/"+str(playerdict["atributos_variaveis"]["mana"]["maxima"])+"\n"
            "🏃**Estamina**:"+str(playerdict["atributos_variaveis"]["estamina"]["atual"])+"/"+str(playerdict["atributos_variaveis"]["estamina"]["maxima"]),
            inline = False
        )

        player_profile.add_field(
            name="**Atributos**",
            value = "👊**For**:"+str(playerdict["atributos_fixos"]["for"])+"\n"
            "👟**Des**:"+str(playerdict["atributos_fixos"]["des"])+"\n"
            "💓**Con**:"+str(playerdict["atributos_fixos"]["con"])+"\n",
            inline = True
        )

        player_profile.add_field(
            name="\u200b",
            value = "🧙‍♂️**Int**:"+str(playerdict["atributos_fixos"]["int"])+"\n"
            "😜**Car**:"+str(playerdict["atributos_fixos"]["car"])+"\n"
            "🍀**Sor**:"+str(playerdict["atributos_fixos"]["sor"])+"\n",
            inline = True
        )

        player_foto_url = self.client.get_user(playerdict["id_player"]).avatar_url
        player_profile.set_footer(text="Develop by:Miko#9331", icon_url=self.client.get_user(239498713347653633).avatar_url)
        player_profile.set_author(name=playerdict["nome"]+" Profile", icon_url= player_foto_url)
        player_profile.set_thumbnail(url= player_foto_url)

        return player_profile