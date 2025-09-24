import streamlit as st
import pandas as pd
from utils.database import listar_clientes, listar_produtos_em_estoque, registrar_venda

# --- Configuração da Página ---
st.set_page_config(page_title="Realizar Vendas", page_icon="💰")
st.title("💰 Realizar Vendas")
st.markdown("---")

# --- Inicialização do Carrinho no st.session_state ---
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# --- Busca de Dados ---
clientes = listar_clientes()
produtos_estoque = listar_produtos_em_estoque()

if not clientes or not produtos_estoque:
    st.warning("É necessário ter ao menos um cliente e um produto com estoque cadastrado para realizar uma venda.")
else:
    # --- Seleção do Cliente ---
    clientes_dict = {c['id']: c['nome'] for c in clientes}
    id_cliente_selecionado = st.selectbox(
        "Selecione o Cliente*",
        options=list(clientes_dict.keys()),
        format_func=lambda id: clientes_dict[id]
    )

    st.markdown("---")
    st.subheader("Adicionar Produtos ao Carrinho")

    # --- Formulário para Adicionar Produto ---
    produtos_dict = {p['id']: p for p in produtos_estoque}

    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        id_produto_selecionado = st.selectbox(
            "Selecione um Produto",
            options=list(produtos_dict.keys()),
            format_func=lambda id: f"{produtos_dict[id]['nome']} (Estoque: {produtos_dict[id]['quantidade_estoque']})"
        )

    produto_selecionado = produtos_dict.get(id_produto_selecionado)

    with col2:
        if produto_selecionado:
            quantidade = st.number_input(
                "Quantidade",
                min_value=1,
                max_value=produto_selecionado['quantidade_estoque'],
                step=1
            )

    if st.button("Adicionar ao Carrinho", use_container_width=True):
        item_carrinho = {
            "id": produto_selecionado['id'],
            "nome": produto_selecionado['nome'],
            "quantidade": quantidade,
            "preco_venda": produto_selecionado['preco_venda'],
            "subtotal": quantidade * produto_selecionado['preco_venda']
        }
        st.session_state.carrinho.append(item_carrinho)
        st.success(f"{quantidade}x '{produto_selecionado['nome']}' adicionado ao carrinho!")

    st.markdown("---")
    st.subheader("🛒 Carrinho de Compras")

    # --- Exibição do Carrinho e Finalização da Venda ---
    if not st.session_state.carrinho:
        st.info("O carrinho está vazio.")
    else:
        df_carrinho = pd.DataFrame(st.session_state.carrinho)
        st.dataframe(df_carrinho[['nome', 'quantidade', 'preco_venda', 'subtotal']], use_container_width=True)

        valor_total = df_carrinho['subtotal'].sum()
        st.metric("Valor Total da Venda", f"R$ {valor_total:.2f}")

        if st.button("Finalizar Venda", type="primary", use_container_width=True):
            try:
                registrar_venda(id_cliente_selecionado, valor_total, st.session_state.carrinho)
                st.success("Venda registrada com sucesso!")
                # Limpa o carrinho e recarrega a página
                st.session_state.carrinho = []
                st.rerun()
            except Exception as e:
                st.error(f"Ocorreu um erro ao finalizar a venda: {e}")