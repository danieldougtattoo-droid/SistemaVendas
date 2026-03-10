# Sistema de Vendas

Um sistema de gerenciamento de vendas desenvolvido em Python com integração ao SQL Server, utilizando Programação Orientada a Objetos (POO) e @property para demonstrar boas práticas de desenvolvimento.

---

🎯 Objetivo

Este projeto foi desenvolvido como portfólio para demonstrar conhecimentos em:

Python avançado com POO

Integração com banco de dados SQL Server

Uso de @property e encapsulamento

Criação de sistemas de vendas

---

🛠️ Tecnologias Utilizadas

Python 3.8+

SQL Server 2019+

Bibliotecas:

pyodbc - Conexão com SQL Server

faker - Geração de dados fictícios

Gradio e Panda

---

📋 Funcionalidades

✅ Gerenciamento de Clientes

Listar clientes

Visualizar histórico de compras

Calcular total gasto por cliente

✅ Gerenciamento de Produtos

Listar produtos

Controlar estoque

Validar disponibilidade

✅ Criar Vendas

Selecionar cliente

Adicionar múltiplos produtos

Atualizar estoque automaticamente

Gerar resumo da venda

✅ Relatórios

Produtos mais vendidos

Clientes top (maior gasto)

Vendas por mês

---

📁 Estrutura do Projeto

SistemaVendas/
├── main.py                      # Arquivo principal - menu interativo
├── conexao.py                   # Classe ConexaoBancoDados
├── cliente.py                   # Classe Cliente
├── produto.py                   # Classe Produto
├── venda.py                     # Classe Venda
├── relatorio.py                 # Classe RelatorioVendas
├── gerar_dados_fake.py          # Script para gerar clientes fake
├── gerar_produtos_fake.py       # Script para gerar produtos fake
├── sistema_vendas.py            # (Opcional) Todas as classes juntas
└── README.md                    # Este arquivo

---

🚀 Como Usar

1. Pré-requisitos

Python 3.8+ instalado

SQL Server instalado e rodando

Visual Studio Code ou editor de texto

2.Instalação

Clone ou baixe o projeto:

```bash
git clone
https://github.com/danieldougtattoo-droid
/SistemaVendas.git
cd SistemaVendas
````

Instale as dependências:

pip install pyodbc faker

3.Configurar Banco de Dados

Execute o script SQL para criar o banco:

CREATE DATABASE SistemaVendas;
GO
USE SistemaVendas;
GO
-- Criar tabelas conforme necessário

4.Gerar Dados Fictícios

python gerar_dados_fake.py
python gerar_produtos_fake.py

5.Executar o Sistema

python main.py

💡 Como Funciona

Menu Principal

Ao executar main.py, aparecerá um menu como:

## SISTEMA DE VENDAS

1. Criar uma venda
2. Ver relatórios
3. Listar clientes
4. Listar produtos
5. Sair

🏗️ Arquitetura das Classes

ConexaoBancoDados

Gerencia conexão com SQL Server

Executa queries

Valida conexão

Produto

Representa um produto

Controla estoque

Valida disponibilidade

Cliente

Representa um cliente

Armazena histórico de compras

Calcula total gasto
Venda

Representa uma venda

Adiciona itens

Atualiza estoque gera resumo formatado

RelatorioVendas

Consulta banco

Gera relatórios de vendas

---

🔐 Boas Práticas Implementadas

Encapsulamento

Uso de @property

Validação de dados

Docstrings

Type hints

Tratamento de erros

---

📊 Dados do Banco

50 clientes fictícios

20 produtos

Estrutura preparada para vendas

---

🐛 Possíveis Problemas

"Não foi possível conectar ao banco"

Verifique SQL Server

Confirme nome do servidor

Confirme nome do banco

"pyodbc not found"

pip install --upgrade pyodbc faker

---

Dashboard de Performance (BI)
​O sistema transforma dados brutos em inteligência visual para facilitar a tomada de decisão:

​1. Volume de Vendas por Produto (Desempenho)

​Identifica instantaneamente quais itens possuem maior saída, permitindo um controle de estoque e marketing mais eficiente.
![Gráfico de Barras]
(indicadores.jpg)

​2. Market Share (Participação por Cliente)

​Análise detalhada da concentração de faturamento por cliente, facilitando a identificação dos parceiros mais estratégicos.
![Gráfico de pizza](pizza.jpg)

​📑 Gestão de Dados e Relatórios
​Além da visualização, o sistema garante a integridade e a portabilidade das informações:

​Persistência em SQL Server: Registro em tempo real via pyodbc.
​Exportação para Excel: Geração automática de relatórios formatados para auditoria e análise offline.
![Relatório Excel](Execel.jpg)
​🛠️ Tecnologias Utilizadas
​Interface: Gradio (Web UI)
​Banco de Dados: Microsoft SQL Server
​Processamento de Dados: Pandas
​Gráficos: Plotly Express
​Exportação: Openpyxl (Relatórios .xlsx)
​⚙️ Como Executar
​Clone o repositório.
​Instale as dependências: pip install -r requirements.txt.
​Verifique a string de conexão no arquivo conexao.py.
​Execute o comando: python app_gradio.py.

👨‍💻 Autor

Desenvolvido como projeto de portfólio para demonstrar conhecimentos em Python e SQL Server.

---

📞 Contato

📱 WhatsApp: 11 98858-2267
📧 Email:dougintelectual@hotmail.com

---

📝 Licença

Projeto aberto para uso educacional e estudos.

---

Desenvolvido com ❤️ em Python
