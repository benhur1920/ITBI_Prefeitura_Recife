import pandas as pd


def entrada_de_dados_de_2021_a_2025():
    mensagem("Iniciando leitura dos arquivos no site e baixando os datasets")
    
    urls = {
        2021: 'http://dados.recife.pe.gov.br/dataset/28e3e25e-a9a7-4a9f-90a8-bb02d09cbc18/resource/1db559c3-ffcb-451f-a7f2-84d1165256bd/download/itbi_2021.csv',
        2022: 'http://dados.recife.pe.gov.br/dataset/28e3e25e-a9a7-4a9f-90a8-bb02d09cbc18/resource/1c22cb35-8ce8-42f0-b631-2c66ea1edaa3/download/itbi_2022.csv',
        2023: 'http://dados.recife.pe.gov.br/dataset/28e3e25e-a9a7-4a9f-90a8-bb02d09cbc18/resource/a01e3b82-055b-4139-b495-e54ec5196f54/download/itbi_2023.csv',
        2024: 'http://dados.recife.pe.gov.br/dataset/28e3e25e-a9a7-4a9f-90a8-bb02d09cbc18/resource/c3feb7bb-4a76-4ddf-becb-ea77f66c23d0/download/itbi_2024.csv',
        2025: 'http://dados.recife.pe.gov.br/dataset/28e3e25e-a9a7-4a9f-90a8-bb02d09cbc18/resource/97bbfc62-efb2-493f-9631-09eb05f980d7/download/itbi_2025.csv'
    }

    dfs = []
    for ano, url in urls.items():
        try:
            df_temp = pd.read_csv(url, sep=';', encoding='utf-8', decimal=",")
            mensagem(f"Arquivo {ano} lido com sucesso! {df_temp.shape[0]} linhas.")
            dfs.append(df_temp)
        except Exception as e:
            mensagem(f"Erro ao ler o arquivo de {ano}: {e}")

    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        mensagem(f"Todos os arquivos foram concatenados. Total de linhas: {df.shape[0]}")
        return df
    else:
        mensagem("Nenhum arquivo pôde ser lido.")
        return pd.DataFrame()  

def excluir_colunas_sem_interesse(df):
    colunas_para_remover = ['cidade', 'uf', 'sfh', 'cod_logradouro', 'fracao_ideal', 'cod_logradouro', 'latitude', 'longitude', 'Distrito' ]
    df.drop(columns=colunas_para_remover, inplace=True)
    return df

def criar_coluna_identificador(df):
    df = df.reset_index()
    return df


def aplicar_title_nomes_colunas(df):
    # Aplica .title() em cada nome de coluna
    df.columns = [col.title() for col in df.columns]
    
    return df

# --------------------------------------------------------------------
# Iniciando tratamento da coluna Bairro
# --------------------------------------------------------------------

def transformar_para_caixa_baixa(df):
    mensagem("Trantando os dados da coluna Bairro!!!")
    df['Bairro'] = df['Bairro'].str.lower()
    return df

def remover_espaços_em_branco_extras(df):
    df['Bairro'] = df['Bairro'].str.strip()
    return df

def padronizar_nomes_dos_bairros(df):
    substituicoes = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ã': 'a', 'õ': 'o', 'â':'a','ç':'c', 'ô':'o', 'ê':'e' , 'Á':'A'}
    # Aplicando as substituições
    df['Bairro'] = df['Bairro'].replace(substituicoes, regex=True)
    return df

def renomeando_bairro(df):
    df['Bairro'] = df['Bairro'].replace({'cohab   ibura': 'ibura'})
    return df

def aplicar_title(df):
    colunas = ["Logradouro", "Complemento", "Bairro", "Tipo_Ocupacao"]
    for col in colunas:
        if col in df.columns:  # garante que a coluna existe
            df[col] = df[col].astype(str).str.title()
    return df

