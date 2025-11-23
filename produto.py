class Produto:

    def __init__(self, id, nome, preco, estoque, categoria=""):
        self._id = id
        self._nome = nome
        self._preco =  float(preco)
        self._estoque = estoque
        self._categoria = categoria

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, novo_preco):
        """ Define um novo preço com validação """
        if novo_preco > 0:
            self._preco = novo_preco
        else:
            print("x Preço não pode ser zero ou negativo")

    @property
    def estoque(self):
        return self._estoque

    @property
    def categoria(self):
        return self._categoria


    def atualizar_estoque(self, quantidade):
        self._estoque += quantidade

    def pode_vender(self, quantidade):
        """Verifica se há estoque suficiente"""
        return self._estoque >= quantidade

    def __str__(self):
        return f"Produto: {self._nome} | Preço: R${self._preco:.2f} | Estoque: {self._estoque}"
        