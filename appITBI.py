import sys
import os
print("Python sys.path:", sys.path)
print("Current dir:", os.getcwd())
import pandas as pd
import streamlit as st
from datetime import date
from streamlit_option_menu import option_menu



# ----------------------------
# Ajusta path para encontrar utils
# ----------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))

# Agora importa os módulos da pasta utils
from utils import sobre, dataframe, dashboards


# ----------------------------
# Configuração da página. Fica sempre no início do projeto
# ----------------------------
st.set_page_config(
    layout="wide",
    page_title="ITBI"
)

# ----------------------------
# Inicialização dos filtros globais
# ----------------------------
filtros_iniciais = ['Ano', 'Mes', 'Região', 'Bairro', 'Tipo_Imovel', 'Tipo_Ocupacao', 'Tipo_Construcao']
for filtro in filtros_iniciais:
    chave = f'main_filtro_{filtro}'
    if chave not in st.session_state:
        st.session_state[chave] = []


# ----------------------------
# Caminho do arquivo
# ----------------------------
CAMINHO_ARQUIVO_ORIGINAL = "dados/ITBI.parquet"

# ----------------------------
# Data atual
# ----------------------------
hoje = date.today()

# ----------------------------
# Função para carregar arquivo Parquet
# ----------------------------
@st.cache_data
def carregar_arquivo_parquet():
    try:
        return pd.read_parquet(CAMINHO_ARQUIVO_ORIGINAL, engine='pyarrow')
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return pd.DataFrame()  # retorna dataframe vazio para evitar crash

df = carregar_arquivo_parquet()

# ----------------------------
# Cópia do DataFrame original
# ----------------------------
df_filtrado = df.copy()

# Última e primeira data
ultima_data = df['Data_Transacao'].max().strftime("%d/%m/%Y") if not df.empty else None
primeira_data = df['Data_Transacao'].min().strftime("%d/%m/%Y") if not df.empty else None

# ----------------------------
# Função do título da página
# ----------------------------
def titulo_pagina():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            "<h1>ITBI - Imposto sobre Tramissão de Bens Imóvies - Recife</h1>"
            "<p>Fonte: Dados abertos da Prefeitura do Recife</p>"
            f"<p>Perído: {primeira_data} a {ultima_data}</p>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div style="margin-top: 40px;">
                <a href="http://dados.recife.pe.gov.br/dataset?q=itbi&sort=score+desc%2C+metadata_modified+desc" 
                   target="_blank" class="botao-link">
                    🔗 Acessar fonte dos dados
                </a>
            </div>
            """, unsafe_allow_html=True
        )
        st.write(f"📅 Data: {hoje.strftime('%d/%m/%Y')}")

# ----------------------------
# Funções de filtro
# ----------------------------

def filtros_aplicados(df, nome_do_filtro):
    chave = f'main_filtro_{nome_do_filtro}'
    
    # Inicializa o session_state caso ainda não exista
    if chave not in st.session_state:
        st.session_state[chave] = []

    # Widget Multiselect
    filtro_opcao = st.multiselect(
        f'Selecione {nome_do_filtro}',
        options=sorted(df[nome_do_filtro].dropna().unique()),
        default=st.session_state[chave],
        key=chave
    )
    
    # Atualiza o session_state automaticamente (Streamlit faz isso ao usar key)
    # Apenas filtra os dados com base no valor atual
    return df[df[nome_do_filtro].isin(st.session_state[chave])] if st.session_state[chave] else df


def filtro_mes_nome(df):
    meses_ordenados = {
        'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4,
        'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8,
        'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12
    }
    
    chave = 'main_filtro_mes'
    
    if chave not in st.session_state:
        st.session_state[chave] = []

    opcoes_disponiveis = sorted(
        df['Mes'].dropna().unique(),
        key=lambda x: meses_ordenados.get(x, 99)
    )

    filtro_opcao = st.multiselect(
        'Selecione o Mês',
        options=opcoes_disponiveis,
        default=st.session_state[chave],
        key=chave
    )
    
    return df[df['Mes'].isin(st.session_state[chave])] if st.session_state[chave] else df


# ----------------------------
# Função principal de navegação e filtros
# ----------------------------
def criacao_navegacao_e_filtros():
    df_filtrado = df.copy()

    with st.sidebar:
        selected = option_menu(
            menu_title="Conheça",
            options=["Sobre", "Dashboards", "Dataframe"],
            icons=["info-circle", "bar-chart", "table"],
            menu_icon="cast",
            default_index=0
        )
        st.markdown("<h1>Filtros</h1>", unsafe_allow_html=True)
        df_filtrado = filtros_aplicados(df_filtrado, 'Ano')
        df_filtrado = filtro_mes_nome(df_filtrado)
        df_filtrado = filtros_aplicados(df_filtrado, 'Região')
        df_filtrado = filtros_aplicados(df_filtrado, 'Bairro')
        df_filtrado = filtros_aplicados(df_filtrado, 'Tipo_Imovel')
        df_filtrado = filtros_aplicados(df_filtrado, 'Tipo_Ocupacao')
        df_filtrado = filtros_aplicados(df_filtrado, 'Tipo_Construcao')

    # DataFrame para gráfico de linha
    df_filtrado_linha = df.copy()
    for col in ['Tipo_Imovel','Tipo_Ocupacao','Região','Bairro']:
        key = f'main_filtro_{col}'
        if key in st.session_state and st.session_state[key]:
            df_filtrado_linha = df_filtrado_linha[df_filtrado_linha[col].isin(st.session_state[key])]

    totalLinhas = df_filtrado.shape[0]

    # Conteúdo principal
    if selected == "Sobre":
        sobre.mainSobre(totalLinhas)
    elif selected == "Dashboards":
        df_filtrado_linha['Ano'] = df_filtrado_linha['Ano'].astype(str)
        dashboards.mainGraficos(df_filtrado, df_filtrado_linha)
    else:
        dataframe.mainDataframe(df_filtrado)

# ----------------------------
# Função main
# ----------------------------
def main():
    titulo_pagina()
    criacao_navegacao_e_filtros()

# ----------------------------
# Executa o app
# ----------------------------
if __name__ == '__main__':
    main()
