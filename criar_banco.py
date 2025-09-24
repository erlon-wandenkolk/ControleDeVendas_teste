import sqlite3

# Nome do arquivo do banco de dados
NOME_BANCO_DADOS = "sistema.db"

# Conecta ao banco de dados (se não existir, ele será criado)
conexao = sqlite3.connect(NOME_BANCO_DADOS)
cursor = conexao.cursor()

# O código SQL que definimos acima
sql_script = """
-- Tabela para armazenar os dados dos fornecedores
CREATE TABLE IF NOT EXISTS Fornecedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    contato TEXT,
    endereco TEXT
);

-- Tabela para armazenar os produtos
CREATE TABLE IF NOT EXISTS Produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco_venda REAL NOT NULL,
    quantidade_estoque INTEGER NOT NULL,
    id_fornecedor INTEGER,
    FOREIGN KEY (id_fornecedor) REFERENCES Fornecedores(id)
);

-- Tabela para armazenar os dados dos clientes
CREATE TABLE IF NOT EXISTS Clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT UNIQUE
);

-- Tabela para registrar as vendas (cabeçalho da venda)
CREATE TABLE IF NOT EXISTS Vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total REAL NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id)
);

-- Tabela de junção para registrar os produtos de cada venda
CREATE TABLE IF NOT EXISTS ItensVenda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venda INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES Vendas(id),
    FOREIGN KEY (id_produto) REFERENCES Produtos(id)
);

-- Tabela para o controle de caixa (entradas e saídas)
CREATE TABLE IF NOT EXISTS Caixa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    tipo_transacao TEXT NOT NULL,
    valor REAL NOT NULL,
    data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_venda INTEGER,
    FOREIGN KEY (id_venda) REFERENCES Vendas(id)
);
"""

# Executa o script SQL para criar as tabelas
# O método executescript pode executar múltiplas instruções SQL de uma vez
cursor.executescript(sql_script)

# Confirma as alterações no banco de dados
conexao.commit()

# Fecha a conexão
conexao.close()

print(f"Banco de dados '{NOME_BANCO_DADOS}' e tabelas criados com sucesso!")