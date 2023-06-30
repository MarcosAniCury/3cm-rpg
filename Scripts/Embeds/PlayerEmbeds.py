#Bibliotecas python
import discord

def player_profile(client, playerdict):  #Embed for players profile
  #adicionar habilidades
  habilidades = ""
  for x in list(playerdict["habilidades"].items()):

    if (x[1] != "None"):
      habilidade = list(x[1].values())
      habilidades += "**Habilidade " + x[0] + "**:" + habilidade[
        0]["nome"] + "(nv" + habilidade[1] + ")\n"
    else:
      habilidades += f'**Habilidade {x[0]}**: Slot Bloqueado\n'

  #adicionar pontos para distribuir
  atributos_fixos = "👊**For**:" + playerdict["atributos_fixos"]["for"] + "\n"
  atributos_fixos += "👟**Des**:" + playerdict["atributos_fixos"]["des"] + "\n"
  atributos_fixos += "💓**Con**:" + playerdict["atributos_fixos"]["con"] + "\n"

  if int(playerdict['atributos_variaveis']['pontos_atributos']) > 0:
    atributos_fixos += "\n**Pontos há distribuir**:" + playerdict[
      'atributos_variaveis']['pontos_atributos'] + "\n"

  player_profile = discord.Embed(colour=0xBF00FF)

  player_info = "**Player Info**"
  if playerdict["morto"] == "True":
    player_info += " (**MORTO**)"

  player_profile.add_field(name=player_info,
                            value="**Classe**:" + playerdict["classe"]["nome"] + "\n"
                            "**Estrelas**:" + playerdict["estrelas"] + "\n" +
                            habilidades,
                            inline=False)

  player_profile.add_field(
    name="**Status**",
    value="🔰**Level**:" + playerdict["atributos_variaveis"]['xp']['level'] +
    "\n"
    "✨**XP**:" + playerdict["atributos_variaveis"]['xp']['atual'] + "/" +
    playerdict["atributos_variaveis"]['xp']['maximo'] + "\n"
    "❤️**Vida**:" + playerdict["atributos_variaveis"]["vida"]["atual"] +
    "/" + playerdict["atributos_variaveis"]["vida"]["maxima"] + "\n"
    "☄️**Mana**:" + playerdict["atributos_variaveis"]["mana"]["atual"] +
    "/" + playerdict["atributos_variaveis"]["mana"]["maxima"] + "\n"
    "🏃**Estamina**:" +
    playerdict["atributos_variaveis"]["estamina"]["atual"] + "/" +
    playerdict["atributos_variaveis"]["estamina"]["maxima"],
    inline=False)

  player_profile.add_field(name="**Atributos**",
                            value=atributos_fixos,
                            inline=True)

  player_profile.add_field(
    name="\u200b",
    value="🧠**Int**:" + playerdict["atributos_fixos"]["int"] + "\n"
    "😜**Car**:" + playerdict["atributos_fixos"]["car"] + "\n"
    "🍀**Sor**:" + playerdict["atributos_fixos"]["sor"] + "\n",
    inline=True)

  player_foto_url = client.get_user(int(
    playerdict["id_player"])).display_avatar
  player_profile.set_footer(
    text="Develop by:Miko#9331",
    icon_url=client.get_user(239498713347653633).display_avatar)
  player_profile.set_author(name=playerdict["nome"] + " Profile",
                            icon_url=player_foto_url)
  player_profile.set_thumbnail(url=player_foto_url)

  return player_profile