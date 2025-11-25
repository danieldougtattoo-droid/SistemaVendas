import gradio as gr
import pandas as pd
from conexao import ConexaoBancoDados
from Cliente import Cliente
from produto import Produto
from venda import Venda
from relatorio import RelatorioVendas

# Conectar ao banco
db = ConexaoBancoDados(r"DOUGTATTOO\SQLEXPRESS", "SistemaVendas")
db.conectar()

# Variável global para armazenar venda em andamento
venda_atual = None
cliente_selecionado = None

def buscar_clientes():
    """Busca clientes do banco"""
    query = "SELECT id, nome, email FROM Clientes"
    cursor = db.executar_query(query)
   
    if cursor:
        clientes = cursor.fetchall()
        return [(f"{c[1]} - {c[2]}", c[0]) for c in clientes]
    return []

def buscar_produtos():
    """Busca produtos do banco"""
    query = "SELECT id, nome, preco, estoque FROM Produtos"
    cursor = db.executar_query(query)
   
    if cursor:
        produtos = cursor.fetchall()
        return [(f"{p[1]} - R${p[2]:.2f} (Estoque: {p[3]})", p[0]) for p in produtos]
    return []

def listar_clientes_df():
    """Lista clientes em formato de tabela"""
    try:
        query = "SELECT TOP 100 id, nome, email, telefone FROM Clientes"
        cursor = db._conexao.cursor()
        cursor.execute(query)
        dados = cursor.fetchall()
        cursor.close()
        
        if dados and len(dados) > 0:
            # Converter pyodbc.Row ou tuplas diretamente para lista
            # pyodbc.Row se comporta como tupla mas não passa em isinstance(row, tuple)
            dados_lista = [list(row) for row in dados]
            
            # Verificar se os dados têm o formato correto
            if len(dados_lista) > 0:
                num_colunas = len(dados_lista[0])
                
                if num_colunas == 4:
                    df = pd.DataFrame(dados_lista, columns=['ID', 'Nome', 'Email', 'Telefone'])
                    return df
                else:
                    print(f"Erro: Dados retornaram {num_colunas} colunas, esperado 4")
                    print(f"Primeira linha processada: {dados_lista[0]}")
                    print(f"Tipo da primeira linha: {type(dados_lista[0])}")
    except Exception as e:
        print(f"Erro ao processar dados de clientes: {e}")
        import traceback
        traceback.print_exc()
    
    return pd.DataFrame(columns=['ID', 'Nome', 'Email', 'Telefone'])

def listar_produtos_df():
    """Lista produtos em formato de tabela"""
    try:
        query = "SELECT TOP 100 id, nome, preco, estoque, categoria FROM Produtos"
        cursor = db._conexao.cursor()
        cursor.execute(query)
        dados = cursor.fetchall()
        cursor.close()
        
        if dados and len(dados) > 0:
            # Debug: verificar formato dos dados originais
            print(f"Debug produtos - Tipo do primeiro elemento: {type(dados[0])}")
            print(f"Debug produtos - Primeiro elemento: {dados[0]}")
            
            # Converter para lista de listas
            # pyodbc.Row se comporta como tupla mas não passa em isinstance(row, tuple)
            # Vamos converter diretamente para lista
            dados_lista = [list(row) for row in dados]
            
            # Verificar se os dados têm o formato correto
            if len(dados_lista) > 0:
                # Se a primeira linha ainda é uma lista contendo uma tupla, extrair todas as linhas
                if len(dados_lista[0]) == 1 and isinstance(dados_lista[0][0], tuple):
                    dados_lista = [list(row[0]) for row in dados_lista]
                
                num_colunas = len(dados_lista[0])
                
                if num_colunas == 5:
                    df = pd.DataFrame(dados_lista, columns=['ID', 'Nome', 'Preço', 'Estoque', 'Categoria'])
                    df['Preço'] = df['Preço'].apply(lambda x: f"R${float(x):.2f}" if x is not None else "R$0.00")
                    return df
                else:
                    print(f"Erro: Dados retornaram {num_colunas} colunas, esperado 5")
                    print(f"Primeira linha processada: {dados_lista[0]}")
                    print(f"Tipo da primeira linha: {type(dados_lista[0])}")
    except Exception as e:
        print(f"Erro ao processar dados de produtos: {e}")
        import traceback
        traceback.print_exc()
    
    return pd.DataFrame(columns=['ID', 'Nome', 'Preço', 'Estoque', 'Categoria'])

