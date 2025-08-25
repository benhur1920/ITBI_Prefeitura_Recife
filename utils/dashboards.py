import matplotlib as pl
import plotly.express as px
import streamlit as st

from utils.totalizadores import calculo_total_transmisao, calculo_media , calculo_mediana, calculo_variancia, calculo_variancia_populacional, calculo_desvio, calculo_maior_valor, calculo_menor_valor, calculo_amplitude, formatar_milhar, formatar_moeda_br, calculo_correlacao, calculo_maior_area, calculo_menor_area, calculo_e_exibicao_formula_reta, calculo_valor_estimado_formula_reta
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
    fig1 = grafico_barras(df_filtrado, 'Bairro', 'Distribuição do ITBI por Bairros do Recife - Top 10', 10)
    fig2 = grafico_tree_map(df_filtrado, 'Padrao_Acabamento', 'Total de transmissões de imóveis por padrão de acabamento')
    fig3 = grafico_barras(df_filtrado, 'Tipo_Imovel', 'Distribuição do ITBI por tipo de construção', None ) 
    fig4 = grafico_rosca(df_filtrado,'Tipo_Ocupacao', 'Total de transmissões por tipo de ocupação do imóvel')
    fig5 = grafico_media_mediana_desvio(df_filtrado)
    fig6 = grafico_tree_map(df_filtrado, 'Região', 'Total de transmissões de imóveis por Região')
    fig7 = grafico_box_plot(df_filtrado)
    fig8 = grafico_correlacao_area_valor(df_filtrado)
    fig9 = grafico_mediana(df_filtrado)
    fig10 = grafico_colunas(df_filtrado_linha, 'Região', 'Valor_Avaliacao', 'Mediana do valor de transmissão por região', 6)
    fig11 = grafico_colunas(df_filtrado_linha, 'Bairro', 'Valor_Avaliacao', 'Mediana do valor de transmissão por Bairro', 10)
    

    aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs(['🏫 Geral', '📊 Medidas de tendência central', '💰 Valores médios', '🔍 Pesquisa', '📉 Regressão Linear', '💵 Valor estimado'])


    # Utilizando a aba1 para dashboards gerais e entendimento do dataframe
    with aba1:
        # Mostrando o total de transmissões e a distribuição por anos no gráfico de linhas
        col1, col2, col16 = st.columns([0.8,2,2], vertical_alignment='center', gap='small')
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
        with col16:
            # Chamando o gráfico de rosca
            st.plotly_chart(fig4, use_container_width=True, key="grafico_rosca_tipo_ocupacao")

        # Mostrando a distruibuição do total de transmissões por Região e Bairros
        col14, col15 = st.columns([2,2], vertical_alignment='center', gap='small')
        with col14:
            st.plotly_chart(fig6, use_container_width=True, key="grafico_tree_regiao")
        with col15:
            st.plotly_chart(fig1, use_container_width=True, key="grafico_barras_bairro")

        # Mostrando a distribuição por tipo de acabamento e tipo de construção
        col17, col18 = st.columns([2,2], vertical_alignment='center', gap='small')
        with col17:
            st.plotly_chart(fig2, use_container_width=True, key="grafico_tree_padrao_acabamento")
        with col18:
            st.plotly_chart(fig3, use_container_width=True, key="grafico_barras_tipo_imovel")
        
        
        
        
        

    # Mostrar os dados de media dos valores de transmissão dos imóveis com serie histórica, gráfico colunas por região e por bairros 
    with aba3:
        col19,  col20 =  st.columns(2)
        with col19:
            with st.container(border=True):
                        st.write("🏫 Mediana" )
                        st.markdown(
                            f"<p style='font-size:24px; '>{formatar_moeda_br(mediana)}</p>",
                                unsafe_allow_html=True
                            )
        with col20:
            with st.container(border=True):
                        st.write("🏫 Total transmissões" )
                        st.markdown(
                            f"<p style='font-size:24px; '>{formatar_milhar(total_transimissoes)}</p>",
                                unsafe_allow_html=True
                            )  
        # Mostrando a distribuição por tipo de acabamento e tipo de construção
        col21, col22 = st.columns([2,2], vertical_alignment='center', gap='medium')
        with col21:
            st.plotly_chart(fig9, use_container_width=True, key="grafico_mediana")
        with col22:
            st.plotly_chart(fig10, use_container_width=True, key="grafico_colunas_regiao")
        col23, col24 = st.columns([2,2], vertical_alignment='center', gap='small')
        with col23:
            st.plotly_chart(fig11, use_container_width=True, key="grafico_colunas_bairro")
        with col24:
            st.dataframe(df_filtrado)


    # Utilizando a aba2 para mostras as medidas de tendência central e grafico valor médio(média e mediana) e desvio padrão
    with aba2:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container(border=True):
                    st.write("📈 Média" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(media)}</p>",
                            unsafe_allow_html=True
                        )
        with col2:
            with st.container(border=True):
                    st.write("🎯 Mediana" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(mediana)}</p>",
                            unsafe_allow_html=True
                        )
                    
        with col3:
            with st.container(border=True):
                    st.write("🔄 Variância amostral" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(variancia)}</p>",
                            unsafe_allow_html=True
                        )
                    
        with col4:
            with st.container(border=True):
                    st.write("🔄 Variancia populacional" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(variancia_populacional)}</p>",
                            unsafe_allow_html=True
                        )
                    
        col5, col6, col7, col8, col9 = st.columns(5)
        with col5:
            with st.container(border=True):
                    st.write("🏫 Amplitude" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(amplitude)}</p>",
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
                    st.write("📊 Desvio padrão" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(desvio)}</p>",
                            unsafe_allow_html=True
                        )
                    
        with col9:
            with st.container(border=True):
                    st.write("🏫 total de transmissões filtradas" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_milhar(total_transimissoes)}</p>",
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
                    "Informe o identificador do imóvel", 
                    value=st.session_state.numero_processo
                )
                submit = st.form_submit_button("Consultar")

                if submit:
                    st.session_state.numero_processo = numero_processo_input.strip()
                    st.session_state.consultou = True
                    st.rerun() 
            
    with aba5:
        escolha = st.radio(
                "Escolha o Box Plot com ou sem Outliers",
                options=["Com Outliers", "Sem Outliers"],   # obrigatório
                captions=["Mostra todos os dados", "Remove valores extremos"],  # opcional
                horizontal=True  # <<< aqui
            )
        
        if escolha == "Com Outliers":
            col25, col26, col31 = st.columns(3)
            with col25:
               
                with st.container(border=True):
                    st.write("⬇️ Menor avaliação" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(menor_valor)}</p>",
                            unsafe_allow_html=True
                        )
                with st.container(border=True):
                        st.write("⬆️ Maior avaliação" )
                        st.markdown(
                            f"<p style='font-size:24px; '>{formatar_moeda_br(maior_valor)}</p>",
                                unsafe_allow_html=True
                            )
                with st.container(border=True):
                    st.write("🏫 Total de transmissões" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_milhar(total_transimissoes)}</p>",
                            unsafe_allow_html=True
                        )  
            with col26:
                
                with st.container(border=True):
                    st.write("📐 Equação da Reta" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{(calculo_e_exibicao_formula_reta(df_filtrado))}</p>",
                            unsafe_allow_html=True
                        )
                with st.container(border=True):
                        st.write("⬇️ Menor Área" )
                        st.markdown(
                            f"<p style='font-size:24px; '>{formatar_milhar(calculo_menor_area(df_filtrado))}</p>",
                                unsafe_allow_html=True
                            )
                with st.container(border=True):
                    st.write("⬆️ Maior Área" )
                    st.markdown(
                        f"<p style='font⬆️-size:24px; '>{formatar_milhar(calculo_maior_area(df_filtrado))}</p>",
                            unsafe_allow_html=True
                        )  
                with col31:
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
                            value=50,
                            step=1
                        )

                        # Capturando coeficiente e intercepto
                        coef_area, intercepto = calculo_valor_estimado_formula_reta(df_filtrado)

                        # Calculando o valor estimado
                        valor_estimado = coef_area * area_usuario + intercepto

                        # Exibindo resultado
                        # Container estilizado
                        st.markdown(
                            f"""
                            <div style="
                                background-color:#D6EAF8;   /* cor de fundo */
                                padding:20px;                /* espaço interno */
                                border-radius:10px;          /* cantos arredondados */
                                text-align:center;            /* centralizar texto */
                            ">
                                <h2 style="font-size:28px;">Valor Estimado:</h2>
                                <p style="font-size:32px; font-weight:bold;">R$ {valor_estimado:,.2f}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                                
            #Exibir os graficos de box plot e scatter
            st.plotly_chart(fig7, use_container_width=True, key="boxplot_com_outliers")
            st.plotly_chart(fig8, use_container_width=True, key="grafico_correlacao_area_valor_outliers_com")
            st.dataframe(df_filtrado)

        else:
            Q1 = df_filtrado['Valor_Avaliacao'].quantile(0.25)
            Q3 = df_filtrado['Valor_Avaliacao'].quantile(0.75)
            IQR = Q3 - Q1
            lim_inf = Q1 - 1.5 * IQR
            lim_sup = Q3 + 1.5 * IQR
            
            # Sem outliers
            df_sem = df_filtrado[(df_filtrado['Valor_Avaliacao'] >= lim_inf) & (df_filtrado['Valor_Avaliacao'] <= lim_sup)]

            # Exibir os cartões e o dataframe
            col29, col30, col32 = st.columns(3)
            with col29:
                maior_valor1 = calculo_maior_valor(df_sem)
                menor_valor1 = calculo_menor_valor(df_sem)
                total_transimissoes1 = calculo_total_transmisao(df_sem)
                with st.container(border=True):
                    st.write("⬇️ Menor avaliação" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_moeda_br(menor_valor1)}</p>",
                            unsafe_allow_html=True
                        )
                with st.container(border=True):
                        st.write("⬆️ Maior avaliação" )
                        st.markdown(
                            f"<p style='font-size:24px; '>{formatar_moeda_br(maior_valor1)}</p>",
                                unsafe_allow_html=True
                            )
                with st.container(border=True):
                    st.write("🏫 Total de transmissões" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_milhar(total_transimissoes1)}</p>",
                            unsafe_allow_html=True
                        )  
            with col30:
                
                with st.container(border=True):
                    st.write("📐 Equação da Reta" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{(calculo_e_exibicao_formula_reta(df_sem))}</p>",
                            unsafe_allow_html=True
                        )
                with st.container(border=True):
                        st.write("⬇️ Menor Área" )
                        st.markdown(
                            f"<p style='font-size:24px; '>{formatar_milhar(calculo_menor_area(df_sem))}</p>",
                                unsafe_allow_html=True
                            )
                with st.container(border=True):
                    st.write("⬆️ Maior Área" )
                    st.markdown(
                        f"<p style='font-size:24px; '>{formatar_milhar(calculo_maior_area(df_sem))}</p>",
                            unsafe_allow_html=True
                        )  
            with col32:
                with st.container():
                    st.markdown(
                        "<h3 style='color:black'>Informe a área construída do imóvel para estimativa de valor (m²)</h3>",
                            unsafe_allow_html=True
                     )
                        # Input do usuário
                    area_usuario = st.number_input(
                            '',
                            min_value=0,
                            max_value=100000,
                            value=50,
                            step=1
                    )

                    # Capturando coeficiente e intercepto
                    coef_area, intercepto = calculo_valor_estimado_formula_reta(df_sem)

                    # Calculando o valor estimado
                    valor_estimado = coef_area * area_usuario + intercepto

                    # Exibindo resultado
                    # Container estilizado
                    st.markdown(
                            f"""
                            <div style="
                                background-color:#D6EAF8;   /* cor de fundo */
                                padding:20px;                /* espaço interno */
                                border-radius:10px;          /* cantos arredondados */
                                text-align:center;            /* centralizar texto */
                            ">
                                <h2 style="font-size:28px;">Valor Estimado:</h2>
                                <p style="font-size:32px; font-weight:bold;">R$ {valor_estimado:,.2f}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            #Exibir os graficos de box plot e scatter
            fig12 = grafico_box_plot_sem_outleirs(df_sem)
            st.plotly_chart(fig12, use_container_width=True, key="boxplot_sem_outliers")
            fig13 = grafico_correlacao_area_valor(df_sem)
            st.plotly_chart(fig13, use_container_width=True, key="grafico_correlacao_area_valor_outliers_sem")
            st.dataframe(df_sem)
            
            # Apenas outliers
            df_out = df_filtrado[(df_filtrado['Valor_Avaliacao'] < lim_inf) | (df_filtrado['Valor_Avaliacao'] > lim_sup)]

        
    #st.dataframe(df_filtrado)

    with aba6:
        st.write("Em construção !!!")
        


def mainGraficos(df_filtrado, df_filtrado_linha):
    divisor()
    graficos(df_filtrado, df_filtrado_linha) # Passe o df_filtrado e o df_filtrado_linha para a função graficos
    divisor()