# import streamlit as st
# from groq import Groq
# import zipfile
# import io
# import json
# import os
# from datetime import datetime

# # --- Configurações Iniciais ---
# st.set_page_config(page_title="Dev Assistant PRO", page_icon="📦", layout="wide")

# # Criar pasta de histórico se não existir
# if not os.path.exists("historico"):
#     os.makedirs("historico")

# client = Groq(api_key="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")

# # --- Lógica de Persistência ---
# def salvar_conversa(nome_arquivo, mensagens):
#     with open(f"historico/{nome_arquivo}.json", "w", encoding="utf-8") as f:
#         json.dump(mensagens, f, ensure_ascii=False, indent=4)

# def listar_conversas():
#     arquivos = [f.replace(".json", "") for f in os.listdir("historico") if f.endswith(".json")]
#     return sorted(arquivos, reverse=True)

# def gerar_titulo_ia(primeira_mensagem):
#     try:
#         # Chamada simples e rápida apenas para o título
#         res = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[{
#                 "role": "system", 
#                 "content": "Gere um título ultra-curto (máximo 5 palavras) para uma conversa que começa com o texto abaixo. Responda APENAS o título, sem aspas."
#             }, {"role": "user", "content": primeira_mensagem}],
#             max_completion_tokens=20
#         )
#         titulo = res.choices[0].message.content.strip()
#         # Limpa caracteres que o Windows não aceita em nomes de arquivos
#         for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
#             titulo = titulo.replace(char, '')
#         return titulo
#     except:
#         return "Conversa Sem Titulo"

# # --- Estado da Sessão ---
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# if "session_id" not in st.session_state:
#     st.session_state.session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# # --- Barra Lateral ---
# with st.sidebar:
#     st.title("📂 Menu")
    
#     # Gerenciamento de Histórico
#     st.subheader("📜 Conversas Salvas")
#     conversas_salvas = listar_conversas()
#     conversa_selecionada = st.selectbox("Carregar conversa antiga:", ["Nova Conversa"] + conversas_salvas)
    
#     if st.button("Carregar"):
#         if conversa_selecionada != "Nova Conversa":
#             with open(f"historico/{conversa_selecionada}.json", "r", encoding="utf-8") as f:
#                 st.session_state.messages = json.load(f)
#                 st.session_state.session_id = conversa_selecionada
#             st.rerun()

#     if st.button("➕ Nova Conversa"):
#         st.session_state.messages = []
#         st.session_state.session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         st.rerun()

#     st.divider()
    
#     # Upload de Arquivos
#     st.subheader("📁 Arquivos de Contexto")
#     uploaded_files = st.file_uploader("Suba arquivos ou um .zip", type=["zip", "py", "txt", "js", "html"], accept_multiple_files=True)
    
#     file_context = ""
#     if uploaded_files:
#         for uploaded_file in uploaded_files:
#             if uploaded_file.name.endswith('.zip'):
#                 with zipfile.ZipFile(uploaded_file, 'r') as z:
#                     for file_name in z.namelist():
#                         with z.open(file_name) as f:
#                             try:
#                                 content = f.read().decode("utf-8", errors="ignore")
#                                 file_context += f"\n--- ZIP: {file_name} ---\n{content}\n"
#                             except: continue
#             else:
#                 content = uploaded_file.read().decode("utf-8", errors="ignore")
#                 file_context += f"\n--- ARQUIVO: {uploaded_file.name} ---\n{content}\n"

# # --- Área de Chat ---
# st.title("🤖 Assistente Pessoal")

# # Exibe o histórico salvo na tela
# for message in st.session_state.messages:
#     # Ignoramos a exibição do contexto bruto para não poluir o chat
#     if "contexto_arquivos" not in message: 
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

# # if prompt := st.chat_input("Como posso ajudar no seu código?"):
# #     # 1. Adiciona a pergunta do usuário ao estado da sessão
# #     st.session_state.messages.append({"role": "user", "content": prompt})
    
