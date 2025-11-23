# from gc import DEBUG_LEAK
# from optparse import OptionContainer
from conexao import ConexaoBancoDados
from Cliente import Cliente
from produto import Produto
import produto
import relatorio
from venda import Venda
from relatorio import RelatorioVendas

def buscar_clientes(db):
    """Busca todos os clientes do banco """
    query = "SELECT TOP 5 id, nome, email, telefone FROM Clientes"
    cursor = db.executar_query(query)

    clientes = []
    if cursor:
        for row in cursor.fetchall():
            cliente = Cliente(row[0], row[1], row[2], row[3])
            clientes.append(cliente)

    return clientes

def buscar_produtos(db):
    query = "SELECT TOP 5 id, nome, preco, estoque, categoria FROM Produtos"
    cursor = db.executar_query(query)

    produtos = []
    if cursor:
        for row in cursor.fetchall():
            produto = Produto(row[0], row[1], row[2], row[3], row[4])
            produtos.append(produto)

    return produtos

def menu_principal():
    """ Menu principal do sistema """
    print("\n" + "="*50)
    print("SISTEMA DE VENDAS")
    print("="*50)
    print("1. Criar uma venda")
    print("2. Ver relatório")
    print("3. Listar clientes")
    print("4. Listar produtos")
    print("5. Sair")
    print("="*50)

    opcao = input("Escolha uma opção (1-5): ").strip()
    return opcao

def criar_venda(db, clientes, produtos):
    """Permite criar uma venda interativa """
    if not clientes:
        print("x Nenhum cliente disponível!")
        return

    if not produtos:
        print("x Nenhum produto disponível!")
        return

    print("\n" + "="*50)
    print("CRIAR VENDA")
    print("="*50)

    # Mostrar clientes
    print("\nClientes disponíveis:")
    for i, cliente in enumerate(clientes, 1):
        print(f"{i}. {cliente.nome} - {cliente.email}")

    cliente_idx = int(input("Escolha o cliente (número):")) - 1
    
    if cliente_idx < 0 or cliente_idx >= len(clientes):
        print("x Cliente inválido!")
        return

    cliente_selecionado = clientes[cliente_idx]

    # Criar venda
    venda = Venda(1, cliente_selecionado)

    #  Adicionar produtos
    while True:
        print("\nProdutos disponíveis:")
        for i, produto in enumerate(produtos, 1):
            print(f"{i}. {produto.nome} - R${produto.preco:.2f} (Estoque: {produto.estoque})")

        produto_idx = int(input("\nEscolha o produto (número) ou 0 para finalizar: ")) - 1
        if produto_idx == -1: # 0 - 1 = -1
            break

        if produto_idx < 0 or produto_idx >= len(produtos):
            print("x Produto inválido!")
            continue
        quantidade = int(input("Quantidade: "))

        produto_selecionado = produtos[produto_idx]
        venda.adicionar_item(produto_selecionado, quantidade)

    # Finalizar venda
    if venda.finalizar_venda():
        venda.exibir_resumo()

def exibir_relatorios(db):
    """  Exibe os relatórios disponíveis """
    print("\n" + "="*50)
    print("RELATÓRIOS")
    print("-"*50)

    relatorio = RelatorioVendas(db)

    # Produtos mais vendidos
    print("\n PRODUTOS MAIS VENDIDOS:")
    print("-"*50)
    produtos = relatorio.produtos_mais_vendidos()
    if produtos:
        for row in produtos:
            print(f" {row[0]}: {row[1]} unidades | R${row[2]:.2f}")
    else:
        print("  Nenhuma venda registrada ainda")

    #  CLIENTES TOP
    print("\n CLIENTE TOP:")
    print("-"*50)
    clientes = relatorio.clientes_top()
    if clientes:
        for row in clientes:
            print(f"  {row[0]}: {row[1]} compras | R${row[2]:.2f}")
    else:
        print(" Nenhum cliente registrado")

    # Vendas por mês
    print("\n VENDAS POR MÊS:")
    print("-"*50)
    vendas_mes = relatorio.vendas_por_mes()
    if vendas_mes:
        for row in vendas_mes:
            print(f"  Mês {row[0]}: {row[1]} vendas | R${row[2]:.2f}")
    else:
        print("   Nenhuma venda registrada")

def listar_clientes(clientes):
    print("\n" + "="*50)
    print("CLIENTES")
    print("="*50)

    if not clientes:
        print("Nenhum cliente encontrado!")
        return

    for cliente in clientes:
        print(f"ID: {cliente.id} | Nome: {cliente.nome} | Email: {cliente.email}")

def listar_produtos(produtos):
    print("\n" + "="*50)
    print("PRODUTOS")
    print("="*50)

    if not produtos:
        print("Nenhum produto encontrado!")
        return

    for produto in produtos:
        print(f"{produto.nome} - R${produto.preco:.2f} | Estoque: {produto.estoque} | {produto.categoria}")

def main():
    """Função principal"""
    # Conectar ao banco
    db = ConexaoBancoDados(r"DOUGTATTOO\SQLEXPRESS", "SistemaVendas")

    if not db.conectar():
        print("Erro ao conectar ao banco de dados!")
        return

    # Buscar dados
    clientes = buscar_clientes(db)
    produtos = buscar_produtos(db)

    #Loop principal
    while True:
        opcao = menu_principal()

        if opcao == "1":
            criar_venda(db, clientes, produtos)

        elif opcao == "2":
            exibir_relatorios(db)
        
        elif opcao == "3":
            listar_clientes(clientes)

        elif opcao == "4":
            listar_produtos(produtos)

        elif opcao == "5":
            print("\n Sistema encerrado!")
            db.desconectar()
            break
        else:
            print("x Opção invalida!")


if __name__ == "__main__":
    main()