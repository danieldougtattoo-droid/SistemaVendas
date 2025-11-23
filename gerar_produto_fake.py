import pyodbc
from faker import Faker
import random

import conexao

SERVIDOR = "DOUGTATTOO\SQLEXPRESS"
BANCO = "SistemaVendas"

#  Categoria de produtos
CATEGORIAS = ["Eletrônicos", "Acessórios", "Periféricos", "Software", "Impressora"]

# Nome dos produtos
NOMES_PRODUTOS = [
    "Notebook", "Desktop", "Monitor", "Teclado", "Mouse",
    "Webcam", "Headset", "Mousepad", "Hub USB", "Cabo HDMI",
    "Fonte", "Cooler", "SSD", "Memória RAM", "Processador",
    "Placa de vídeo", "Impressora", "Scanner", "Roteador", "Switch"
]

def gerar_produtos_fake(quantidade=20):
    """Gerar produtos fictícios """
    produtos = []

    for _ in range(quantidade):
        produto = {
            'nome': random.choice(NOMES_PRODUTOS),
            'preco': round(random.uniform(50, 5000), 2),
            'estoque': random.randint(5, 100),
            'categoria': random.choice(CATEGORIAS)
        }
        produtos.append(produto)
    return produtos

def inserir_produtos_no_banco(produtos):
    """Insere os produtos gerados no SQL Server"""
    try:
        # Conectar ao banco
        conexao_string = f'Driver={{ODBC Driver 17 for SQL Server}};Server={SERVIDOR};Database={BANCO};Trusted_Connection=yes;'
        conexao = pyodbc.connect(conexao_string)
        cursor = conexao.cursor()

        #Limpar produtos antigos
        # print("Limpando produtos antigos")
        # cursor.execute(query, (produto['nome'], produto['preco'], produto['estoque'], produto['categoria']))
        # conexao.commit()

        # Inserir novos produtos
        print(f"Inserindo {len(produtos)} produtos fake...")

        for produto in produtos:
            query = "INSERT INTO Produtos(nome, preco, estoque, categoria) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (produto['nome'], produto['preco'], produto['estoque'], produto['categoria']))

        conexao.commit()
        print(f"{len(produtos)} produtos inseridos com sucesso!")

        # Verificar dados
        cursor.execute("SELECT COUNT(*) FROM Produtos")
        total = cursor.fetchone()[0]
        print(f"Total de produtos no banco: {total}")
        
        # Mostrar alguns produtos inseridos
        print("\nAlguns produtos inseridos:")
        cursor.execute("SELECT TOP 6 nome, preco, estoque, categoria FROM Produtos ORDER BY id DESC")
        for row in cursor.fetchall():
            print(f" - {row[0]} | R${row[1]:.2f} | Estoque: {row[2]} | {row[3]}")

        conexao.close()

    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("GERADOR DE PRODUTOS FAKE")
    print("=" * 50)

    # Gerar produtos
    produtos_fake = gerar_produtos_fake(20)

    # Exibir alguns exemplos
    print("\nInserindo no banco de dados...")
    inserir_produtos_no_banco(produtos_fake)

print("\n" + "=" * 50)
print("Processo finalizado!")
print("=" * 50)