def iniciar_venda(cliente_nome):
    """Inicia uma nova venda"""
    global venda_atual, cliente_selecionado
   
    if not cliente_nome:
        return "❌ Selecione um cliente!", "", gr.update(visible=False)
   
    # Extrair ID do cliente
    cliente_id = int(cliente_nome.split(" - ")[0].split(":")[0]) if ":" in cliente_nome else None
   
    if not cliente_id:
        # Buscar cliente pelo nome
        query = "SELECT id, nome, email, telefone FROM Clientes WHERE nome = ?"
        nome_limpo = cliente_nome.split(" - ")[0]
        cursor = db.executar_query(query, (nome_limpo,))
       
        if cursor:
            cliente_data = cursor.fetchone()
            if cliente_data:
                cliente_selecionado = Cliente(cliente_data[0], cliente_data[1], cliente_data[2], cliente_data[3])
                venda_atual = Venda(1, cliente_selecionado)
                return (
                    f"✅ Venda iniciada para: {cliente_selecionado.nome}",
                    "Nenhum item adicionado ainda",
                    gr.update(visible=True)
                )
   
    return "❌ Cliente não encontrado!", "", gr.update(visible=False)

def adicionar_item_venda(produto_nome, quantidade):
    """Adiciona item à venda"""
    global venda_atual
   
    if not venda_atual:
        return "❌ Inicie uma venda primeiro!", ""
   
    if not produto_nome or quantidade <= 0:
        return "❌ Selecione um produto e quantidade válida!", exibir_resumo_venda()
   
    # Buscar produto
    query = "SELECT id, nome, preco, estoque, categoria FROM Produtos WHERE nome LIKE ?"
    nome_produto = produto_nome.split(" - ")[0]
    cursor = db.executar_query(query, (f"%{nome_produto}%",))
   
    if cursor:
        produto_data = cursor.fetchone()
        if produto_data:
            produto = Produto(produto_data[0], produto_data[1], float(produto_data[2]), produto_data[3], produto_data[4])
            venda_atual.adicionar_item(produto, quantidade)
            return f"✅ {quantidade}x {produto.nome} adicionado!", exibir_resumo_venda()
   
    return "❌ Produto não encontrado!", exibir_resumo_venda()

def exibir_resumo_venda():
    """Exibe resumo da venda atual"""
    global venda_atual
   
    if not venda_atual or len(venda_atual.itens) == 0:
        return "Nenhum item na venda"
   
    resumo = f"**Cliente:** {venda_atual.cliente.nome}\n\n"
    resumo += "**Itens:**\n"
   
    for item in venda_atual.itens:
        resumo += f"- {item['produto'].nome} x{item['quantidade']} = R${item['subtotal']:.2f}\n"
   
    resumo += f"\n**TOTAL: R${venda_atual.valor_total:.2f}**"
   
    return resumo

def finalizar_venda_atual():
    """Finaliza a venda"""
    global venda_atual, cliente_selecionado
   
    if not venda_atual:
        return "❌ Nenhuma venda em andamento!", "", gr.update(visible=False)
   
    if venda_atual.finalizar_venda(db):
        mensagem = f"✅ Venda finalizada! Total: R${venda_atual.valor_total:.2f}"
        venda_atual = None
        cliente_selecionado = None
        return mensagem, "", gr.update(visible=False)
   
    return "❌ Erro ao finalizar venda!", exibir_resumo_venda(), gr.update(visible=True)

def cancelar_venda_atual():
    """Cancela a venda"""
    global venda_atual, cliente_selecionado
   
    venda_atual = None
    cliente_selecionado = None
   
    return "❌ Venda cancelada", "", gr.update(visible=False)

def obter_relatorio_produtos():
    """Gera relatório de produtos mais vendidos"""
    relatorio = RelatorioVendas(db)
    produtos = relatorio.produtos_mais_vendidos()
   
    if produtos and len(produtos) > 0:
        dados = [(p[0], p[1], f"R${float(p[2]):.2f}") for p in produtos]
        df = pd.DataFrame(dados, columns=['Produto', 'Quantidade', 'Valor Total'])
        return df
   
    return pd.DataFrame(columns=['Produto', 'Quantidade', 'Valor Total'])

