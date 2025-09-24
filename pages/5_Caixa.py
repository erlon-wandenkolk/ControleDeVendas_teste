import streamlit as st
from datetime import datetime
from utils.database import calcular_saldo_caixa, listar_transacoes_caixa, adicionar_transacao_caixa

# --- Configuração da Página ---
st.set_page_config(page_title="Controle de Caixa", page_icon="🧾")
st.title("🧾 Controle de Caixa")
st.markdown("---")

# --- Métrica de Saldo Atual ---
saldo_atual = calcular_saldo_caixa()
cor_saldo = "green" if saldo_atual >= 0 else "red"
st.header(f"Saldo Atual: :{cor_saldo}[R$ {saldo_atual:.2f}]")

st.markdown("---")

# --- Formulário de Lançamento Manual em um Expander ---
with st.expander("➕ Adicionar Novo Lançamento"):
    with st.form(key="novo_lancamento", clear_on_submit=True):
        descricao = st.text_input("Descrição*", placeholder="Ex: Pagamento da conta de luz")
        valor = st.number_input("Valor (R$)*", min_value=0.01, format="%.2f")
        tipo = st.radio("Tipo de Lançamento*", ["Entrada", "Saída"], horizontal=True)

        submit_button = st.form_submit_button("Lançar no Caixa")

        if submit_button:
            if not descricao or not valor:
                st.error("Os campos 'Descrição' e 'Valor' são obrigatórios!")
            else:
                try:
                    adicionar_transacao_caixa(descricao, tipo, valor)
                    st.success("Lançamento adicionado com sucesso!")
                    st.rerun()  # Recarrega para atualizar o saldo e a lista
                except Exception as e:
                    st.error(f"Erro ao adicionar lançamento: {e}")

st.markdown("---")

# --- Histórico de Transações (Extrato) ---
st.subheader("Histórico de Transações")
transacoes = listar_transacoes_caixa()

if not transacoes:
    st.info("Nenhuma transação registrada no caixa ainda.")
else:
    # Cabeçalho da lista
    col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
    col1.markdown("**Descrição**")
    col2.markdown("**Data**")
    col3.markdown("**Valor (R$)**")

    # Lista de transações
    for t in transacoes:
        col1, col2, col3 = st.columns([0.5, 0.3, 0.2])
        col1.text(t['descricao'])

        # Formata a data para um formato mais legível
        data_formatada = datetime.strptime(t['data_transacao'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
        col2.text(data_formatada)

        # Formatação condicional para o valor (verde para entrada, vermelho para saída)
        if t['tipo_transacao'] == 'entrada':
            col3.markdown(f":green[+ {t['valor']:.2f}]")
        else:
            col3.markdown(f":red[- {t['valor']:.2f}]")