import sqlite3

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados SQLite.
    A conexão é configurada para retornar linhas que podem ser acessadas por nome de coluna.
    """
    conn = sqlite3.connect('./database/sistema.db')
    conn.row_factory = sqlite3.Row
    return conn

def listar_clientes():
    """Busca e retorna todos os clientes cadastrados no banco de dados."""
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM Clientes ORDER BY nome').fetchall()
    conn.close()
    return clientes


def deletar_cliente(id):
    """Deleta um cliente do banco de dados com base no seu id."""
    conn = get_db_connection()
    conn.execute('DELETE FROM Clientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def listar_fornecedores():
    """Busca e retorna todos os fornecedores cadastrados."""
    conn = get_db_connection()
    fornecedores = conn.execute('SELECT * FROM Fornecedores ORDER BY nome').fetchall()
    conn.close()
    return fornecedores

def deletar_fornecedor(id):
    """Deleta um fornecedor do banco de dados com base no seu id."""
    conn = get_db_connection()
    conn.execute('DELETE FROM Fornecedores WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def listar_produtos():
    """Busca e retorna todos os produtos com o nome do fornecedor."""
    conn = get_db_connection()
    # Usamos JOIN para combinar dados da tabela Produtos e Fornecedores
    produtos = conn.execute('''
        SELECT p.id, p.nome, p.descricao, p.preco_venda, p.quantidade_estoque, f.nome as fornecedor_nome
        FROM Produtos p
        JOIN Fornecedores f ON p.id_fornecedor = f.id
        ORDER BY p.nome
    ''').fetchall()
    conn.close()
    return produtos

def deletar_produto(id):
    """Deleta um produto do banco de dados com base no seu id."""
    conn = get_db_connection()
    conn.execute('DELETE FROM Produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()


def listar_produtos_em_estoque():
    """Busca e retorna todos os produtos com estoque maior que zero."""
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM Produtos WHERE quantidade_estoque > 0 ORDER BY nome').fetchall()
    conn.close()
    return produtos


def registrar_venda(id_cliente, valor_total, carrinho):
    """
    Registra uma nova venda e atualiza o estoque e o caixa.
    Usa uma transação para garantir a integridade dos dados.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Inserir na tabela Vendas
        sql_venda = "INSERT INTO Vendas (id_cliente, valor_total) VALUES (?, ?)"
        cursor.execute(sql_venda, (id_cliente, valor_total))
        id_venda = cursor.lastrowid  # Pega o ID da venda que acabamos de criar

        # 2. Inserir na tabela Caixa
        sql_caixa = "INSERT INTO Caixa (descricao, tipo_transacao, valor, id_venda) VALUES (?, 'entrada', ?, ?)"
        cursor.execute(sql_caixa, (f"Venda #{id_venda}", valor_total, id_venda))

        # 3. Inserir itens da venda e atualizar o estoque (loop)
        sql_itens_venda = "INSERT INTO ItensVenda (id_venda, id_produto, quantidade, preco_unitario) VALUES (?, ?, ?, ?)"
        sql_update_estoque = "UPDATE Produtos SET quantidade_estoque = quantidade_estoque - ? WHERE id = ?"

        for item in carrinho:
            cursor.execute(sql_itens_venda, (id_venda, item['id'], item['quantidade'], item['preco_venda']))
            cursor.execute(sql_update_estoque, (item['quantidade'], item['id']))

        # Se tudo deu certo, confirma a transação
        conn.commit()

    except Exception as e:
        # Se qualquer passo deu errado, desfaz todas as alterações
        conn.rollback()
        # Propaga o erro para ser tratado na interface
        raise e
    finally:
        # Garante que a conexão será fechada
        conn.close()
def calcular_saldo_caixa():
    """
    Calcula o saldo atual do caixa somando todas as entradas e subtraindo todas as saídas.
    Retorna um único valor de saldo.
    """
    conn = get_db_connection()
    # IFNULL garante que se não houver entradas ou saídas, o valor seja 0 em vez de NULO.
    query = """
    SELECT 
        (SELECT IFNULL(SUM(valor), 0) FROM Caixa WHERE tipo_transacao = 'entrada') -
        (SELECT IFNULL(SUM(valor), 0) FROM Caixa WHERE tipo_transacao = 'saida') as saldo
    """
    saldo = conn.execute(query).fetchone()['saldo']
    conn.close()
    return saldo

def listar_transacoes_caixa():
    """Busca e retorna todas as transações do caixa, da mais recente para a mais antiga."""
    conn = get_db_connection()
    transacoes = conn.execute('SELECT * FROM Caixa ORDER BY data_transacao DESC').fetchall()
    conn.close()
    return transacoes

def adicionar_transacao_caixa(descricao, tipo, valor):
    """Adiciona um lançamento manual no caixa."""
    conn = get_db_connection()
    # Garantimos que o tipo seja 'entrada' ou 'saida'
    tipo_transacao = 'entrada' if tipo.lower() == 'entrada' else 'saida'
    sql = "INSERT INTO Caixa (descricao, tipo_transacao, valor) VALUES (?, ?, ?)"
    conn.execute(sql, (descricao, tipo_transacao, valor))
    conn.commit()
    conn.close()