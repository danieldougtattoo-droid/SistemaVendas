class Cliente:

    def __init__(self, id, nome, email, telefone=""):
        self._id = id
        self._nome = nome
        self._email = email
        self._telefone = telefone
        self._compras = []

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email

    @property
    def telefone(self):
        return self._telefone

    @property
    def compras(self):
        return self._compras

    @property
    def total_gasto(self):
        """Calcula o total gasto pelo cliente """
        return sum(venda.valor_total for venda in self._compras)

    @property
    def quantidade_compras(self):
        """ Retorna a quantidade de compras realizadas"""
        return len(self._compras)

    def adicionar_compra(self, venda):
        """Adicionar uma compra ao histórico do cliente"""
        self._compras.append(venda)

    def __str__(self):
        return f"Cliente: {self._nome} | Email: {self._email} | Total gasto: R${self.total_gasto:.2f} | Compras: {self.quantidade_compras}"
