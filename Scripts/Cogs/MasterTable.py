# Meus arquivos .py
import discord
# Bibliotecas python
from discord.ext import commands

from Scripts.Database.CRUD import CRUD
from Scripts.Utils.UtilsFunctions import (add_XP, find_player_by_id,
                                          update_pontos, update_status)


class master_table(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Evento
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

        # Canal de log
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

        # Canal de log
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

    @commands.command()
    @commands.is_owner()
    async def add_skill(self, ctx):
        skill = {
            "utilizado": "False",
            "descrição_nivel": {},
            "consumo": {}
        }

        message_name = "Digite o nome da habilidade"
        await ctx.send(message_name, delete_after=10)
        name = await self.client.wait_for(
            'message', check=lambda msg: msg.author == ctx.author, timeout=60)
        skill["nome"] = name.content.lower().capitalize()
        
        message_description = "Digite a descrição da habilidade (Para o Player)"
        await ctx.send(message_description, delete_after=10)
        description = await self.client.wait_for(
            'message', check=lambda msg: msg.author == ctx.author, timeout=60)
        skill["descricao"] = description.content.lower()
        
        message_level_description = "Digite a descrição para o level 1"
        await ctx.send(message_level_description, delete_after=10)
        level_description = await self.client.wait_for(
            'message', check=lambda msg: msg.author == ctx.author, timeout=60)
        skill["descrição_nivel"]['nv1'] = level_description.content.lower()
        
        message_duration_turn = "Digite o tempo de duração para a habilidade (Turno)"
        await ctx.send(message_duration_turn, delete_after=10)
        duration_turn = await self.client.wait_for(
            'message', check=lambda msg: msg.author == ctx.author, timeout=60)
        skill['consumo']["duração"] = int(duration_turn.content)
        
        message_recharge_time = "Tempo de recarga da habilidade (Turno)"
        await ctx.send(message_recharge_time, delete_after=10)
        recharge_time = await self.client.wait_for(
            'message', check=lambda msg: msg.author == ctx.author, timeout=60)
        skill['consumo']["recarga"] = int(recharge_time.content)
        
        status_affect = None
        options_status_affect = [
            'mana',
            'vida',
            'estamina'
        ]

        while status_affect not in options_status_affect:
            message_status_affect = "Qual status a habilidade irá influenciar?"
            await ctx.send(message_status_affect, delete_after=10)
            status_affect_response = await self.client.wait_for(
                'message', check=lambda msg: msg.author == ctx.author, timeout=60)
            status_affect = status_affect_response.content.lower()
        
        message_status = "Quanto irá reduzir da "+status_affect+"?"
        await ctx.send(message_status, delete_after=10)
        status = await self.client.wait_for(
            'message', check=lambda msg: msg.author == ctx.author, timeout=60)
        skill['consumo'][status_affect] = int(status.content)
        

        message_confirmation = f"Deseja realmente criar uma habilidade {skill['nome']}\n" \
            f"*Descrição:* {skill['descricao']}\n" \
            f"*Descrição Level 1:* {skill['descrição_nivel']['nv1']}\n" \
            f"Duração de {skill['consumo']['duração']} e custo de {skill['consumo'][status_affect]} {status_affect} (s/n)?"

        
        await ctx.send(message_confirmation, delete_after=120)
        confirmation_response = await self.client.wait_for(
            'message', check=lambda msg: msg.author == ctx.author, timeout=60)
        confirmation = confirmation_response.content.lower()

        # Canal Log
        canal_log = self.client.get_channel(873616219700334622)
        if confirmation == 's':
            CRUD.create("skills", skill)
            await ctx.send("Skill criada com sucesso", delete_after=20)
            await canal_log.send(f"O player {ctx.author.mention} criou a skill {skill['nome']}")
        else:
            await ctx.send("Operação cancelada", delete_after=20)

    @commands.command(aliases=["ax"])
    @commands.is_owner()
    async def add_xp(self, ctx, player: discord.Member, valor):
        dict_player = find_player_by_id(player.id)
        level_anterior = dict_player['atributos_variaveis']['xp']['level']

        add_XP(dict_player.copy(), int(valor))

        # Confirmação
        mensagem_confirmacao = "Tem certeza que irá adicionar " + \
            valor + " de XP para o usuário " + player.name + "(S/N):"

        level_atual = dict_player['atributos_variaveis']['xp']['level']
        if level_anterior < level_atual:
            mensagem_confirmacao += "\n__O player irá passar de nível__"

        await ctx.send(mensagem_confirmacao, delete_after=10)
        confirmacao = await self.client.wait_for(
            'message', check=lambda msg: msg.author == ctx.author, timeout=60)
        confirmacao = confirmacao.content.lower()

        # Canal Log
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


# ------------Rpg Class Fim-----------------


async def setup(client):  # Ativa o Cog
    await client.add_cog(master_table(client))


# -----------Funcoes do Cog Inicio-----------

# -----------Funcoes do Cog Fim-----------
