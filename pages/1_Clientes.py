import streamlit as st
import sqlite3
# Importamos as novas funções que acabamos de criar
from utils.database import get_db_connection, listar_clientes, deletar_cliente

# --- Configuração da Página ---
st.set_page_config(page_title="Cadastro de Clientes", page_icon="👤")
st.title("👤 Cadastro de Clientes")
st.markdown("---")

# --- Formulário de Cadastro ---
with st.form(key="cadastro_cliente", clear_on_submit=True):
    nome_cliente = st.text_input("Nome do Cliente*", placeholder="Digite o nome completo")
    telefone_cliente = st.text_input("Telefone", placeholder="(XX) XXXXX-XXXX")
    email_cliente = st.text_input("Email", placeholder="exemplo@email.com")
    submit_button = st.form_submit_button("Cadastrar Cliente")

# --- Lógica de Inserção no Banco de Dados ---
if submit_button:
    if not nome_cliente:
        st.error("O campo 'Nome do Cliente' é obrigatório!")
    else:
        try:
            conn = get_db_connection()
            sql = "INSERT INTO Clientes (nome, telefone, email) VALUES (?, ?, ?)"
            conn.execute(sql, (nome_cliente, telefone_cliente, email_cliente))
            conn.commit()
            conn.close()
            st.success(f"Cliente '{nome_cliente}' cadastrado com sucesso!")
        except sqlite3.IntegrityError:
            st.error(f"Erro: O email '{email_cliente}' já está cadastrado.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao cadastrar o cliente: {e}")

# --- SEÇÃO DE CONSULTA E DELEÇÃO DE CLIENTES (NOVO) ---
st.markdown("---")
st.subheader("Clientes Cadastrados")

# Busca os clientes no banco de dados
clientes = listar_clientes()

if not clientes:
    st.info("Nenhum cliente cadastrado ainda.")
else:
    # Cria um layout com colunas para alinhar as informações e o botão
    col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.3, 0.1])
    col1.markdown("**Nome**")
    col2.markdown("**Telefone**")
    col3.markdown("**Email**")

    # Itera sobre cada cliente e exibe suas informações
    for cliente in clientes:
        with st.container():
            col1, col2, col3, col4 = st.columns([0.3, 0.3, 0.3, 0.1])
            col1.write(cliente['nome'])
            col2.write(cliente['telefone'])
            col3.write(cliente['email'])

            # Botão de deleção na quarta coluna
            if col4.button("🗑️", key=f"delete_{cliente['id']}"):
                try:
                    deletar_cliente(cliente['id'])
                    st.success(f"Cliente '{cliente['nome']}' deletado com sucesso!")
                    st.rerun()  # Recarrega a página para atualizar a lista
                except Exception as e:
                    st.error(f"Erro ao deletar o cliente: {e}")
                    print("")