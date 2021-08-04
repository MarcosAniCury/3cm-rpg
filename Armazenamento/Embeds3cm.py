#Meus arquivos .py
from discord.colour import Color
from Armazenamento import TOKENs

#Bibliotecas python
import discord
from discord import client
from discord.ext.commands.help import HelpCommand

class Epic3cm:
    
    #Construtores
    def __init__(self, client):
        self.client = client
        self.prefix = TOKENs.get_prefix()
        if type(self.prefix) is list:
            self.prefix = self.prefix[0]

    def get_HelpCommand(self):#Embed Command help

        HelpCommand = discord.Embed(
            title = "Comandos",
            description = "Bot feito para o Rpg 3CM\n\u200b",
            colour = 0xBF00FF,
        )

        HelpCommand.add_field(
            name="📄Server Comandos📄", 
            value ="`"+self.prefix+"ping` - para testar a latência\n"
            "`"+self.prefix+"helpadm || hadm` - comando help para adms **Apenas ADMs**\n"
            "`"+self.prefix+"credits` - créditos e agradecimentos\n\u200b",
            inline = False
        )

        HelpCommand.add_field(
            name="🏹RPG de Mesa Comandos⚔️",
            value = "`rd<numero de lados> <quantidades de vezes>` - Rodar um dado de n lados m vezes\n"
            "\nBot em construção, mais comandos serão adicionados no futuro",
            inline = False
        )

        HelpCommand.set_footer(text="Develop by:Miko#9331", icon_url=f'{self.client.get_user(239498713347653633).avatar_url}')
        HelpCommand.set_author(name="3cm Rpg", icon_url=f'{self.client.get_user(869952210979663883).avatar_url}')

        return HelpCommand

    def get_HelpAdmCommand(self): #Emd Commnad helpadm
        
        HelpAdmCommand = discord.Embed(
            title = "Comandos Adms",
            description = "Bot feito para ajudar os jogadores do rpg epic\n\u200b",
            colour = 0xBF00FF, #laranja
        )

        HelpAdmCommand.add_field(
            name="📄Server Comandos📄", 
            value = "`"+self.prefix+"ativar_modulo <modulo>` - ativar um modulo do bot\n"
            "`"+self.prefix+"desativar_modulo <modulo>` - desativar um modulo do bot\n"
            "`"+self.prefix+"reiniciar_modulo <modulo>` - reiniciar um modulo do bot\n\u200b",
        )

        HelpAdmCommand.set_footer(text="Develop by:Miko#9331", icon_url=f'{self.client.get_user(239498713347653633).avatar_url}')
        HelpAdmCommand.set_author(name="3cm Rpg", icon_url=f'{self.client.get_user(869952210979663883).avatar_url}')

        return HelpAdmCommand