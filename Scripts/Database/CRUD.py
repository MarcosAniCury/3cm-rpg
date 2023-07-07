# Meus arquivos .py
# Bibliotecas python
from pymongo import MongoClient

from Scripts import TOKENs


class CRUD:
    DB = None
    data_base = None

    # Construtor
    def __init__(self):
        raise NotImplementedError(
            "A criação de objetos desta classe é proibida.")

    def connect():
        CRUD.DB = MongoClient(TOKENs.get_tokenDB())
        CRUD.data_base = CRUD.DB.cm3
        print("Conexão com o MongoDB realizada")
        print("------------------------------")

    def disconnect():
        CRUD.DB.close()
        CRUD.data_base = None
        print("Conexão com o banco de dados encerrada")
        print("------------------------------")

    # --------Colection Servidores Inicio--------

    # --------------crud Inicio--------------

    def create(colecao, item):  # Criar um documento
        CRUD.data_base[colecao].insert_one(item)
        return True

    def read(Colecao, item):  # Ler um documento
        return CRUD.data_base[Colecao].find_one(item)

    def read_colection(Colecao):
        return CRUD.data_base.find_one()

    def read_specific_item(colecao, item):
        return CRUD.data_base[colecao].find_one(item)

    def read_chose_random_one(Colecao):  # Ler a coleção inteira
        return CRUD.data_base[Colecao].aggregate([{"$sample": {"size": 1}}]).next()

    def update_item(Colecao, itemNew):
        Obj = CRUD.read(Colecao, itemNew['_id'])
        return CRUD.data_base[Colecao].update_one(Obj, {'$set': itemNew})

    # def delete_Servidores(self, Server_id):
    #   conseguiu = False
    #   if (self.read_ServidoresById(Server_id) != None):
    #     self.Servidores.delete_one({"Server_id": Server_id})
    #     conseguiu = True
    #   return conseguiu

# ---------------crud Fim------------------

# def ServidoresCheck(
#     self, Arr,
#     key):  #Checar para alterar um dos valores presentes na Coleção
#   Server = dict(Arr)
#   Obj = self.read_ServidoresById(Server["Server_id"])
#   conseguiu = False
#   if (Obj != None):  #Existe logo irei fazer um update
#     if key != "None":  #Verifica se altera um key expecifica
#       Obj[key] = Server[key]
#     else:
#       Obj = Server
#     self.update_Servidores(Obj)
#     conseguiu = True
#   else:
#     self.create_Servidores(Server)

    def check_player(id):
        players = CRUD.data_base['players']
        retorno = False
        if (players.find_one({"id_player": str(id)}) != None):
            retorno = True
        return retorno


# ----------Colection Servidores Fim----------
