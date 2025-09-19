import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    # A função abaixo gera um gráfico de disperção com base em 2 parameros y e x, coluna year e csiro[...] respectivamente
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'])

    # Create first line of best fit
    # A função linregress realiza uma regressão linear simples entre duas variáveis. Retornando diversos valores, entre eles: slope (coeficiente angular) e intercept (intercepto da linha), que são os que nos interessa.
    slope, intercept, r_value, p_value, std_err = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    # Crie anos a partir do ano mínimo em dados até 2050
    # Aqui eu criei uma lista de anos que vai do menor ano presente até 2050
    years_extended = range(df['Year'].min(), 2051)
    # Calculo dos valores de y correspondentes à linha de regressão para cada ano no intervalo definido.
    line_values = [slope * year + intercept for year in years_extended]
    # Desenho a linha de regressão no gráfico em vermelho ('r')
    plt.plot(years_extended, line_values, 'r')
    
    # Create second line of best fit
    # Filtro apenas os dados a partir do ano 2000.
    df_2000 = df[df['Year'] >= 2000]
    # Aqui eu calculo a regressão linear apenas para os dados filtrados (2000 em diante).
    slope_2000, intercept_2000, r_value_2000, p_value_2000, std_err_2000 = linregress(df_2000['Year'], df_2000['CSIRO Adjusted Sea Level'])
    
    # Crio anos de 2000 até 2050 para estender a segunda linha de regressão.
    years_2000_extended = range(2000, 2051)
    # Calculo os valores de y correspondentes à segunda linha de regressão.
    line_values_2000 = [slope_2000 * year + intercept_2000 for year in years_2000_extended]
    # Só ploto o gráfico igual antes, nada demais
    plt.plot(years_2000_extended, line_values_2000, 'g', label='Best fit line (2000-onwards)')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    plt.legend()
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()