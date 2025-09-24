import streamlit as st

# --- Configuração da Página ---
# st.set_page_config define as configurações da aba do navegador
st.set_page_config(
    page_title="Sistema de Controle de Loja",
    page_icon="🛒", # Você pode usar emojis como ícones
    layout="wide", # 'wide' usa mais espaço da tela
    initial_sidebar_state="expanded" # A barra lateral já começa aberta
)

# --- Título e Descrição ---
st.title("🛒 Sistema de Controle de Loja")

st.markdown("""
---
Bem-vindo ao seu sistema de gerenciamento!

Este é um protótipo para ajudar a controlar as principais operações da sua loja,
como cadastro de clientes, produtos e controle de caixa.

**👈 Utilize o menu na barra lateral para navegar entre as diferentes funcionalidades.**
""")

# --- Rodapé (opcional) ---
st.markdown("---")
st.write("Desenvolvido como um protótipo didático.")