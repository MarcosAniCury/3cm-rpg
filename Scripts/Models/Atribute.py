class Atribute:

    def __init__(self, id, str, dex, con, int, cha, luc):
        self.id = id
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.cha = cha
        self.luc = luc

    def get_insert_values(self):
        return "\'" + self.str + "\',\'" + self.dex + "\',\'" + self.con + "\',\'" + self.int + \
               "\',\'" + self.cha + "\',\'" + self.luc + "\'"
