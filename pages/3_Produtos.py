import streamlit as st
import sqlite3
# Note que importamos funções de fornecedores também!
from utils.database import get_db_connection, listar_fornecedores, listar_produtos, deletar_produto

# --- Configuração da Página ---
st.set_page_config(page_title="Cadastro de Produtos", page_icon="📦")
st.title("📦 Cadastro de Produtos")
st.markdown("---")

# --- Busca os fornecedores para popular o selectbox ---
fornecedores = listar_fornecedores()

if not fornecedores:
    st.warning("Nenhum fornecedor cadastrado. Por favor, cadastre um fornecedor primeiro na página 'Fornecedores'.")
else:
    # Cria um dicionário para mapear id -> nome, facilitando a exibição no selectbox
    fornecedores_dict = {f['id']: f['nome'] for f in fornecedores}

    # --- Formulário de Cadastro ---
    with st.form(key="cadastro_produto", clear_on_submit=True):
        nome_produto = st.text_input("Nome do Produto*", placeholder="Digite o nome do produto")
        descricao_produto = st.text_area("Descrição", placeholder="Detalhes do produto")

        # Campos numéricos e de seleção em colunas
        col1, col2, col3 = st.columns(3)
        preco_venda = col1.number_input("Preço de Venda (R$)*", min_value=0.0, format="%.2f")
        quantidade_estoque = col2.number_input("Qtd. em Estoque*", min_value=0, step=1)
        id_fornecedor = col3.selectbox(
            "Fornecedor*",
            options=list(fornecedores_dict.keys()),  # As opções são os IDs
            format_func=lambda id: fornecedores_dict[id]  # Exibe os nomes
        )

        submit_button = st.form_submit_button("Cadastrar Produto")

    # --- Lógica de Inserção ---
    if submit_button:
        if not nome_produto or preco_venda <= 0:
            st.error("Os campos 'Nome do Produto' e 'Preço de Venda' são obrigatórios.")
        else:
            try:
                conn = get_db_connection()
                sql = """
                INSERT INTO Produtos (nome, descricao, preco_venda, quantidade_estoque, id_fornecedor)
                VALUES (?, ?, ?, ?, ?)
                """
                conn.execute(sql, (nome_produto, descricao_produto, preco_venda, quantidade_estoque, id_fornecedor))
                conn.commit()
                conn.close()
                st.success(f"Produto '{nome_produto}' cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao cadastrar o produto: {e}")

# --- Seção de Consulta e Deleção ---
st.markdown("---")
st.subheader("Produtos Cadastrados")
produtos = listar_produtos()

if not produtos:
    st.info("Nenhum produto cadastrado ainda.")
else:
    # Exibição dos produtos com o nome do fornecedor
    for produto in produtos:
        with st.container():
            st.markdown(f"**{produto['nome']}** | **Fornecedor:** {produto['fornecedor_nome']}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Preço", f"R$ {produto['preco_venda']:.2f}")
            col2.metric("Estoque", f"{produto['quantidade_estoque']} un.")

            with col3:
                st.write("")  # Espaçamento
                if st.button("🗑️ Deletar", key=f"delete_prod_{produto['id']}", use_container_width=True):
                    try:
                        deletar_produto(produto['id'])
                        st.success(f"Produto '{produto['nome']}' deletado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao deletar produto: {e}")
            st.markdown("---")