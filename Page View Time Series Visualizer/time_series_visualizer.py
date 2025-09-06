import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# importei o data frame, e defini o indice padrão para ser a coluna 'date' por meio do código index_col. Para o eixo x não sair como texto e no gráfico ficar como tempo(data) eu tive que "parsear"(formatar) como data
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Limpei o dataframe filtrando os dados para quando os dias estiverem com views maior que 2,5% OU (operador | em dataframes python) menor que 2,5% do conjunto de dados original
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # A função plt.subplots() gera um gráfico de linhas com duas variáveis com escalas diferentes no mesmo gráfico, enquanto o ax é o objeto dos eixos para criar o gráfico o fig é o objeto que salva a figura.
    # O figsize serve para ajsutar o tamanho do gráfico, melhorando a visualização
    fig, ax = plt.subplots(figsize=(15,5))
    # Ploto o gráfico com eixo x sendo o indice(datas) e eixo y sendo as views(value)
    ax.plot(df.index, df['value'])
    # As funções abaixo mudam o nome de visualização do eixo x, y e título do gráfico respectivamente.
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # A primeira coisa é agrupar um novo dataframe onde haja um primeiro agrupamento por ano, e um segundo agrupamento por mes
    # OBS: como lá em cima eu já tratei os dados para que o indice fosse salvo como data e não string, então e possível manipular com essas funções
    # OBS: Após esse agrupamento eu já faço a média das colunas value, que nesse contexto são as views
    df_bar = df.groupby([df.index.year, df.index.month])['value'].mean()

    # Agora eu preciso transformar o agrupamento mês em coluna, a coluna value em valor da celula e o ano manter como indice.
    df_bar = df_bar.unstack()
    # O unstack já vai pegar o formato que estava que era: ano, mes muklti indice e valor como coluna. E fazer a formatação que comentei acima

    meses_ordem = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    # Na primeira vesão eu passava o df.index.month_name assim ele puxava os nomes direto dos meses por já estar formatado. Porém eles vinham em ordem alfabética devido ao agrupamento.
    # Eu não consegui achar uma solução buscando, então pedi para o gpt e ele me disse que uma forma prática seria primeiro puxar pelo indice mesmo, ou seja mes como número e depois de pivotar com .unstrack() eu reordeanar a coluna e mudar o nome dos número para o mês específico.
    df_bar.columns = [meses_ordem[m-1] for m in df_bar.columns]
    df_bar = df_bar.reindex(columns=meses_ordem)

    # Draw bar plot
    fig, ax = plt.subplots()
    df_bar.plot(kind='bar', ax=ax)

    # Configurar eixo x, y e legenda
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    #eu crio uma variavel com a ordem dos meses que quero, já que na hora de plotar existe um parametro chamado order que ordena o eixo conforme ordem que eu pedir
    order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5))
    # Pedi pro chat gerar 12 cores em hash que abranjam todo o círculo cromático e passo essa lista de cores para serem as paletas usadas no gráfico
    custom_palette = ["#e51919", "#e57f19", "#e5e519", "#7fe519", "#19e519", "#19e57f", "#19e5e5", "#197fe5", "#1919e5", "#7f19e5", "#e519e5", "#e5197f"]
    sns.boxplot(df_box, x='year', y='value', ax=ax1, palette=custom_palette).set(title='Year-wise Box Plot (Trend)', xlabel=('Year'), ylabel=('Page Views'))
    sns.boxplot(df_box, x='month', y='value', ax=ax2, order=order, palette=custom_palette).set(title='Month-wise Box Plot (Seasonality)', xlabel=('Month'), ylabel=('Page Views'))

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig