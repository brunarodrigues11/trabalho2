# =========================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =========================

import pandas as pd  
# pandas = biblioteca para trabalhar com tabelas (DataFrame)

import numpy as np  
# numpy = biblioteca para os cálculos

import matplotlib.pyplot as plt  
# matplotlib = biblioteca para criar os gráficos

import seaborn as sns
# seaborn = biblioteca para gráficos mais bonitos


# =========================
# PARTE 1 - CARREGAMENTO E EXPLORAÇÃO
# =========================

df = pd.read_csv('data.csv')  
# read_csv() = lê o arquivo CSV e transforma em tabela

print(df.head())  
# head() = mostra as 5 primeiras linhas

print(df.shape)  
# shape = mostra (linhas, colunas)

print(df.dtypes)  
# dtypes = mostra o tipo de cada coluna (int, float, object)

print(df.info())  
# info() = resumo geral (dados, nulos, tipos)

print(df.describe())  
# describe() = estatísticas (média, mínimo, máximo, etc)


df.columns = df.columns.str.strip()
# remove espaços antes/depois

df.columns = df.columns.str.replace(" ", "_")
# troca espaço por _


# =========================
# PARTE 2 - LIMPEZA 
# =========================

print(df.isnull().sum())  
# isnull() = verifica valores vazios
# sum() = soma quantos tem em cada coluna

df['MetaScore'] = df['MetaScore'].fillna(df['MetaScore'].mean())  
# fillna() = preenche valores vazios
# mean() = calcula a média

df = df.dropna(subset=['Gross'])  
# dropna() = remove linhas com valores vazios
# subset = define a coluna que será verificada

df = df.drop_duplicates()  
# drop_duplicates() = remove linhas repetidas


# =========================
# PARTE 3 - ANÁLISE E FILTROS
# =========================

# Filmes com nota maior que 8 e mais de 100 mil votos
filtro1 = df[(df['Movie_Rating'] > 8) & (df['Votes'] > 100000)]
# & = E (duas condições ao mesmo tempo)

print(filtro1.head())  
# mostra primeiros resultados

# Filmes com nota maior que 9 ou MetaScore maior que 80
filtro2 = df[(df['Movie_Rating'] > 9) | (df['MetaScore'] > 80)]
# | = OU (uma ou outra condição)

print(filtro2.head())

# Filmes com nota menor que 7 usando o 'não'
filtro3 = df[~(df['Movie_Rating'] >= 7)]
# ~ = NÃO (negação)

print(filtro3.head())


# -------- ORDENAÇÃO --------

# Top 10 filmes por nota (melhores)
top10 = df.sort_values(by='Movie_Rating', ascending=False).head(10)
# sort_values() = ordena dados
# ascending=False = ordem decrescente

print(top10[['Movie_Name', 'Movie_Rating']])

# Top 10 filmes por nota (piores)
bottom10 = df.sort_values(by='Movie_Rating', ascending=True).head(10)
# ascending=True = ordem crescente

print(bottom10[['Movie_Name', 'Movie_Rating']])


# -------- AGRUPAMENTO --------

# Média de nota por ano de lançamento
media_por_ano = df.groupby('Year_of_Release')['Movie_Rating'].mean()
# groupby() = agrupa dados por coluna
# mean() = média

print(media_por_ano)

# Contagem de filmes por gênero
generos = df['Genre'].value_counts()
# value_counts() = conta quantas vezes cada valor aparece

print(generos)


# -------- NUMPY --------

# desvio padrão das notas
desvio = np.std(df['Movie_Rating'])
# std() = desvio padrão (variação dos dados)

print("Desvio padrão:", desvio)

# correlação entre nota e número de votos
correlacao = np.corrcoef(df['Movie_Rating'], df['Votes'])
# corrcoef() = correlação entre duas variáveis

print("Correlação:", correlacao)


# -------- NOVA COLUNA --------

# nova coluna popularidade = nota * número de votos
df['Popularidade'] = df['Movie_Rating'] * df['Votes']
# cria nova coluna baseada em outras


# =========================
# PARTE 4 - GRÁFICOS
# =========================

# ----- BARRAS -----

# cria uma nova área de gráfico
plt.figure(figsize=(10, 5))

top_gen = df['Genre'].value_counts().head(5)
# conta os 5 gêneros mais frequentes

sns.barplot(              # barplot() cria gráfico de barras
    x=top_gen.index,      # x = nomes das categorias (gêneros)
    y=top_gen.values,     # y = valores (quantidade de filmes em cada gênero)
    color="#E80577",    # cor das barras
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
# salva o gráfico em alta qualidade

plt.show()
# mostra o gráfico


# ----- HISTOGRAMA -----


plt.figure(figsize=(10, 5))

plt.hist(df['Movie_Rating'], bins=20, color="#E80577")
# hist() = histograma
# bins = quantidade de divisões

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
    marker='^',        # adiciona pontos na linha
    linewidth=2,       # deixa a linha mais grossa
    color='#E80577'    # define a cor da linha
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
    colors=["#E80577", "#05E8B3"],  # Define as cores
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

sns.heatmap(correlacao, annot=True, cmap='Greens')
# heatmap() = mapa de calor
# annot=True = mostra os valores
# cmap = paleta de cores

plt.title('Mapa de Correlação')

plt.savefig('heatmap.png')
plt.show()