import matplotlib as pl
import plotly.express as px
import streamlit as st
import joblib
import pandas as pd
import os
# Carregar o modelo treinado só uma vez
modelo = joblib.load("modelo_itbi.pkl")




from utils.totalizadores import calculo_total_transmisao, calculo_media , calculo_mediana, calculo_variancia, calculo_variancia_populacional, calculo_desvio, calculo_maior_valor, calculo_menor_valor, calculo_amplitude, formatar_milhar, formatar_moeda_br, calcular_correlacao, calculo_maior_area, calculo_menor_area, calculo_e_exibicao_formula_reta, calculo_valor_estimado_formula_reta, formatar_equacao_reta, calculo_mediana_area
from utils.graficos import grafico_total_licenciamentos_linha, grafico_barras, grafico_tree_map, grafico_rosca, grafico_media_mediana_desvio, grafico_box_plot, grafico_correlacao_area_valor, grafico_mediana, grafico_colunas, grafico_box_plot_sem_outleirs
from utils.marcadores import divisor
from utils.dataframe import mainDataframe

def graficos(df_filtrado, df_filtrado_linha):
    
    # Calculo das medidas de tendencia central
    media = calculo_media(df_filtrado)
    mediana = calculo_mediana(df_filtrado)
    variancia = calculo_variancia(df_filtrado)
    variancia_populacional = calculo_variancia_populacional(df_filtrado)
    desvio = calculo_desvio(df_filtrado)
    
    maior_valor = calculo_maior_valor(df_filtrado)
    menor_valor = calculo_menor_valor(df_filtrado)
    amplitude = calculo_amplitude(df_filtrado)

    # Calculo de totalizadores
    total_transimissoes = calculo_total_transmisao(df_filtrado)

    # Gráficos
    fig = grafico_total_licenciamentos_linha(df_filtrado_linha)
    fig1 = grafico_barras(df_filtrado, 'Bairro', 'Distribuição do ITBI por Bairros do Recife - Top 10', 10, "quantitativo")
    fig2 = grafico_tree_map(df_filtrado, 'Padrao_Acabamento', 'Total de transmissão de imóvel por padrão de acabamento')
    fig3 = grafico_barras(df_filtrado, 'Tipo_Imovel', 'Distribuição do ITBI por tipo de imóvel', None, "quantitativo" ) 
    fig4 = grafico_rosca(df_filtrado,'Tipo_Ocupacao', 'Total de transmissões por tipo de ocupação do imóvel')
    fig5 = grafico_media_mediana_desvio(df_filtrado)
    fig6 = grafico_tree_map(df_filtrado, 'Região', 'Total de transmissões de imóveis por Região')
    fig7 = grafico_box_plot(df_filtrado)
    fig8 = grafico_correlacao_area_valor(df_filtrado)
    fig9 = grafico_mediana(df_filtrado, 'Valor_Avaliacao', 'Mediana das avaliações de valor das transmissões' )
    fig10 = grafico_colunas(df_filtrado, 'Região', 'Valor_Avaliacao', 'Mediana do valor de transmissão por região', None, "mediana", "Blue")
    fig11 = grafico_colunas(df_filtrado, 'Bairro', 'Valor_Avaliacao', 'Mediana do valor de transmissão por Bairro -Top 10', 10, "mediana", "Blue")
    
    fig12 = grafico_barras(df_filtrado, 'Tipo_Construcao', 'Distribuição do ITBI por tipo de construção', None, 'quantitativo')


    aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs(['🏫 Geral', '📊 Medidas de tendência central', '💰 Valores médios', '🔍 Pesquisa', '📉 Regressão Linear', '💵 Valores Preditivos'])


    # Utilizando a aba1 para dashboards gerais e entendimento do dataframe
    with aba1:
        # Mostrando o total de transmissões e a distribuição por anos no gráfico de linhas
        col1, col2 = st.columns([1,3], vertical_alignment='center', gap='small')
        with col1:
            with st.container(border=True):
                st.write("🏫 Total de transmissões" )
                st.markdown(
                    f"<p style='font-size:24px; '>{formatar_milhar(total_transimissoes)}</p>",
                        unsafe_allow_html=True
                    )
        with col2:
            # Chamando o grafico de linha 
            st.plotly_chart(fig, use_container_width=True, key="grafico_linha_total_transmissoes")
        

        # Mostrando a distruibuição do total de transmissões por Região e Bairros
        col14, col15 = st.columns([2,2], vertical_alignment='center', gap='small')
        with col14:
            
            st.plotly_chart(fig1, use_container_width=True, key="grafico_barras_bairro")
        with col15:
            st.plotly_chart(fig6, use_container_width=True, key="grafico_tree_regiao")

        # Mostrando a distribuição por tipo de acabamento e tipo de construção
        col17, col18 = st.columns(2)
        with col17:
            
            st.plotly_chart(fig3, use_container_width=True, key="grafico_barras_tipo_imovel")
        with col18:
            st.plotly_chart(fig2, use_container_width=True, key="grafico_tree_padrao_acabamento")

        col16, col33 = st.columns(2)
        with col16:
            
            st.plotly_chart(fig12, use_container_width=True, key="grafico_barras_tipo_construcao")
            
        with col33:
            st.plotly_chart(fig4, use_container_width=True, key="grafico_rosca_tipo_ocupacao")
        
        
        
        

    # Mostrar os dados de media dos valores de transmissão dos imóveis com serie histórica, gráfico colunas por região e por bairros 
    with aba3:
        col19,  col20, col48 =  st.columns(3)
        with col19:
            with st.container(border=True):
                        st.write("🎯 Valor mediana da avaliação" )
                        st.markdown(
                            f"<p style='font-size:24px; '>{formatar_moeda_br(mediana)}</p>",
                                unsafe_allow_html=True
                            )
        with col20:
            with st.container(border=True):
                        st.write("🏫 Mediana da área construída m2" )
                        st.markdown(
                            f"<p style='font-size:24px; '>{formatar_milhar(calculo_mediana_area(df_filtrado))}</p>",
                                unsafe_allow_html=True
                            )  
            
        with col48:
             with st.container(border=True):
                        st.write("🏫 Total de transmissões" )
                        st.markdown(
                            f"<p style='font-size:24px; '>{formatar_milhar(total_transimissoes)}</p>",
                                unsafe_allow_html=True
                            )  
        # Mostrando a média de distribuição por tipo de acabamento e tipo de construção
        st.subheader('Analise de desempenho de valores medios dos imóveis')
        st.plotly_chart(fig9, use_container_width=True, key="grafico_mediana")

        col21, col22 = st.columns([2,2], vertical_alignment='center', gap='medium')
        with col21:
            st.plotly_chart(fig10, use_container_width=True, key="grafico_colunas_regiao")
        with col22:
            st.plotly_chart(fig11, use_container_width=True, key="grafico_colunas_bairro")

        

    # Utilizando a aba2 para mostras as medidas de tendência central e grafico valor médio(média e mediana) e desvio padrão
    with aba2:
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                    st.write("📈 Valor médio da avaliação" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(media)}</p>",
                            unsafe_allow_html=True
                        )
        with col2:
            with st.container(border=True):
                    st.write("🎯 Valor mediana da avaliação" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(mediana)}</p>",
                            unsafe_allow_html=True
                        )
                    
        with col3:
            with st.container(border=True):
                    st.write("📊 Desvio padrão da avaliação" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(desvio)}</p>",
                            unsafe_allow_html=True
                        )
                    
        
                    
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            with st.container(border=True):
                    st.write("🏫 Total de transmissões" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_milhar(total_transimissoes)}</p>",
                            unsafe_allow_html=True
                        )
        with col6:
            with st.container(border=True):
                    st.write("⬆️ Maior avaliação" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(maior_valor)}</p>",
                            unsafe_allow_html=True
                        )
                    
        with col7:
            with st.container(border=True):
                    st.write("⬇️ Menor avaliação" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(menor_valor)}</p>",
                            unsafe_allow_html=True
                        )
                    
        with col8:
            with st.container(border=True):
                    st.write("📉 Amplitude" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(amplitude)}</p>",
                            unsafe_allow_html=True
                        )
                    
        

        # Mostrando gráfico de linha contendo a série histórica da média, mediana e desvio padrão, mostrando que para analise de imóveis a melhor medida é a mediana           
        col10, col11 = st.columns([3,1], border=True)
        with col10:
            # Chamando o gráfico de linhas
            st.plotly_chart(fig5, use_container_width=True, key="grafico_media_mediana_desvio")

        with col11:
            st.markdown(
                """
                <div style="text-align: justify; font-size: 17px; padding-top: 50px; padding-bottom: 50px;">
                    <h5> Usado Mediana como medida de tendência central<h5>
                    <p>
                        A mediana é uma medida mais robusta do valor típico dos imóveis, pois não é afetada por valores muito altos ou muito baixos (outliers), ao contrário da média. Por isso, ela pode representar melhor o preço central praticado. Já a distância entre a média e o desvio padrão indica o grau de dispersão dos valores: quanto maior essa distância, maior é a variação dos preços em relação à média.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        

        
        

    with aba4:
        # Inicializa os estados da sessão
        if 'numero_processo' not in st.session_state:
            st.session_state.numero_processo = ''
        if 'consultou' not in st.session_state:
            st.session_state.consultou = False

        # Função de callback para o botão "Nova consulta"
        def reset_state():
            st.session_state.numero_processo = ''
            st.session_state.consultou = False

        # A lógica para exibir os resultados e o botão de Nova Consulta.
        if st.session_state.consultou:
            # Exibe o botão de Nova Consulta
            st.button("Nova consulta", on_click=reset_state)

            # Lógica para exibir os resultados
            num = st.session_state.numero_processo

            if num.strip() == "":
                st.warning("Digite o indice do imovel (Index)")
            elif num.isdigit():
                num = int(num)
                df_numero_processo = df_filtrado[df_filtrado['Index'] == num]

                if not df_numero_processo.empty:
                    mainDataframe(df_numero_processo)
                else:
                    st.warning("Nenhum imóvel  encontrado com esse índice.")
            else:
                st.error("Digite apenas números inteiros para o processo.")

        # Se a consulta ainda não foi feita ou foi resetada, exibe o formulário.
        else:
            with st.form(key='form_consulta'):
                numero_processo_input = st.text_input(
                    "Informe o identificador do imóvel (Index)", 
                    value=st.session_state.numero_processo
                )
                submit = st.form_submit_button("Consultar")

                if submit:
                    st.session_state.numero_processo = numero_processo_input.strip()
                    st.session_state.consultou = True
                    st.rerun() 
            
    with aba5:
        #placeholder_subheader = st.empty()
        #placeholder_dataframe = st.empty()
        escolha = st.radio(
                    "Escolha o Box Plot com ou sem Outliers",
                    options=["Com Outliers", "Sem Outliers"],   # obrigatório
                    captions=["Mostra todos os dados", "Remove valores extremos"],  # opcional
                    horizontal=True  # <<< aqui
                )
        
        total_com_outliers = df_filtrado.shape[0]
        if escolha == "Com Outliers":
            
            if df_filtrado.shape[0] >= 2:
                col40, col41, col42, col43  =  st.columns(4)
                with col40:
                    with st.container(border=True):
                            st.write("📐 Equação da Reta" )
                            st.markdown(
                                f"<p style='font-size:24px; '>{(calculo_e_exibicao_formula_reta(df_filtrado))}</p>",
                                    unsafe_allow_html=True
                                )
                with col41:
                    with st.container(border=True):
                            st.write("🔗 Correlação" )
                            st.markdown(
                                f"<p style='font-size:24px; '>{(calcular_correlacao(df_filtrado))}</p>",
                                    unsafe_allow_html=True
                                )
                with col42:
                    with st.container(border=True):
                            st.write("📏 Maior Área Construída" )
                            st.markdown(
                                f"<p style='font-size:24px; '>{(formatar_milhar(calculo_maior_area(df_filtrado)))}</p>",
                                    unsafe_allow_html=True
                                ) 
                with col43:
                    with st.container(border=True):
                            st.write("📏 Menor Área Construída" )
                            st.markdown(
                                f"<p style='font-size:24px; '>{formatar_milhar(calculo_menor_area(df_filtrado))}</p>",
                                    unsafe_allow_html=True
                                )  
                with st.container():
                        st.markdown(
                            "<h3 style='color:black'>Informe a área construída do imóvel para estimativa de valor (m²)</h3>",
                            unsafe_allow_html=True
                        )
                        # Input do usuário
                        area_usuario = st.number_input(
                            'Área construída:',
                            min_value=0,
                            max_value=100000,
                            value=0,
                            step=1
                        ) 
                valor_estimado = calculo_valor_estimado_formula_reta(df_filtrado, area_usuario)  
                st.markdown(
                                f"""
                                <div style="
                                    background-color:#D6EAF8;
                                    padding:20px;
                                    border-radius:10px;
                                    text-align:center;
                                ">
                                    <h2 style="font-size:28px;">Valor Estimado:</h2>
                                    <p style="font-size:32px; font-weight:bold;">R$ {valor_estimado:,.2f}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                st.subheader(f'Dataset Com Outliers ({df_filtrado.shape[0]})')
                st.dataframe(df_filtrado)
            else:
                st.subheader(f'Dataset Com Outliers ({df_filtrado.shape[0]})')
                st.dataframe(df_filtrado)
                st.error('Filtros selecionados não permite cálculo da reta')
        #Exibir os graficos de box plot e scatter
            st.plotly_chart(fig7, use_container_width=True, key="boxplot_com_outliers")
            st.plotly_chart(fig8, use_container_width=True, key="grafico_correlacao_area_valor_outliers_com")   
        else:
            
            Q1 = df_filtrado['Valor_Avaliacao'].quantile(0.25)
            Q3 = df_filtrado['Valor_Avaliacao'].quantile(0.75)
            IQR = Q3 - Q1
            lim_inf = Q1 - 1.5 * IQR
            lim_sup = Q3 + 1.5 * IQR
            
            # Sem outliers
            
            df_sem = df_filtrado[(df_filtrado['Valor_Avaliacao'] >= lim_inf) & (df_filtrado['Valor_Avaliacao'] <= lim_sup)]
            total_sem_outliers = df_sem.shape[0]
            if total_com_outliers > total_sem_outliers:
                st.subheader(f'Dataset Sem Outliers ({df_sem.shape[0]})')
                st.dataframe(df_sem)
            else:
                st.subheader('Dataset Sem Outliers')
                st.dataframe(df_filtrado)
            if df_sem.shape[0] >= 2:
                col44, col45, col46, col47 =  st.columns(4)
                with col44:
                    with st.container(border=True):
                            st.write("📐 Equação da Reta" )
                            st.markdown(
                                f"<p style='font-size:24px; '>{(calculo_e_exibicao_formula_reta(df_filtrado))}</p>",
                                    unsafe_allow_html=True
                                )
                with col45:
                    with st.container(border=True):
                            st.write("🔗 Correlação" )
                            st.markdown(
                                f"<p style='font-size:24px; '>{(calcular_correlacao(df_sem))}</p>",
                                    unsafe_allow_html=True
                                )

                with col46:
                    with st.container(border=True):
                            st.write("📏 Maior Área Construída" )
                            st.markdown(
                                f"<p style='font-size:24px; '>{(formatar_milhar(calculo_maior_area(df_sem)))}</p>",
                                    unsafe_allow_html=True
                                ) 
                with col47:
                    with st.container(border=True):
                            st.write("📏 Menor Área Construída" )
                            st.markdown(
                                f"<p style='font-size:24px; '>{formatar_milhar(calculo_menor_area(df_sem))}</p>",
                                    unsafe_allow_html=True
                                )   
                with st.container():
                        st.markdown(
                            "<h3 style='color:black'>Informe a área construída do imóvel para estimativa de valor (m²)</h3>",
                            unsafe_allow_html=True
                        )
                        # Input do usuário
                        area_usuario = st.number_input(
                            'Área construída:',
                            min_value=0,
                            max_value=100000,
                            value=0,
                            step=1
                        ) 
                valor_estimado = calculo_valor_estimado_formula_reta(df_sem, area_usuario)  
                st.markdown(
                                f"""
                                <div style="
                                    background-color:#D6EAF8;
                                    padding:20px;
                                    border-radius:10px;
                                    text-align:center;
                                ">
                                    <h2 style="font-size:28px;">Valor Estimado:</h2>
                                    <p style="font-size:32px; font-weight:bold;">R$ {valor_estimado:,.2f}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                
                df_outliers = df_filtrado[df_filtrado['Valor_Avaliacao'] > lim_sup]
                total_outliers = df_outliers.shape[0]
                st.subheader(f'Outliers ({total_outliers}) registros')
                st.dataframe(df_outliers)       
            else: 
                st.error('Filtros selecionados não permite cálculo da reta')
        #Exibir os graficos de box plot e scatter
            fig12 = grafico_box_plot_sem_outleirs(df_sem)
            st.plotly_chart(fig12, use_container_width=True, key="boxplot_sem_outliers")
            fig13 = grafico_correlacao_area_valor(df_sem)
            st.plotly_chart(fig13, use_container_width=True, key="grafico_correlacao_area_valor_outliers_sem")
                 

    with aba6:
        # Carregar modelo treinado
        #modelo = joblib.load("modelo_itbi.pkl")
        st.title("🏠 Predição de Valor de Imóvel - ITBI")
        st.subheader("Forneça abaixo os parametros para o modelo preditivo")
        st.write("⚠️Dados de melhor qualidade geram predições mais precisas !!!")
        col60, col61, col62 = st.columns([1,1,1])

        # Coluna 1: dados do imóvel
        with col60:
            area_terreno = st.number_input("📐 Área do Terreno (m²)", min_value=0, step=1, key="area_terreno")
            area_construida = st.number_input("🏗️ Área Construída (m²)", min_value=0, step=1, key="area_construida")
            bairro = st.selectbox("📍 Bairro", df_filtrado["Bairro"].sort_values().unique(), key="bairro")
            regiao = df_filtrado.loc[df_filtrado["Bairro"] == bairro, "Região"].iloc[0]
            #st.info(f"Zona {regiao}")

        # Coluna 2: características do imóvel
        with col61:
            padrao = st.selectbox("✨ Padrão de Acabamento", df_filtrado["Padrao_Acabamento"].sort_values().unique(), key="padrao")
            ocupacao = st.selectbox("🏢 Tipo de Ocupação", df_filtrado["Tipo_Ocupacao"].sort_values().unique(), key="ocupacao")
            construcao = st.selectbox("🏠 Tipo de Construção", df_filtrado["Tipo_Construcao"].sort_values().unique(), key="construcao")

        # Coluna 3: botão e resultado
        with col62:
            # Centralizar botão e resultado
            st.markdown("<div style='display:flex; flex-direction:column; align-items:center;'>", unsafe_allow_html=True)
            
            if st.button("🔮 Prever Valor do Imóvel"):
                entrada = pd.DataFrame([{
                    "Bairro": bairro,
                    "Padrao_Acabamento": padrao,
                    "Area_Terreno": area_terreno,
                    "Area_Construida": area_construida,
                    "Tipo_Ocupacao": ocupacao,
                    "Região": regiao,
                    "Tipo_Construcao": construcao
                }])
                pred = modelo.predict(entrada)[0]

                st.markdown(f"""
                    <div style="border:2px solid #0052cc; padding:10px; border-radius:12px; text-align:center; width:100%;">
                        <h3>💰 Valor venal estimado</h3>
                        <h2 style="color:#0052cc;">R$ {pred:,.2f}</h2>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

        
        divisor()

        col63, col64 =  st.columns([1,3])

        with col63:
    # Caminhos das imagens
            imagens = {
                "Casa": ("Casa.jpg", "Casa"),
                "Mocambo": ("Mocambo.jpg", "Casa"),
                "Galpão": ("galpao.jpg", "Galpão"),
                "Edificação Industrial": ("Industria.jpg", "Industria"),
                "Sala <= 4 Pavimentos": ("Sala.jpg", "Sala"),
                "Sala > 4 Pavimentos": ("Sala.jpg", "Sala"),
                "Edificação Garagem": ("garajem.jpg", "Garagem"),
                "Instituição Financeira": ("banco.jpg", "Instituição Financeira"),
                "Instituição Hospitalar": ("hospital.jpg", "Instituição Hospitalar"),
                "Posto de Combustível": ("Posto.jpg", "Posto de Combustível"),
                "Hotel": ("hotel.jpg", "Hotel"),
                "Apartamento <= 4 Pavimentos": ("Apartamento.jpg", "Apartamento"),
                "Apartamento > 4 Pavimentos": ("Apartamento.jpg", "Apartamento"),
                "Edificação Especial": ("Apartamento.jpg", "Apartamento"),
                "Loja <= 4 Pavimentos": ("Loja.jpg", "Loja"),
                "Loja > 4 Pavimentos": ("Loja.jpg", "Loja"),
            }

            # Verifica se o tipo de construção existe no dicionário
            if construcao in imagens:
                img_file, legenda = imagens[construcao]
                img_path = os.path.join(os.path.dirname(__file__), '..', 'images', img_file)
                st.image(img_path, caption=legenda)

        with col64:         
            st.markdown(
                """
                <div style="text-align: justify; font-size: 17px">
                    <h3>Nota</h3>
                        <p>
                            É importante destacar que o valor venal registrado no ITBI não representa, necessariamente, o valor de mercado de cada imóvel. Os dados refletem o valor declarado para fins tributários e não capturam aspectos qualitativos, como estado de conservação, reformas, localização exata na rua, vizinhança ou fatores subjetivos de valorização. Portanto, os modelos baseados nesses registros oferecem uma referência estatística de preços, mas não substituem uma avaliação individual ou comercial realizada em campo.
                        </p>
                                                        
                </div>
                    """,
                unsafe_allow_html=True
                )
def mainGraficos(df_filtrado, df_filtrado_linha):
    divisor()
    graficos(df_filtrado, df_filtrado_linha) # Passe o df_filtrado e o df_filtrado_linha para a função graficos
    divisor()