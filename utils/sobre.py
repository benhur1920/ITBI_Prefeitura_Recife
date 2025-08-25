import streamlit as st
import os
#from utils.totalizadores import *
from utils.marcadores import divisor

def sobre(df):
    
    
    # Imagens
    imagem_path1 = os.path.join(os.path.dirname(__file__), '..', 'images', 'fotorecife.jpeg')
    

    st.markdown("<h2 style='text-align: center; '>ITBI</h2>", unsafe_allow_html=True)
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

  

def mainSobre(df):
    divisor()
    sobre(df)
    divisor()
