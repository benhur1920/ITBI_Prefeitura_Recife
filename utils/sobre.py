import streamlit as st
import os
#from utils.totalizadores import *
from utils.marcadores import divisor

def sobre(df):
    
    
    # Imagens
    imagem_path1 = os.path.join(os.path.dirname(__file__), '..', 'images', 'fotorecife.jpeg')
    

    st.markdown("<h2 style='text-align: center; '>ITBI -  Imposto sobre Transmissão de Bens Imóveis - Recife</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Primeira seção com imagem e texto
    col1, col2 = st.columns([2, 3], gap="small")

    with col1:
        st.image(imagem_path1, use_container_width=True, clamp=True, caption="Marco zero, Recife")

    with col2:
        
        st.markdown(
            """
            <div style="text-align: justify; font-size: 17px">
                <p>
                    O Imposto sobre a Transmissão de Bens Imóveis (ITBI) é um tributo municipal cobrado na transferência de imóveis. O pagamento é condição para registrar a escritura em cartório, garantindo a efetiva mudança de propriedade.
                </p>
                <p>
                    A análise dos dados do ITBI é relevante porque:
                </p>
                <ul>
                    <li><strong>Revela a saúde do mercado imobiliário</strong></li>
                    <li><strong>Identifica áreas em expansão</strong></li>
                    <li><strong>Auxilia no planejamento urbano e econômico</strong></li>
                    <li><strong>Norteia os valores venais dos imóveis</strong></li>
                </ul>
                <p>
                    Essas informações são valiosas para corretores, investidores e gestores públicos, oferecendo um retrato claro do dinamismo do mercado imobiliário local.
                </p>
                
            </div>
            """,
        unsafe_allow_html=True
    )

def objetivo_aplicacao():
    imagem_path2 = os.path.join(os.path.dirname(__file__), '..', 'images', 'lampada.jpg')
    col1, col2 = st.columns([3, 2], gap="small")
    with col1:
        st.markdown("""
        <div contenteditable="false" style="text-align: justify; font-size: 17px;">
            <h3>PredictImóvel Recife</h3>
            <p>
                Esta ferramenta permitirá  estimar o valor venal com base em estudos estatísticos da base de dados
                do ITBI da Prefeitura do Recife.
            </p>
            <p>Os principais enfoques são:</p>
            <ul>
                <li><strong>Distribuição entre zonas e bairros da cidade</strong></li>
                <li><strong>Cálculo de medidas de tendência central e dispersão</strong></li>
                <li><strong>Consulta e exploração da base de dados</strong></li>
                <li><strong>Estimativa preditiva do valor venal utilizando técnicas de Machine Learning</strong></li>
            </ul>
            <p>
                Navegue entre as páginas e conheça os painéis das transmissões imobiliárias na cidade do Recife.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image(imagem_path2, use_container_width=True, clamp=True, caption="Boa ideia")

def mainSobre(df):
    divisor()
    sobre(df)
    divisor()
    objetivo_aplicacao()
    divisor()