# --------------------------------------------------------------------
# Criar a  coluna Região
# --------------------------------------------------------------------
def criar_a_coluna_Regiao(df):
    dicionario = {
        'Centro': [
            'Boa Vista', 'Cabanga', 'Coelhos', 'Ilha Do Leite', 'Ilha Joana Bezerra',
            'Paissandu', 'Recife', 'Santo Amaro', 'Santo Antônio', 'Santo Antonio',
            'Soledade', 'São José', 'Sao Jose'
        ],
        'Noroeste': [
            'Aflitos', 'Alto Do Mandu', 'Alto José Bonifácio', 'Alto Jose Bonifacio',
            'Alto José Do Pinho','Alto Jose Do Pinho', 'Apipucos', 'Brejo Da Guabiraba',
            'Brejo De Beberibe', 'Casa Amarela', 'Casa Forte', 'Córrego Do Jenipapo',
            'Corrego Do Jenipapo', 'Derby', 'Dois Irmãos','Dois Irmaos' , 'Espinheiro',
            'Graças', 'Gracas', 'Guabiraba', 'Jaqueira', 'Macaxeira', 'Mangabeira',
            'Monteiro', 'Morro Da Conceição','Morro Da Conceicao', 'Nova Descoberta',
            'Parnamirim', 'Passarinho', 'Pau Ferro', 'Poço', 'Poco', 'Santana',
            'Sítio Dos Pintos','Sitio Dos Pintos' ,'Tamarineira', 'Vasco Da Gama'
        ],
        'Norte': [
            'Alto Santa Terezinha', 'Arruda', 'Beberibe', 'Bomba Do Hemetério',
            'Bomba Do Hemeterio', 'Cajueiro', 'Campina Do Barreto', 'Campo Grande',
            'Dois Unidos', 'Encruzilhada', 'Fundão', 'Fundao', 'Hipódromo','Hipodromo',
            'Linha Do Tiro', 'Peixinhos', 'Ponto De Parada', 'Porto Da Madeira',
            'Rosarinho', 'Torreão', 'Torreao', 'Água Fria', 'Agua Fria'
        ],
        'Oeste': [
            'Caxangá', 'Caxanga', 'Cidade Universitária', 'Cidade Universitaria',
            'Cordeiro', 'Engenho Do Meio', 'Ilha Do Retiro', 'Iputinga', 'Madalena',
            'Prado', 'Torre', 'Torrões','Torroes', 'Várzea', 'Varzea', 'Zumbi'
        ],
        'Sudeste': [
            'Afogados', 'Areias', 'Barro', 'Bongi', 'Caçote', 'Cacote', 'Coqueiral',
            'Curado', 'Estância', 'Estancia', 'Jardim São Paulo', 'Jardim Sao Paulo',
            'Jiquiá', 'Jiquia', 'Mangueira', 'Mustardinha', 'San Martin', 'Sancho',
            'Tejipió','Tejipio', 'Totó', 'Toto'
        ],
        'Sul': [
            'Boa Viagem', 'Brasília Teimosa', 'Brasilia Teimosa', 'Cohab', 'Ibura',
            'Imbiribeira', 'Ipsep', 'Jordão', 'Jordao', 'Pina'
        ]
    }

    def buscar_regiao(bairro):
        for regiao, bairros in dicionario.items():
            if bairro in bairros:
                return regiao
        return 'Não informado'  # caso não encontre

    df['Região'] = df['Bairro'].apply(buscar_regiao)
    return df

# --------------------------------------------------------------------
# Alterando valores da coluna tipo de ocupacao
# --------------------------------------------------------------------

def substituir_os_valores_da_coluna_tipo_ocupacao_pardronizar(df):
    df['Tipo_Ocupacao'] = df['Tipo_Ocupacao'].replace({
        'Comercial Com Lixo Organico': 'Comercial',
        'Comercial Sem Lixo Organico': 'Comercial'
    })
    return df

# --------------------------------------------------------------------
# Criar as colunas de ano e mes
# --------------------------------------------------------------------

def criar_coluna_ano(df):
    df['Data_Transacao'] = pd.to_datetime(df['Data_Transacao'])
    df['Ano'] = df['Data_Transacao'].dt.year
    return df

def criar_coluna_mes(df):
    meses = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    df['Mes'] = df['Data_Transacao'].dt.month.map(meses)
    return df

def converter_coluna_valor_avaliacao(df):
    df['Valor_Avaliacao'] = pd.to_numeric(df['Valor_Avaliacao'], errors='coerce').fillna(0).astype(int)
    return df

def Salvar_o_DataFrame_em_arquivo_CSV_e_Json(df):
    mensagem("Salvando os arquivos !!! Até o próximos mes !!!!!")
    #df.to_csv(r'C:\Users\Ben-Hur\OneDrive\Desktop\Projeto Prefeitura\Arquivos Fontes\saida\ITBI.csv', sep=';',encoding='utf-8-sig', index=False)
    df.to_parquet(r'dados/ITBI.parquet', engine='pyarrow',   index=False)
    df.to_csv(r"dados/ITBI.csv", sep=";", encoding="utf-8-sig", index=False)
    # df.to_json('ITBI.json', orient='records', force_ascii=False, indent=4)

def mensagem(mensagem):
    print("\n", mensagem)


def main():
    df = entrada_de_dados_de_2021_a_2025()
    df = excluir_colunas_sem_interesse(df)
    df = criar_coluna_identificador(df)
    df = aplicar_title_nomes_colunas(df)
    # Iniciando tratamento da coluna Bairro
    df = transformar_para_caixa_baixa(df)
    df = remover_espaços_em_branco_extras(df)
    df = padronizar_nomes_dos_bairros(df)
    df = renomeando_bairro(df)
    df = aplicar_title(df)
    # Criar a coluna regiao
    df = criar_a_coluna_Regiao(df)

    df = substituir_os_valores_da_coluna_tipo_ocupacao_pardronizar(df)

    df = criar_coluna_ano(df)
    df = criar_coluna_mes(df)

    df = converter_coluna_valor_avaliacao(df)
    Salvar_o_DataFrame_em_arquivo_CSV_e_Json(df)

if __name__ == '__main__':
    main()