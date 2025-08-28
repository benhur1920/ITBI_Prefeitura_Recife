import matplotlib as pl
import plotly.express as px
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import plotly.graph_objects as go

from utils.marcadores import texto, sidebar
from utils.totalizadores import formatar_moeda_br, formatar_milhar

import plotly.express as px

def grafico_total_licenciamentos_linha(df):
    # agrupar por ano e contar transmissões
    df_agrupado = df.groupby("Ano").size().reset_index(name="Total_Transmissoes")

    # criar gráfico
    fig = px.line(
        df_agrupado,
        x="Ano",
        y="Total_Transmissoes",
        markers=True,  # adiciona bolinhas nos pontos
        labels={"Ano": "Ano", "Total_Transmissoes": "Total de Transmissões"},
        title="Total de Transmissões por Ano"
    )
    fig.update_layout(
        title={'text': 'Total de Transmissões por Ano',   'font': {'size': 26}}
    )
    return fig

# Gráfico de barras
def grafico_barras(df, nome_coluna, titulo_grafico, top_n, tipo_calculo, coluna_valor=None):
    
    if tipo_calculo == 'quantitativo':
        # contar registros por categoria
        df_bairro = (
            df.groupby(nome_coluna).size()
            .reset_index(name='TOTAL')
            .sort_values('TOTAL', ascending=False)
            .head(top_n)
        )

        # aplicar formatação de milhar
        df_bairro["VALOR_FORMATADO"] = formatar_milhar(df_bairro["TOTAL"])

        fig1 = px.bar(
            df_bairro,
            x=nome_coluna,
            y="TOTAL",
            text="VALOR_FORMATADO",
            color="TOTAL",
            color_continuous_scale="Blues"
        )

        fig1.update_layout(
            title={'text': titulo_grafico, 'font': {'size': 26}},
            xaxis_title=nome_coluna,
            yaxis_title="Total"
        )

    else:
        if coluna_valor is None:
            raise ValueError("Precisa informar `coluna_valor` para calcular mediana ou valor.")

        # calcular mediana por categoria
        df_bairro = (
            df.groupby(nome_coluna)[coluna_valor]
            .median()
            .reset_index(name='TOTAL')
            .sort_values('TOTAL', ascending=False)
            .head(top_n)
        )

        # aplicar formatação de moeda
        df_bairro["VALOR_FORMATADO"] = df_bairro["TOTAL"].apply(formatar_moeda_br)

        fig1 = px.bar(
            df_bairro,
            x=nome_coluna,
            y="TOTAL",
            text="VALOR_FORMATADO",
            color="TOTAL",
            color_continuous_scale="Blues"
        )

        fig1.update_layout(
            title={'text': titulo_grafico, 'font': {'size': 26}},
            xaxis_title=nome_coluna,
            yaxis_title="Mediana"
        )

    # configuração comum
    fig1.update_traces(textposition="outside")
    fig1.update_coloraxes(showscale=False)
    return fig1
    
# Grafico tree map
def grafico_tree_map(df, nome_coluna, titulo_grafico):
    
    # Padrão geral
    df_agrupado = df.groupby(nome_coluna).size().reset_index(name='TOTAL').sort_values('TOTAL', ascending=False)
    fig2 = px.treemap(df_agrupado, path=[nome_coluna], values='TOTAL', color=nome_coluna,  color_discrete_sequence=px.colors.sequential.Blues)

    fig2.update_layout(
        title={
            'text': titulo_grafico,
            'font': {'size': 26}
        },
        
    )
    # mostrar nome + valor dentro dos quadrados
    fig2.update_traces(
        texttemplate="%{label}<br>%{value:.}",   # usa vírgula padrão
        textinfo="text+label+value"
    )
    
    
    return fig2

# Gráfico rosca
def grafico_rosca(df, nome_coluna, titulo_grafico):
    
    # Agrupar por tipo de coupacao
    df_situacao = (
        df.groupby(nome_coluna)
        .size()
        .reset_index(name='TOTAL')
        .sort_values('TOTAL', ascending=False)
    )

    # Gráfico de rosca
    fig = px.pie(
        df_situacao,
        values='TOTAL',
        names=nome_coluna,
        hole=0.5,
        color_discrete_sequence=['#1f4e79', '#769fd0']
    )

    fig.update_layout(
    title={'text': titulo_grafico, 'font': {'size': 26}},
    font=dict(color=texto),
    legend_title=dict(text=nome_coluna, font=dict(size=20)),
    legend=dict(font=dict(size=16)),
)
    return fig

# grafico de linha com media, media e desvio
def grafico_media_mediana_desvio(df):
    # garantir que a coluna seja datetime
    df["Data_Transacao"] = pd.to_datetime(df["Data_Transacao"])

    # agrupar por ano e mês
    df["AnoMes"] = df["Data_Transacao"].dt.to_period("M").astype(str)

    df_stats = df.groupby("AnoMes")["Valor_Avaliacao"].agg(
        Média="mean",
        Mediana="median",
        Desvio="std"
    ).reset_index()

    # transformar em formato longo para plotly
    df_melt = df_stats.melt(
        id_vars="AnoMes",
        value_vars=["Média", "Mediana", "Desvio"],
        var_name="Métrica",
        value_name="Valor"
    )

    # criar gráfico de linha
    fig = px.line(
        df_melt,
        x="AnoMes",
        y="Valor",
        color="Métrica",
        markers=True,
        labels={"AnoMes": "Período", "Valor": "Valor da Avaliação"},
        title="Média, Mediana e Desvio Padrão por Mês"
    )

    fig.update_layout(
        title={'text': 'Média, Mediana e Desvio Padrão por Mês', 'font': {'size': 22}},
        xaxis_tickangle=-45
    )

    return fig

# Criar boxplot Com outilers
def grafico_box_plot(df):
    fig = px.box(
        df,
        x="Valor_Avaliacao",   # ajuste para o nome correto da sua coluna
        title="Boxplot do Valor de Avaliação Com Outliers"
        
    )
    fig.update_layout(
        xaxis_title="Valor de Avaliação (R$)",
        yaxis_title=""
    )
    return fig

# Criar boxplot SEM outilers
def grafico_box_plot_sem_outleirs(df):
    fig = px.box(
        df,
        x="Valor_Avaliacao",   # ajuste para o nome correto da sua coluna
        title="Boxplot do Valor de Avaliação Sem Outliers",
        points=False
    )
    fig.update_layout(
        xaxis_title="Valor de Avaliação (R$)",
        yaxis_title=""
    )
    return fig





# Grafico scatter 
def grafico_correlacao_area_valor(df):
    # Calcular a correlação de Pearson
    correlacao = df['Area_Construida'].corr(df['Valor_Avaliacao'])

    # Ajustar modelo de regressão linear
    X = sm.add_constant(df['Area_Construida'])
    modelo = sm.OLS(df['Valor_Avaliacao'], X).fit()
    # intercepto e coeficiente de forma segura
    intercepto = modelo.params.get("const", modelo.params.iloc[0])
    coef_area = modelo.params.get("Area_Construida", modelo.params.iloc[-1])

    # Criar scatter plot
    fig = px.scatter(
        df,
        x="Area_Construida",
        y="Valor_Avaliacao",
        labels={
            "Area_Construida": "Área Construída (m²)",
            "Valor_Avaliacao": "Valor de Avaliação (R$)"
        },
        title=f"Correlação entre Área Construída e Valor de Avaliação (R = {correlacao:.2f})",
        hover_data={"Area_Construida": True, "Valor_Avaliacao": True}
    )

    # Adiciona a reta de regressão manualmente usando go.Scatter
    x_range = np.linspace(df['Area_Construida'].min(), df['Area_Construida'].max(), 100)
    y_range = intercepto + coef_area * x_range
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=y_range,
            mode='lines',
            name='Reta de regressão',
            line=dict(color='red')
        )
    )

    # Adiciona a equação da reta como anotação
    """
    fig.add_annotation(
        x=df['Area_Construida'].max() * 0.6,
        y=df['Valor_Avaliacao'].max() * 0.9,
        text=f"Equação da Reta -> Fx = {coef_area:.2f} X + {intercepto:.2f}" ,
        showarrow=False,
        font=dict(color="blue", size=18)
    )
    """
    fig.update_traces(marker=dict(size=6, opacity=0.6))

    return fig

def grafico_mediana(df, valor_coluna, titulo):
    # garantir que a coluna seja datetime
    df["Data_Transacao"] = pd.to_datetime(df["Data_Transacao"])

    # agrupar por ano e mês
    df["AnoMes"] = df["Data_Transacao"].dt.to_period("M").astype(str)

    # calcular a mediana
    df_stats = df.groupby("AnoMes")[valor_coluna].agg(
        Valor="median"
    ).reset_index()

    # criar gráfico de linha
    fig = px.line(
        df_stats,
        x="AnoMes",
        y="Valor",
        markers=True,
        labels={"AnoMes": "Período", "Valor": "Valor da Avaliação"},
        title=titulo
    )
    fig.update_layout(
        title={'text': titulo, 'font': {'size': 22}},
        xaxis_tickangle=-45
    )

    return fig

# Gráfico de colunas - Atenção colocar a orientacao para H para ter efeito horizontal nas barras

# Gráfico de colunas horizontal
def grafico_colunas(df, coluna_principal, coluna_valor, titulo_grafico, top_n, tipo_calculado, cor):
    
    if tipo_calculado != 'quantitativo':
        if coluna_valor is None:
            raise ValueError("Precisa informar `coluna_valor` para calcular mediana ou valor.")

        # calcular mediana
        df_stats = df.groupby(coluna_principal)[coluna_valor].median().reset_index()

        # ordenar do maior para o menor e pegar os top_n
        df_stats = df_stats.sort_values(coluna_valor, ascending=False).head(top_n)

        # aplicar formatação de moeda
        df_stats["VALOR_FORMATADO"] = df_stats[coluna_valor].apply(formatar_moeda_br)

        # gráfico horizontal
        fig = px.bar(
            df_stats,
            x=coluna_valor,
            y=coluna_principal,
            orientation="h",
            text="VALOR_FORMATADO",
            color=coluna_valor,
            color_continuous_scale="Blues"
        )

        y_title = "Mediana"

    else:
        # calcular contagem de registros
        df_stats = df.groupby(coluna_principal).size().reset_index(name="TOTAL")
        df_stats = df_stats.sort_values("TOTAL", ascending=False).head(top_n)

        # aplicar formatação de milhar
        df_stats["VALOR_FORMATADO"] = df_stats["TOTAL"].apply(formatar_milhar)

        # gráfico horizontal
        fig = px.bar(
            df_stats,
            x="TOTAL",
            y=coluna_principal,
            orientation="h",
            text="VALOR_FORMATADO",
            color="TOTAL",
            color_continuous_scale="Blues"
        )

        y_title = "Total"

    # layout comum
    fig.update_traces(textposition="inside", insidetextanchor="middle")
    fig.update_layout(
        title={'text': titulo_grafico, 'font': {'size': 22}},
        height=400,
        showlegend=False,
        yaxis=dict(categoryorder="total ascending"),  # maiores valores no topo
        yaxis_title=y_title
    )

    fig.update_coloraxes(showscale=False)
    return fig
