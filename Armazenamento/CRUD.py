#Meus arquivos .py
from Armazenamento import TOKENs

#Bibliotecas python
import pyodbc

class crud:

    #Construtor
    def __init__(self):
        DB = pyodbc.connect('DRIVER= '+ TOKENs.get_driver_azure() + '; SERVER=tcp:'+TOKENs.get_server_azure()+';PORT=1433;DATABASE='+TOKENs.get_database_name_azure()+';UID='+TOKENs.get_user_name_azure()+';PWD='+ TOKENs.get_password_name_azure())        
        self.banco = DB.cursor()
        print("Conexão com a Azure realizada")
        print("------------------------------")
        self.banco.execute("INSERT INTO modify (type_target, target, type_modify, value) VALUES ('teste','target_teste','cansei','testei dnv')")

    #--------Colection Servidores Inicio--------

    #--------------crud Inicio--------------

    def create(self,Colecao,item): #Criar um documento
        self.banco[Colecao].insert_one(item)
        return True

    def read(self,Colecao,item): #Ler um documento
        return self.banco[Colecao].find_one(item)

    def read_colection(self,Colecao):
        return self.banco[Colecao].find_one()

    def read_chose_random_one(self,Colecao): #Ler a coleção inteira
        return self.banco[Colecao].find_one()

    def update_item(self,Colecao,itemNew):
        Obj = self.read(Colecao,itemNew['_id'])
        return self.banco[Colecao].update_one(Obj,{'$set': itemNew})

    def delete_Servidores(self,Server_id):
        conseguiu = False
        if (self.read_ServidoresById(Server_id) != None):
            self.Servidores.delete_one({"Server_id": Server_id})
            conseguiu = True
        return conseguiu

    #---------------crud Fim------------------

    def ServidoresCheck(self,Arr,key): #Checar para alterar um dos valores presentes na Coleção
        Server = dict(Arr)
        Obj = self.read_ServidoresById(Server["Server_id"]) 
        conseguiu = False
        if (Obj != None): #Existe logo irei fazer um update
            if key != "None": #Verifica se altera um key expecifica
                Obj[key] = Server[key]
            else:    
                Obj = Server
            self.update_Servidores(Obj)
            conseguiu = True
        else:
            self.create_Servidores(Server)

    def check_player(self,id):
        players = self.banco['players']
        retorno = False
        if(players.find_one({"id_player":str(id)}) != None):
            retorno = True
        return retorno

    #----------Colection Servidores Fim----------
    