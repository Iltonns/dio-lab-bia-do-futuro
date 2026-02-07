import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Sther - Agente Financeiro",
    page_icon="💰",
    layout="centered"
)

from agente import StherAgent

# Título e Descrição
st.title("💰 Sther")
st.subheader("Sua Educadora Financeira Pessoal")

# Inicialização da Sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    # Inicializa o agente apenas uma vez
    st.session_state.agent = StherAgent()

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do Usuário
if prompt := st.chat_input("Olá! Como posso ajudar com suas finanças hoje?"):
    # Adiciona mensagem do usuário ao histórico visual
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera resposta do assistente
    with st.chat_message("assistant"):
        with st.spinner("A Sther está analisando..."):
            # Passa o histórico para o agente (excluindo a system prompt que é interna dele)
            historico_para_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            resposta = st.session_state.agent.responder(historico_para_api)
            st.markdown(resposta)
    
    # Adiciona resposta ao histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta})