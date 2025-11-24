import pyodbc
from datetime import datetime
from typing import List, Optional

# Configuração da conexão  com SQL Server

class ConexaoBancoDados: 
    """Gerencia a conexão com o SQL Server"""

    def __init__(self, servidor, banco):
        self._servidor = servidor
        self._banco = banco
        self._conexao = None

    @property
    def servidor(self):
        """Retorna o servidor """
        return self._servidor

    @property
    def banco(self):
        """ Retorna o nome do banco """
        return self._banco

    @property
    def conexao(self):
        """ Retorna a conexao ativa """
        return self._conexao

    def conectar(self):
        try:
            conexao_string = (
                f'Driver={{ODBC Driver 17 for SQL Server}};'
                f'Server={self._servidor};Database={self._banco};Trusted_Connection=yes;'
            )
            self._conexao = pyodbc.connect(conexao_string)
            print("Conectado ao banco de dados com sucesso!")
            return self._conexao
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return None

    def desconectar(self):
        if self._conexao:
            self._conexao.close()
            print("Desconectado do banco de dados")

    def executar_query(self, query, parametros=None):
        try:
            cursor = self._conexao.cursor()
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            
            # Apenas faz commit para queries que modificam dados (INSERT, UPDATE, DELETE)
            query_upper = query.strip().upper()
            if query_upper.startswith(('INSERT', 'UPDATE', 'DELETE')):
                self._conexao.commit()
            
            return cursor
        except Exception as e:
            print(f"Erro ao executar query: {e}")
            return None
    
    def listar_tabelas(self):
        """Lista todas as tabelas do banco de dados"""
        try:
            query = """
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
            """
            cursor = self._conexao.cursor()
            cursor.execute(query)
            tabelas = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tabelas
        except Exception as e:
            print(f"Erro ao listar tabelas: {e}")
            return []
    
    def tabela_existe(self, nome_tabela):
        """Verifica se uma tabela existe no banco de dados"""
        try:
            query = """
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = ?
            """
            cursor = self._conexao.cursor()
            cursor.execute(query, (nome_tabela,))
            resultado = cursor.fetchone()[0]
            cursor.close()
            return resultado > 0
        except Exception as e:
            print(f"Erro ao verificar tabela: {e}")
            return False
    
    def buscar_tabelas_similares(self, termo):
        """Busca tabelas que contenham o termo no nome"""
        try:
            query = """
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            AND (TABLE_NAME LIKE ? OR TABLE_NAME LIKE ?)
            ORDER BY TABLE_NAME
            """
            cursor = self._conexao.cursor()
            cursor.execute(query, (f'%{termo}%', f'%{termo.lower()}%'))
            tabelas = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return tabelas
        except Exception as e:
            print(f"Erro ao buscar tabelas similares: {e}")
            return []
    
    def listar_colunas_tabela(self, nome_tabela):
        """Lista as colunas de uma tabela"""
        try:
            query = """
            SELECT COLUMN_NAME, DATA_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
            """
            cursor = self._conexao.cursor()
            cursor.execute(query, (nome_tabela,))
            colunas = [(row[0], row[1]) for row in cursor.fetchall()]
            cursor.close()
            return colunas
        except Exception as e:
            print(f"Erro ao listar colunas: {e}")
            return []