def obter_relatorio_clientes():
    """Gera relatório de clientes top"""
    relatorio = RelatorioVendas(db)
    clientes = relatorio.clientes_top()
   
    if clientes and len(clientes) > 0:
        dados = [(c[0], c[1], f"R${float(c[2]):.2f}") for c in clientes]
        df = pd.DataFrame(dados, columns=['Cliente', 'Compras', 'Valor Total'])
        return df
   
    return pd.DataFrame(columns=['Cliente', 'Compras', 'Valor Total'])

# Interface Gradio
with gr.Blocks(title="Sistema de Vendas") as app:
   
    gr.Markdown("# 🛒 Sistema de Vendas")
    gr.Markdown("Sistema de gerenciamento de vendas com Python e SQL Server")
   
    with gr.Tabs():
       
        # ABA 1: Criar Venda
        with gr.Tab("🛍️ Criar Venda"):
            gr.Markdown("### Iniciar Nova Venda")
           
            with gr.Row():
                cliente_dropdown = gr.Dropdown(
                    choices=[c[0] for c in buscar_clientes()],
                    label="Selecione o Cliente",
                    interactive=True
                )
                btn_iniciar = gr.Button("Iniciar Venda", variant="primary")
           
            msg_inicio = gr.Markdown("")
           
            with gr.Column(visible=False) as col_itens:
                gr.Markdown("### Adicionar Produtos")
               
                with gr.Row():
                    produto_dropdown = gr.Dropdown(
                        choices=[p[0] for p in buscar_produtos()],
                        label="Selecione o Produto",
                        interactive=True
                    )
                    quantidade_input = gr.Number(
                        label="Quantidade",
                        value=1,
                        minimum=1
                    )
                    btn_adicionar = gr.Button("Adicionar Item", variant="secondary")
               
                msg_item = gr.Markdown("")
               
                gr.Markdown("### Resumo da Venda")
                resumo_venda = gr.Markdown("")
               
                with gr.Row():
                    btn_finalizar = gr.Button("✅ Finalizar Venda", variant="primary")
                    btn_cancelar = gr.Button("❌ Cancelar Venda", variant="stop")
           
            # Eventos
            btn_iniciar.click(
                iniciar_venda,
                inputs=[cliente_dropdown],
                outputs=[msg_inicio, resumo_venda, col_itens]
            )
           
            btn_adicionar.click(
                adicionar_item_venda,
                inputs=[produto_dropdown, quantidade_input],
                outputs=[msg_item, resumo_venda]
            )
           
            btn_finalizar.click(
                finalizar_venda_atual,
                outputs=[msg_inicio, resumo_venda, col_itens]
            )
           
            btn_cancelar.click(
                cancelar_venda_atual,
                outputs=[msg_inicio, resumo_venda, col_itens]
            )
       
        # ABA 2: Relatórios
        with gr.Tab("📊 Relatórios"):
            gr.Markdown("### Relatórios de Vendas")
           
            with gr.Row():
                btn_rel_produtos = gr.Button("🏆 Produtos Mais Vendidos")
                btn_rel_clientes = gr.Button("👥 Clientes Top")
           
            tabela_relatorio = gr.DataFrame(label="Resultados")
           
            btn_rel_produtos.click(
                obter_relatorio_produtos,
                outputs=[tabela_relatorio]
            )
           
            btn_rel_clientes.click(
                obter_relatorio_clientes,
                outputs=[tabela_relatorio]
            )
       
        # ABA 3: Listar Clientes
        with gr.Tab("👥 Clientes"):
            gr.Markdown("### Lista de Clientes")
            btn_listar_clientes = gr.Button("Atualizar Lista")
            tabela_clientes = gr.DataFrame(value=listar_clientes_df(), label="Clientes")
           
            btn_listar_clientes.click(
                listar_clientes_df,
                outputs=[tabela_clientes]
            )
       
        # ABA 4: Listar Produtos
        with gr.Tab("📦 Produtos"):
            gr.Markdown("### Lista de Produtos")
            btn_listar_produtos = gr.Button("Atualizar Lista")
            tabela_produtos = gr.DataFrame(value=listar_produtos_df(), label="Produtos")
           
            btn_listar_produtos.click(
                listar_produtos_df,
                outputs=[tabela_produtos]
            )

# Iniciar aplicação
if __name__ == "__main__":
    app.launch(share=True)