# #     with st.chat_message("user"):
# #         st.markdown(prompt)

# #     with st.chat_message("assistant"):
# #         response_placeholder = st.empty()
# #         full_response = ""
        
# #         # 2. PREPARAÇÃO DO CONTEXTO COMPLETO
# #         # Criamos uma cópia das mensagens para enviar à API
# #         # Adicionamos uma mensagem de sistema no início com os arquivos (se houver)
# #         mensagens_para_enviar = [
# #             {"role": "system", "content": f"Você é um programador sênior. Contexto dos arquivos atuais:\n{file_context}"}
# #         ]
        
# #         # Adicionamos o histórico acumulado (perguntas e respostas anteriores)
# #         for m in st.session_state.messages:
# #             mensagens_para_enviar.append({"role": m["role"], "content": m["content"]})

# #         # 3. Chamada à API enviando TODO o histórico
# #         completion = client.chat.completions.create(
# #             model="groq/compound",
# #             messages=mensagens_para_enviar, # Agora enviamos a lista completa!
# #             stream=True
# #         )

# #         for chunk in completion:
# #             full_response += chunk.choices[0].delta.content or ""
# #             response_placeholder.markdown(full_response + "▌")
        
# #         response_placeholder.markdown(full_response)
        
# #         # 4. Salva a resposta da IA no histórico
# #         st.session_state.messages.append({"role": "assistant", "content": full_response})
        
# #         # Persistência no arquivo JSON
# #         salvar_conversa(st.session_state.session_id, st.session_state.messages)

# #     # Botão de download de código se houver blocos de código na resposta
# #     if "```" in full_response:
# #         st.download_button("📥 Baixar código gerado", full_response, file_name="codigo_gerado.txt")

import streamlit as st
from groq import Groq
import zipfile
import io
import json
import os
from datetime import datetime

# --- Configurações de Interface ---
st.set_page_config(page_title="Dev Assistant PRO", page_icon="🤖", layout="wide")

