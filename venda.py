from datetime import datetime
from math import e
from Cliente import Cliente
from produto import Produto
from typing import List

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

    def salvar_no_banco(self, db):
        """Salva a venda no banco de dados SQL Server """
        try:
            # Verificar estrutura da tabela ItensVendas (debug)
            if len(self._itens) > 0:
                colunas = db.listar_colunas_tabela('ItensVendas')
                if colunas:
                    print(f"\n📋 Colunas da tabela ItensVendas: {[c[0] for c in colunas]}")
                else:
                    print("⚠️  Não foi possível listar as colunas da tabela ItensVendas")
            
            query_venda = """ 
            INSERT INTO [Vendas] (cliente_id, data_venda, valor_total)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?)
            """
            # Executar query sem commit automático para poder fazer fetchone()
            try:
                cursor = db._conexao.cursor()
                cursor.execute(query_venda, (self._cliente.id, self._data_venda, self._valor_total))
                venda_id = cursor.fetchone()[0]
                db._conexao.commit()
                cursor.close()
                print(f"✓ Venda #{venda_id} criada. Salvando {len(self._itens)} item(ns)...")
            except Exception as e:
                db._conexao.rollback()
                raise e

            itens_salvos = 0
            total_registros = 0
            for item in self._itens:
                # Inserir um registro para cada unidade do produto
                quantidade = item['quantidade']
                registros_item = 0
                for _ in range(quantidade):
                        query_item = """
                        INSERT INTO [ItensVendas] (venda_id, produto_id, preco_unitario)
                        VALUES (?, ?, ?)
                         """
                        try:
                            cursor_item = db.executar_query(query_item, (
                                venda_id,
                                item['produto'].id,
                                item['preco_unitario']
                            ))
                            if cursor_item:
                                registros_item += 1
                                total_registros += 1
                            else:
                                print(f"  ✗ Erro ao salvar unidade do item: {item['produto'].nome}")
                                print(f"     venda_id={venda_id}, produto_id={item['produto'].id}, preco={item['preco_unitario']}")
                        except Exception as e:
                            print(f"  ✗ Erro ao salvar unidade: {e}")
                            print(f"     venda_id={venda_id}, produto_id={item['produto'].id}, preco={item['preco_unitario']}")
                
                if registros_item == quantidade:
                    print(f"  ✓ Item salvo: {item['produto'].nome} x{quantidade} ({registros_item} registros)")
                    itens_salvos += 1
                else:
                    print(f"  ⚠️  Item parcialmente salvo: {item['produto'].nome} - {registros_item}/{quantidade} registros")
            
            if itens_salvos == len(self._itens):
                print(f"✓ Todos os {len(self._itens)} itens foram salvos com sucesso! ({total_registros} registros no total)")
            else:
                print(f"⚠️  Aviso: Apenas {itens_salvos} de {len(self._itens)} itens foram salvos completamente!")
            
            # Atualizar estoque dos produtos no banco
            estoques_atualizados = 0
            for item in self._itens:
                query_estoque = """
                UPDATE [Produtos]
                SET estoque = estoque - ?
                WHERE id = ?
                 """
                cursor_estoque = db.executar_query(query_estoque,(item['quantidade'],item['produto'].id))
                if cursor_estoque:
                    estoques_atualizados += 1
                else:
                    print(f"  ⚠️  Erro ao atualizar estoque do produto: {item['produto'].nome}")
            
            if estoques_atualizados == len(self._itens):
                print(f"✓ Estoque atualizado para todos os {len(self._itens)} produtos")
            
            print(f"✓ Venda #{venda_id} salva no banco de dados!")
            return True
        
        except Exception as e:
            print(f"\n❌ Erro ao salvar venda no banco de dados:")
            print(f"   Tipo: {type(e).__name__}")
            print(f"   Mensagem: {e}")
            import traceback
            print(f"\n   Detalhes técnicos:")
            traceback.print_exc()
            return False

    def finalizar_venda(self, db=None):
        if len(self._itens) == 0:
            print(f"Venda sem itens não pode ser finalizada")
            return False

        self._cliente.adicionar_compra(self)
        
        if db:
            sucesso = self.salvar_no_banco(db)
            if not sucesso:
                print(f"⚠️  Venda finalizada localmente, mas houve erro ao salvar no banco de dados!")
                print(f"Venda finalizada! Total: R${self._valor_total:.2f}")
                return False
        
        print(f"Venda finalizada! Total: R${self._valor_total:.2f}")
        return True

    def exibir_resumo(self):
        print(f"\n{'='*50}")
        print(f"RESUMO DA VENDA {self._id}")
        print(f"{'='*50}")
        print(f"Cliente: {self._cliente.nome}")
        print(f"Data: {self._data_venda.strftime('%d/%m/%Y %H:%M')}")
        print(f"{'='*50}")

        for item in self._itens:
            print(f"{item['produto'].nome} x{item['quantidade']} = R${item['subtotal']:.2f}")

        print(f"{'-'*50}")
        print(f"TOTAL: R${self.valor_total:.2f}")
        print(f"{'='*50}\n")
            