import streamlit as st
import sqlite3
from utils.database import get_db_connection, listar_fornecedores, deletar_fornecedor

# --- Configuração da Página ---
st.set_page_config(page_title="Cadastro de Fornecedores", page_icon="🚚")
st.title("🚚 Cadastro de Fornecedores")
st.markdown("---")

# --- Formulário de Cadastro ---
with st.form(key="cadastro_fornecedor", clear_on_submit=True):
    nome_fornecedor = st.text_input("Nome do Fornecedor*", placeholder="Digite o nome da empresa")
    contato_fornecedor = st.text_input("Contato (Telefone/Email)", placeholder="Informações de contato")
    endereco_fornecedor = st.text_input("Endereço", placeholder="Endereço completo")
    submit_button = st.form_submit_button("Cadastrar Fornecedor")

# --- Lógica de Inserção ---
if submit_button:
    if not nome_fornecedor:
        st.error("O campo 'Nome do Fornecedor' é obrigatório!")
    else:
        try:
            conn = get_db_connection()
            sql = "INSERT INTO Fornecedores (nome, contato, endereco) VALUES (?, ?, ?)"
            conn.execute(sql, (nome_fornecedor, contato_fornecedor, endereco_fornecedor))
            conn.commit()
            conn.close()
            st.success(f"Fornecedor '{nome_fornecedor}' cadastrado com sucesso!")
        except Exception as e:
            st.error(f"Ocorreu um erro ao cadastrar o fornecedor: {e}")

# --- Seção de Consulta e Deleção ---
st.markdown("---")
st.subheader("Fornecedores Cadastrados")

fornecedores = listar_fornecedores()

if not fornecedores:
    st.info("Nenhum fornecedor cadastrado ainda.")
else:
    col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.3, 0.1])
    col1.markdown("**Nome**")
    col2.markdown("**Contato**")
    col3.markdown("**Endereço**")

    for fornecedor in fornecedores:
        with st.container():
            col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.3, 0.1])
            col1.write(fornecedor['nome'])
            col2.write(fornecedor['contato'])
            col3.write(fornecedor['endereco'])
            if col4.button("🗑️", key=f"delete_forn_{fornecedor['id']}"):
                try:
                    deletar_fornecedor(fornecedor['id'])
                    st.success(f"Fornecedor '{fornecedor['nome']}' deletado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao deletar o fornecedor: {e}")