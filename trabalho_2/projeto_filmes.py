print('=========================')
print('PROJETO FILMES')
print('=========================\n\n')

print('CARREGANDO AS BIBLIOTECAS...')
print('--------------------------\n\n')

import pandas as pd  
# pandas = biblioteca para trabalhar com tabelas (DataFrame)

import numpy as np  
# numpy = biblioteca para os cálculos

import matplotlib.pyplot as plt  
# matplotlib = biblioteca para criar os gráficos

import seaborn as sns
# seaborn = biblioteca para gráficos mais bonitos

print('=========================')
print('PARTE 1 - CARREGAMENTO E EXPLORAÇÃO')
print('=========================\n\n')

df = pd.read_csv('data.csv')
# read_csv() = lê o arquivo CSV e transforma em tabela

df.columns = df.columns.str.strip()
# remove espaços antes/depois

df.columns = df.columns.str.replace(" ", "_")
# troca espaço por _

print('AS 5 PRIMEIRAS LINHAS DO DATAFRAME: ')
print(df[['Movie_Name', 'Movie_Rating']].head(), '\n') 
# head() = mostra as 5 primeiras linhas

print('LINHAS X COLUNAS: ')
print(df.shape, '\n')  
# shape = mostra (linhas, colunas)

print('TIPO DAS COLUNAS: ')
print(df.dtypes, '\n')  
# dtypes = mostra o tipo de cada coluna (int, float, object)

print('RESUMO GERAL: ')
print(df.info(), '\n')  
# info() = resumo geral (dados, nulos, tipos)

print('ESTATÍSTICAS: ')
print(df.describe(), '\n')  
# describe() = estatísticas (média, mínimo, máximo, etc)

print('=========================')
print('PARTE 2 - LIMPEZA ')
print('=========================\n\n')

print('VAZIOS: ')
print(df.isnull().sum(), '\n')  
# isnull() = verifica valores vazios
# sum() = soma quantos tem em cada coluna

df['MetaScore'] = df['MetaScore'].fillna(df['MetaScore'].mean())  
# fillna() = preenche valores vazios
# mean() = calcula a média

df = df.dropna(subset=['Gross'])  
# dropna() = remove linhas com valores vazios
# subset = define a coluna que será verificada

print('DUPLICADOS: ')
df = df.drop_duplicates()  
# drop_duplicates() = remove linhas repetidas
print(df.duplicated().sum(),'\n')  
# duplicated() = verifica quantas linhas repetidas ainda existem

print('=========================')
print('PARTE 3 - ANÁLISE E FILTROS')
print('=========================\n\n')

# Filmes com nota maior que 8 e mais de 100 mil votos
filtro1 = df[
    (df['Movie_Rating'] > 8) &
    (df['Votes'] > 100000)
    ].head()
# & = E (duas condições ao mesmo tempo)

print('FILTRO 1 (Nota > 8 e Votos > 100k): ')
print(filtro1[['Movie_Rating', 'Votes', 'Movie_Name']],'\n')  
# mostra primeiros resultados

# Filmes com nota maior que 9 ou MetaScore maior que 80
filtro2 = df[
    (df['Movie_Rating'] > 9) |
    (df['MetaScore'] > 80)
].head()
# | = OU (uma ou outra condição)

print('FILTRO 2 (Nota > 9 ou MetaScore > 80): ')
print(filtro2[['Movie_Rating', 'MetaScore', 'Movie_Name']],'\n')

# Filmes com nota menor que 7 usando o 'não'
filtro3 = df[
    ~(df['Movie_Rating'] >= 7)
    ].head()
# ~ = NÃO (negação)

print('FILTRO 3 (Nota < 7): ')
print(filtro3[['Movie_Rating', 'Movie_Name']],'\n')

print('-------- ORDENAÇÃO --------')

# Top 10 filmes por nota (melhores)
top10 = df.sort_values(by='Movie_Rating', ascending=False).head(10)
# sort_values() = ordena dados
# ascending=False = ordem decrescente

print('TOP 10 (melhores): ')
print(top10[['Movie_Name', 'Movie_Rating']],'\n')

# Top 10 filmes por nota (piores)
bottom10 = df.sort_values(by='Movie_Rating', ascending=True).head(10)
# ascending=True = ordem crescente

print('TOP 10 (piores): ')
print(bottom10[['Movie_Name', 'Movie_Rating']],'\n')

print('-------- AGRUPAMENTO --------')

# Média de nota por ano de lançamento
media_por_ano = df.groupby('Year_of_Release')['Movie_Rating'].mean()
# groupby() = agrupa dados por coluna
# mean() = média

print('MÉDIA DE NOTA POR ANO DE LANÇAMENTO:')
print(media_por_ano,'\n')

# Contagem de filmes por gênero
generos = df['Genre'].value_counts()
# value_counts() = conta quantas vezes cada valor aparece

print('CONTAGEM DE FILMES POR GÊNERO:')
print(generos, '\n')

print('-------- NUMPY --------')

# desvio padrão das notas
desvio = np.std(df['Movie_Rating'])
# std() = desvio padrão (variação dos dados)

print('DESVIO PADRÃO DAS NOTAS: ')
print(desvio, '\n')

