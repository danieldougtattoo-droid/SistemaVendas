import pyodbc
from faker import Faker

servidor = r"DOUGTATTOO\SQLEXPRESS"
BANCO = "SistemaVendas"

def gerar_clientes_fake(quantidade=50):
    """Gera clientes fictícios usando Faker"""
    fake = Faker('pt_BR')
    clientes = []

    for _ in range(quantidade):
        cliente = {
            'nome': fake.name(),
            'email': fake.unique.email(),
            'telefone': fake.phone_number()
        }
        clientes.append(cliente)
    return clientes

def inserir_clientes_no_banco(clientes):
    """Insere os clientes gerados no SQL Server usando pyodbc."""
    
    conexao_string = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={servidor};"
        f"DATABASE={BANCO};"
        f"Trusted_Connection=yes;"
    )
    conexao = None
    try:
        conexao = pyodbc.connect(conexao_string)
        cursor = conexao.cursor()

        for c in clientes:
            cursor.execute("""INSERT INTO Clientes (nome, email, telefone)
                           VALUES(?, ?, ?)
            """, c['nome'], c['email'], c['telefone'])

        conexao.commit()
        conexao.close()

        print(f"{len(clientes)} clientes inseridos com sucesso!")

    except Exception as e:
        print(f"Erro ao inserir clientes: {e}")

clientes_fake = gerar_clientes_fake(50)
inserir_clientes_no_banco(clientes_fake)



    