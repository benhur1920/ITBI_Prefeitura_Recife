import pandas as pd
import statsmodels.api as sm
import streamlit as st

# Calculo dos totalizadores
def calculo_total_transmisao(df_filtrado):
    total_df = df_filtrado['Data_Transacao'].count()
    #total_df = formatar_milhar(total_df)
    return total_df


# Calculando os indicadores gerais para o ano de 2025

def calculo_media(df_filtrado):
    media =  df_filtrado['Valor_Avaliacao'].mean()
    #media = formatar_moeda_br(media)
    return media

def calculo_mediana(df_filtrado):
    mediana =  df_filtrado['Valor_Avaliacao'].median()
    #mediana = formatar_moeda_br(mediana)
    return mediana

def calculo_variancia(df_filtrado):
    variancia =  df_filtrado['Valor_Avaliacao'].var()
    #variancia = formatar_moeda_br(variancia)
    return variancia

def calculo_desvio(df_filtrado):
    desvio =  df_filtrado['Valor_Avaliacao'].std()
    #desvio = formatar_moeda_br(desvio)
    return desvio

def calculo_variancia_populacional(df_filtrado):
    variancia_populacional =  df_filtrado['Valor_Avaliacao'].var(ddof=0)
    #variancia_populacional = formatar_moeda_br(variancia_populacional)
    return variancia_populacional


def calculo_maior_valor(df_filtrado):
    maior_valor =  df_filtrado['Valor_Avaliacao'].max()
    #maior_valor = formatar_moeda_br(maior_valor)
    return maior_valor

def calculo_menor_valor(df_filtrado):
    menor_valor =  df_filtrado['Valor_Avaliacao'].min()
    #menor_valor = formatar_moeda_br(menor_valor)
    return menor_valor

def calculo_amplitude(df_filtrado):
    amplitude = df_filtrado['Valor_Avaliacao'].max() - df_filtrado['Valor_Avaliacao'].min()
    #amplitude = formatar_moeda_br(amplitude)
    return amplitude

def calculo_correlacao(df):
    return df['Area_Construida'].corr(df['Valor_Avaliacao'])

def calculo_menor_area(df):
    return df['Area_Construida'].min()

def calculo_maior_area(df):
    return df['Area_Construida'].max()

# Para calculo da reta, devemos levar em consideração: o df_filtrado é menor que 2, o valor do resultado é negativo.
def calculo_e_exibicao_formula_reta(df):
    # ✅ Conta quantos imóveis existem
    cont = df.shape[0]

    # Se houver menos de 2 imóveis, não é possível calcular reta
    if cont < 2:
        return "⚠️ Quantidade de imóveis insuficiente para cálculo da reta."

    try:
        # Ajusta modelo de regressão linear
        X = sm.add_constant(df['Area_Construida'], has_constant='add')
        modelo = sm.OLS(df['Valor_Avaliacao'], X).fit()

        # Coeficientes seguros
        intercepto = modelo.params.get("const", modelo.params.iloc[0])
        coef_area = modelo.params.get("Area_Construida", modelo.params.iloc[-1])

        # Se valores negativos, não faz sentido
        #if coef_area < 0 or intercepto < 0:
            #return "⚠️ Valores negativos –. Os filtros selecionados retornam valores negativos e não interessam"

        # Retorna equação formatada
        texto = formatar_equacao_reta(coef_area, intercepto)
        return texto

    except Exception as e:
        return f"Erro ao calcular a reta: {e}"

def calculo_valor_estimado_formula_reta(df, area):
    # Prepara X e y
    X = sm.add_constant(df['Area_Construida'], has_constant='add')
    y = df['Valor_Avaliacao']

    # Ajusta o modelo de regressão linear
    modelo = sm.OLS(y, X).fit()

    # Coeficientes
    intercepto = modelo.params.get("const", modelo.params.iloc[0])
    coef_area = modelo.params.get("Area_Construida", modelo.params.iloc[-1])

    # Valor estimado para a área informada
    valor_estimado = intercepto + coef_area * area

    return valor_estimado

def calcular_correlacao(df):
    corr = df['Area_Construida'].corr(df['Valor_Avaliacao'])
    # Retorna como float arredondado
    return round(corr, 3)

def formatar_equacao_reta(coef_area, intercepto):
    if intercepto < 0:
        return f"y = {coef_area:,.2f} x - {abs(intercepto):,.2f}"
    else:
        return f"y = {coef_area:,.2f} x + {intercepto:,.2f}"

"""
mediana = df[df['ano'] == 2025]['valor_avaliacao'].median()
desvio = df[df['ano'] == 2025]['valor_avaliacao'].std()
variancia = df[df['ano'] == 2025]['valor_avaliacao'].var()
variancia_populacional = df[df['ano'] == 2025]['valor_avaliacao'].var(ddof=0)
valoresdistintos = df[df['ano'] == 2025]['valor_avaliacao'].value_counts()
maior = df[df['ano'] == 2025]['valor_avaliacao'].max()
menor = df[df['ano'] == 2025]['valor_avaliacao'].min()
amplitude_2025 = maior - menor

"""

# Funcoes de formatacao

def formatar_moeda_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_milhar(valor):
    if isinstance(valor, (pd.Series, list)):
        return [formatar_milhar(v) for v in valor]
    if pd.isna(valor):
        return 0
    return f"{int(valor):,}".replace(",", ".")

def formatar_equacao(coef, intercepto):
    # Usa ponto decimal para float e vírgula para milhar
    coef_str = f"{coef:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    intercepto_str = f"{abs(intercepto):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    # Ajusta sinal do intercepto
    sinal = "+" if intercepto >= 0 else "-"
    
    return f"Fx = {coef_str} × Área {sinal} {intercepto_str}"