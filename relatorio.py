from conexao import ConexaoBancoDados


class RelatorioVendas:

    def __init__(self, conexao_db: ConexaoBancoDados):
        self._conexao_db = conexao_db

    def vendas_por_mes(self):
        """Retorna vendas agrupadas por mês """
        query = """
        SELECT
             MONTH(data_venda) as mes,
             COUNT(*) as total_vendas,
             SUM(valor_total) as valor_total
        FROM Vendas
        GROUP BY MONTH(data_venda)
        ORDER BY mes
        """

        cursor = self._conexao_db.executar_query(query)
        return cursor.fetchall() if cursor else []

    def produtos_mais_vendidos(self):
        query = """
        SELECT TOP 5
            p.nome,
            SUM(iv.quantidade) as quantidade_total,
            SUM(iv.quantidade * iv.preco_unitario) as valor_total
        FROM ItemVenda iv
        JOIN Produtos p ON iv.produto_id = p.id
        GROUP BY p.nome
        ORDER BY quantidade_total DESC
        """
        
        cursor = self._conexao_db.executar_query(query)
        return cursor.fetchall() if cursor else []

    def clientes_top(self):
        """Retorna os clientes que mais compraram """
        query = """
        SELECT TOP 5
            c.nome,
            COUNT(v.id) as total_compras,
            SUM(v.valor_total) as valor_total
        FROM Clientes c
        JOIN Vendas v ON c.id = v.cliente_id
        GROUP BY c.nome
        ORDER BY valor_total DESC
        """
        
        cursor = self._conexao_db.executar_query(query)
        return cursor.fetchall() if cursor else []

        # Exemplo de sistema
        if __name__ == "__main__":
            # Conectar ao banco
            db = ConexaoBancoDados(r"DOUGTATTOO\SQLEXPRESS", "SistemaVendas")
            db.conectar()
