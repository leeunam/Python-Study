import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Importei a base de dados pelo comando do pandas (pd.read_csv) e atribui a uma variável chamada df
df = pd.read_csv("medical_examination.csv")

# 2. O primeiro passo para criar uma nova coluna ('overweight') será por atribuição direta, para passar os valores dela usaremos o método de filtragem: 
# df['NovaColuna'] = np.where(df['ColunaExistente'] > valor, 'Condição Verdadeira', 'Condição Falsa')
# A função acima segue a lógica de criado uma nova coluna no dataset, usaremos o numpy para verificar se uma determinada condição acontece, se sim retornar a primeira mensagem depois da vírgula, se não retornar o outro valor.
# Dividi por 100 porque o valor de height está em cm, e a questão pede em metros.
df['overweight'] = np.where(df['weight']/(df['height']/100)**2 > 25, 1, 0)

# 3. Como eu preciso normalizar as colunas 'cholesterol' e 'gluc', usei a mesma formula acima. A regra será, se o valor for acima de 1, vira 1, abaixo de 1, vira 0. 
df['cholesterol'] = np.where(df['cholesterol'] > 1, 1, 0)
df['gluc'] = np.where(df['gluc'] > 1, 1, 0)


# 4. O gráfico categórico sera desenhado dentro da função abaixo
def draw_cat_plot():
    # 5.  criei um DataFrame chamada df_cat que irá manter a coluna cardio e irá derreter do DataFrame (df) as colunas após value_vars.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])   

    # 6. Na primeira linha eu uso a função de groupby para agrupar as linhas por cardio, catplot e value. Já a função size conta quantas linhas existem em cada grupo.
    # no final eu uso reset_index porque o seaborn precisa de um DataFrame. Depois de usar groupby().size(), o resultado são series com índices múltiplos.
    # Sendo assim o reset_index(name='total') transforma cada coluna do índice em uma coluna normal e o valor do .size() em uma coluna chamada total.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    
    # 7. O DataFrame já esta convertido em long. Logo, eu apenas vou gerar o gráfico com seaborn e guardar dentro do chart
    chart = sns.catplot(data=df_cat, x="variable",y="total",col="cardio", hue="value", kind="bar")

    # 8. Pego a figure dentro do FacetGrid e armazeno isso na variável fig
    fig = chart.fig

    # 9. Não é necessário modificar nada
    fig.savefig('catplot.png')
    return fig

# 10 Função para gerar mapa de calor
def draw_heat_map():
    # 11. Dentro do data frame heat eu vou:
    # pegar os dados em que a pressão diastólica é menor que a sistólica 
    # a altura é maior que o percentil 2,5
    # a altura é menor que o percentil 97,5
    # o peso é maior que o percentil 2,5
    # o peso é menor que o percentil 97,5
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12. A função corr() do pandas já cria a matriz de correlação em um data frame
    corr = df_heat.corr()

    # 13. Crio uma mascara de triângulo superior na matriz de correlação e guardo ela dentro da variável mask
    # Abaixo crio uma mascara que ira armazenar uma matriz de zeros booleanos, o tamanho da matriz será o tamanho da matriz de correlação criada acima
    # A formula len(corr) pega as linhas da matriz de correlação enquanto a len(matriz[0]) pega a coluna da matriz de correlação
    columns = len(corr.columns)
    lines = len(corr)
    mask = np.zeros((lines, columns), dtype=bool)


    # iteração sobre as linhas para definir a mascara
    for i in range(lines):
        # iteração sobre as colunas para definir a mascara
        for j in range (columns):
            # Condição para o triângulo superior incluir a diagonal
            if i <= j:
                mask[i, j] = True

    # O triangulo superior de uma matriz é onde todos os elementos abaixo da diagonal principal são zero. 
    # A condição formal é que um elemento da matriz (a_ij) (na linha i e coluna j) deve ser zero sempre que o índice da linha for maior que o índice da coluna (i>j). 
    # Os elementos na diagonal principal (i=j) e acima dela (i<j) podem ter qualquer valor, incluindo zero.

    # 14 Configurar a figura do matplotlib
    fig, ax = plt.subplots()

    # 15. traço a matriz de correlação usando o método de imporatação sns.heatmap()
    # A função espera (uma data em formato de matriz) sendo assim passo a matriz de correlação (corr) e uso a mascara para esconder a parte superior
    # O annot coloca o número da correlação escrito dentro do quadrado, enquanto o fmt mosstra os números com 1 casa decimal e o center 0 coloca um ponto neutro da paleta(ou seja menor que zero a cor é azul e maior que zero fica vermelho)
    # Por último, ax são os eixos, e como padrão eu vou passar o ax sem modificar.
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", center=0, ax=ax)

    # 16
    fig.savefig('heatmap.png')
    return fig