from model.odi import Odi

class OdiSE(Odi):
    def __init__(self, nome, num, cc, loc, tipo, ti, cm1, cm3, setores,faseamento):
        super().__init__(nome, num, cc, loc, tipo, ti)
        self.cm1 = cm1
        self.cm3 = cm3
        self.setores = setores
        self.faseamento = faseamento
    
    # extrair de dentro do objeto odi os setores e colocar em um obj list    
    def getSetores(self):
        setores = list()
        if "-" in str(self.setores):
            for setor in self.setores.split("-"):
                setores.append(int(setor))
        else:
            setores.append(int(self.setores))
        return setores