# correlação entre nota e número de votos
correlacao = np.corrcoef(df['Movie_Rating'], df['Votes'])
# corrcoef() = correlação entre duas variáveis

print('CORRELAÇÃO ENTRE NOTA E NÚMERO DE VOTOS: ')
print(correlacao, '\n')

print('-------- NOVA COLUNA --------')

# nova coluna popularidade = nota * número de votos
df['Popularidade'] = df['Movie_Rating'] * df['Votes']
# cria nova coluna baseada em outras

print('POPULARIDADE: ')
print(df[['Movie_Name', 'Popularidade']].head(), '\n')

# =========================
# PARTE 4 - GRÁFICOS
# =========================

# ----- BARRAS -----

# cria uma nova área de gráfico
plt.figure(figsize=(10, 5))

top_gen = df['Genre'].value_counts().head(5) # os 5 do topo
# conta os 5 gêneros mais frequentes

sns.barplot(              # barplot() cria gráfico de barras
    x=top_gen.index,      # x = nomes das categorias (gêneros)
    y=top_gen.values,     # y = valores (quantidade de filmes em cada gênero)
    color= "#70ECB0",       # cor das barras
    width=0.9             # largura das barras
)

plt.title('Top 5 Gêneros de Filmes', weight='bold')
# título do gráfico

plt.xlabel('Gênero')
# nome do eixo X

plt.ylabel('Quantidade')
# nome do eixo Y

plt.xticks(rotation=30)
# gira os nomes para não ficarem sobrepostos

plt.tight_layout()
# ajusta o layout

plt.savefig('grafico_barras.png', dpi=300)
# salva o gráfico em alta qualidade (PNG)

plt.show()
# mostra o gráfico

# ----- HISTOGRAMA -----

plt.figure(figsize=(10, 5))

sns.histplot(df['Movie_Rating'], bins=20, color= "#70ECB0")

plt.title('Distribuição das Notas')
plt.xlabel('Nota')
plt.ylabel('Frequência')
plt.tight_layout()
# Ajusta o layout para não cortar elementos

plt.savefig('histograma.png')
plt.show()

# ----- LINHA -----

# Cria uma nova área para o gráfico
plt.figure(figsize=(10, 5))

media_por_ano = df.groupby('Year_of_Release')['Movie_Rating'].mean()
# groupby() agrupa os dados por ano de lançamento
# ['IMDB_Rating'] seleciona a coluna de notas
# mean() calcula a média das notas em cada ano

media_por_ano = media_por_ano.sort_index()
# sort_index() organiza os anos em ordem crescente

sns.lineplot(
    x=media_por_ano.index,
    y=media_por_ano.values,
    marker='^',          # adiciona pontos na linha
    linewidth=2,         # deixa a linha mais grossa
    color= "#70ECB0"   # define a cor da linha
)
# lineplot() cria o gráfico de linha

plt.fill_between(
    media_por_ano.index,
    media_por_ano.values,
    alpha=0.1
)
# fill_between() preenche a área abaixo da linha
# alpha controla a transparência

plt.title('Evolução da Nota Média dos Filmes ao Longo dos Anos', weight='bold')
# Define o título do gráfico em negrito

plt.xlabel('Ano')
# Nome do eixo X

plt.ylabel('Nota Média')
# Nome do eixo Y


plt.tight_layout()
# Ajusta o layout para não cortar elementos

plt.savefig('grafico_linha.png', dpi=300)
# Salva o gráfico com alta qualidade

plt.show()
# Exibe o gráfico na tela

# ----- PIZZA -----

plt.figure(figsize=(10, 5))
# Cria uma nova área para o gráfico

labels = ['Filmes Bons (≥7)', 'Filmes Ruins (<7)']
# Define os nomes das categorias que vão aparecer na pizza

valores = [
    len(df[df['Movie_Rating'] >= 7]),   # Conta os filmes (nota >= 7)
    len(df[df['Movie_Rating'] < 7])     # Conta os filmes (nota < 7)
]

plt.pie(                                # Cria o gráfico de pizza
    valores,                            # Tamanho de cada fatia
    labels=labels,                      # Nomes das fatias
    autopct='%1.1f%%',                  # Mostra a porcentagem em cada fatia
    colors=["#E175AF", "#70ECB0"],  # Define as cores
    explode=(0.1, 0),                   # Destaca a maior fatia
    startangle=90                       # Gira o gráfico para melhor visualização
)

plt.title('Proporção de Filmes Bons vs Ruins', weight='bold')
# Define o título do gráfico (em negrito)

plt.savefig('grafico_pizza.png', dpi=300)
# Salva o gráfico como imagem com alta qualidade

plt.show()
# Exibe o gráfico na tela

# =========================
# BÔNUS - HEATMAP
# =========================

import seaborn as sns  
# seaborn = gráficos mais avançados

plt.figure(figsize=(10, 5))

correlacao = df[['Movie_Rating', 'Votes', 'MetaScore']].corr()
# corr() = calcula correlação entre colunas

sns.heatmap(correlacao, annot=True, cmap='Blues')
# heatmap() = mapa de calor
# annot=True = mostra os valores
# cmap = paleta de cores

plt.title('Mapa de Correlação')

plt.savefig('heatmap.png')
plt.show()