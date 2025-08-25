import pandas as pd
import statsmodels.api as sm

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

def calculo_e_exibicao_formula_reta(df):
    # Ajustar modelo de regressão linear
    X = sm.add_constant(df['Area_Construida'])
    modelo = sm.OLS(df['Valor_Avaliacao'], X).fit()
    intercepto = modelo.params['const']
    coef_area = modelo.params['Area_Construida']
    return f"Equação da Reta -> Fx = {coef_area:.2f} X + {intercepto:.2f}"

def calculo_valor_estimado_formula_reta(df):
    # Ajustar modelo de regressão linear
    X = sm.add_constant(df['Area_Construida'])
    modelo = sm.OLS(df['Valor_Avaliacao'], X).fit()
    intercepto = modelo.params['const']
    coef_area = modelo.params['Area_Construida']
    
    return coef_area, intercepto

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



def formatar_moeda_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_milhar(valor):
    if isinstance(valor, (pd.Series, list)):
        return [formatar_milhar(v) for v in valor]
    if pd.isna(valor):
        return 0
    return f"{int(valor):,}".replace(",", ".")