# Estilo personalizado para esconder ícones padrões e melhorar o visual
st.markdown("""
    <style>
    .stChatMessage { border-radius: 10px; margin-bottom: 5px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Criar pasta de histórico se não existir
if not os.path.exists("historico"):
    os.makedirs("historico")

# --- Inicialização do Cliente Groq ---
# Substitua pela sua chave ou configure no ambiente
client = Groq(api_key="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")

# --- Funções de Suporte ---

def salvar_conversa(nome_arquivo, mensagens):
    with open(f"historico/{nome_arquivo}.json", "w", encoding="utf-8") as f:
        json.dump(mensagens, f, ensure_ascii=False, indent=4)

def listar_conversas():
    arquivos = [f.replace(".json", "") for f in os.listdir("historico") if f.endswith(".json")]
    return sorted(arquivos, reverse=True)

def gerar_titulo_ia(primeira_mensagem):
    try:
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "system", 
                "content": "Sua tarefa é criar um nome de arquivo curto e limpo para a conversa. "
                           "Regras: Máximo 3 palavras, SEM markdown, SEM hashtags, SEM símbolos. "
                           "Exemplo de saída: Centralizar Div CSS"
            }, {"role": "user", "content": primeira_mensagem}],
            max_completion_tokens=15
        )
        # Limpeza de caracteres e formatação
        titulo = res.choices[0].message.content.strip()
        
        # Remove símbolos de Markdown e outros chatos
        for char in ['#', '`', '*', '_', '{', '}', '[', ']', '(', ')', '.', '!', '?']:
            titulo = titulo.replace(char, '')
            
        # Remove quebras de linha
        titulo = " ".join(titulo.split())
        
        # Remove caracteres proibidos pelo Windows
        for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
            titulo = titulo.replace(char, '')

        return titulo[:40] if titulo else "Conversa_Nova"
    except:
        return f"Conversa_{datetime.now().strftime('%H%M')}"

# --- Estado da Sessão ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"Temp_{datetime.now().strftime('%H%M%S')}"

# --- Barra Lateral ---
with st.sidebar:
    st.title("👨‍💻 Dev Central")
    
    # 1. Gerenciamento de Histórico
    st.subheader("📜 Histórico")
    conversas_salvas = listar_conversas()
    conversa_selecionada = st.selectbox("Minhas conversas:", ["Nova Conversa"] + conversas_salvas)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Carregar"):
            if conversa_selecionada != "Nova Conversa":
                with open(f"historico/{conversa_selecionada}.json", "r", encoding="utf-8") as f:
                    st.session_state.messages = json.load(f)
                    st.session_state.session_id = conversa_selecionada
                st.rerun()
    with col2:
        if st.button("➕ Limpar"):
            st.session_state.messages = []
            st.session_state.session_id = f"Temp_{datetime.now().strftime('%H%M%S')}"
            st.rerun()

    st.divider()
    
    # 2. Upload de Arquivos (Contexto)
    st.subheader("📂 Contexto do Projeto")
    uploaded_files = st.file_uploader("Upload arquivos ou ZIP", type=["zip", "py", "txt", "js", "html", "css", "json"], accept_multiple_files=True)
    
    file_context = ""
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith('.zip'):
                with zipfile.ZipFile(uploaded_file, 'r') as z:
                    for file_name in z.namelist():
                        if not file_name.endswith('/'): # Ignora pastas
                            with z.open(file_name) as f:
                                try:
                                    content = uploaded_file.read().decode("utf-8", errors="ignore")
                                    content = content[:15000] # Pega apenas os primeiros 15k caracteres (~3000 tokens)
                                    file_context += f"\n--- CAMINHO ZIP: {file_name} ---\n{content}\n"
                                except: continue
            else:
                content = uploaded_file.read().decode("utf-8", errors="ignore")
                file_context += f"\n--- ARQUIVO: {uploaded_file.name} ---\n{content}\n"
        st.success("Arquivos prontos para análise!")

# --- Área de Chat Principal ---
st.title("🤖 Assistente AI")
st.caption(f"Conversa atual: **{st.session_state.session_id}**")

# Exibição do Histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do Usuário
if prompt := st.chat_input("Como posso ajudar no seu código?"):
    
    # Se for a PRIMEIRA mensagem real, geramos um título para o arquivo
    if not st.session_state.messages:
        titulo_gerado = gerar_titulo_ia(prompt)
        # Se o arquivo já existir (por coincidência), adicionamos hora
        timestamp = datetime.now().strftime("%H%M")
        novo_id = f"{titulo_gerado}_{timestamp}"
        st.session_state.session_id = novo_id

    # 1. Adiciona a pergunta do usuário à memória
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # 2. Preparação do Contexto para a Groq
        # Enviamos as instruções de sistema + arquivos PRIMEIRO
        mensagens_para_enviar = [
            {
                "role": "system", 
                "content": f"Você é um programador sênior. Responda em Português. Utilize o contexto dos arquivos fornecidos se necessário:\n{file_context}"
            }
        ]
        
        # Incluímos TODO o histórico da conversa atual
        for m in st.session_state.messages:
            mensagens_para_enviar.append({"role": m["role"], "content": m["content"]})

        # 3. Chamada via Streaming
        try:
            completion = client.chat.completions.create(
                model="groq/compound",
                messages=mensagens_para_enviar,
                temperature=0.7,
                stream=True
            )

            for chunk in completion:
                token = chunk.choices[0].delta.content or ""
                full_response += token
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Erro na Groq: {e}")

        # 4. Finalização e Salvamento
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        salvar_conversa(st.session_state.session_id, st.session_state.messages)

    # Botão de download se houver código na resposta
    if "```" in full_response:
        st.download_button("📥 Baixar código gerado", full_response, file_name=f"codigo_{st.session_state.session_id}.txt")