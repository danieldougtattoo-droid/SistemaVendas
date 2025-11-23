from datetime import datetime
from Cliente import Cliente
from produto import Produto


class Venda:

    def __init__(self, id, cliente: Cliente):
        self._id = id
        self._cliente = cliente
        self._itens = []
        self._data_venda = datetime.now()
        self._valor_total = 0.0

    @property
    def id(self):
        """ R etorna o ID  da venda """
        return self._id

    @property
    def cliente(self):
        return self._cliente

    @property
    def itens(self):
        return self._itens

    @property
    def data_venda(self):
        return self._data_venda

    @property
    def valor_total(self):
        return self._valor_total

    @property
    def quatidade_itens(self):
        return len(self._itens)

    def adicionar_item(self, produto: Produto, quantidade: int):
        """Adicionar um produto à venda """
        if produto.pode_vender(quantidade):
            valor_item = float(produto.preco) * quantidade
            self.itens.append({
                'produto': produto,
                'quantidade': quantidade,
                'preco_unitario': float(produto.preco),
                'subtotal': valor_item
            })
            produto.atualizar_estoque(-quantidade) #Diminui estoque
            self._valor_total += valor_item
        else:
            print(f"Estoque insuficiente para {produto.nome}")

    def finalizar_venda(self):
        if len(self._itens) == 0:
            print(f"Venda sem itens não pode ser finalizada")
            return False

        self._cliente.adicionar_compra(self)
        print(f"Venda finalizada! Total: R${self._valor_total:.2f}")
        return True

    def exibir_resumo(self):
        print(f"\n{'='*50}")
        print(f"RESUMO DA VENDA {self._id}")
        print(f"{'='*50}")

        for item in self._itens:
            print(f"{item['produto'].nome} x{item['quantidade']} = R${item['subtotal']:.2f}")

        print(f"{'-'*50}")
        print(f"TOTAL: R${self.valor_total:.2f}")
        print(f"{'='*50}\n")
            