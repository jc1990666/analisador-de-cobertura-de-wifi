import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np

# Função para calcular a perda de sinal com base no tipo de parede
def calcula_perda_parede(tipo_paredes):
    perdas_parede = {
        'concreto': 10,
        'azulejo': 6,
        'metal': 13,
        'nenhuma': 0
    }
    return sum([perdas_parede[parede] for parede in tipo_paredes])

# Função para calcular a cobertura geral com base na potência do sinal e perdas
def calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares, quantidade_roteadores, frequencia_ghz):
    perdas_parede_total = calcula_perda_parede(tipo_paredes)
    potencia_ajustada_dBm = potencia_sinal_dBm - perdas_parede_total

    # Ajuste adicional com base na posição do roteador
    posicao_fatores = {'frente': 1.2, 'meio': 1.0, 'fundos': 0.8}
    fator_ajuste = posicao_fatores.get(posicao_roteador, 1.0)

    # Ajuste para andares
    potencia_ajustada_dBm -= (andares - 1) * 2  # Perda adicional de sinal por andar

    # Ajuste para quantidade de roteadores
    potencia_ajustada_dBm += quantidade_roteadores * 5  # Cada roteador adicional melhora a cobertura

    # Ajuste para frequência
    if frequencia_ghz == 5.0:
        potencia_ajustada_dBm -= 5  # Frequência de 5 GHz tem menor penetração

    # Cobertura geral estimada considerando a potência ajustada
    cobertura_base_dBm = 20  # Valor base para cálculo (potência ideal)
    porcentagem_cobertura = (potencia_ajustada_dBm / cobertura_base_dBm) * 100 * fator_ajuste
    return max(0, min(porcentagem_cobertura, 100))

# Função para sugerir cabeamento baseado na cobertura obtida
def sugerir_cabeamento(porcentagem_cobertura_geral):
    if porcentagem_cobertura_geral < 30:
        recomendacao = "A cobertura Wi-Fi é muito baixa. Para melhorar, considere a instalação de roteadores adicionais cabeados. "
        quantidade_roteadores = np.ceil((70 - porcentagem_cobertura_geral) / 10)
        recomendacao += f"Para atingir uma cobertura ideal, considere a instalação de aproximadamente {int(quantidade_roteadores)} roteadores adicionais."
    elif porcentagem_cobertura_geral < 60:
        recomendacao = "A cobertura Wi-Fi é moderada. Para alcançar 70%, considere a instalação de mais roteadores cabeados. "
        quantidade_roteadores = np.ceil((70 - porcentagem_cobertura_geral) / 10)
        recomendacao += f"Instalar cerca de {int(quantidade_roteadores)} roteadores adicionais pode ajudar a melhorar a cobertura."
    else:
        recomendacao = "A cobertura Wi-Fi é boa, mas sempre é bom monitorar áreas distantes. Se necessário, adicione roteadores em pontos estratégicos."

    return recomendacao

# Função principal para calcular a cobertura dos cômodos
def calcular_cobertura_comodos(area_total, comprimento, largura, num_comodos, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares, quantidade_roteadores, quantidade_internet, frequencia_ghz):
    output.clear_output()
    with output:
        porcentagem_cobertura_geral = calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares, quantidade_roteadores, frequencia_ghz)
        print(f"\nCobertura total estimada para a casa: {porcentagem_cobertura_geral:.2f}%\n")

        # Cálculo da área por cômodo
        area_comodo = area_total / num_comodos if num_comodos > 0 else area_total

        for i in range(num_comodos):
            distancia_impacto = 1 - (i / (num_comodos - 1)) if num_comodos > 1 else 1
            porcentagem_cobertura_comodo = porcentagem_cobertura_geral * (0.8 + 0.2 * distancia_impacto)
            print(f"Cobertura na Cômodo {i + 1} ({area_comodo:.2f} m²): {porcentagem_cobertura_comodo:.2f}%")

        # Relatório final
        print("\nRelatório de Cobertura Wi-Fi:")
        print(f"Área total da casa: {area_total:.2f} m²")
        print(f"Comprimento: {comprimento:.2f} m")
        print(f"Largura: {largura:.2f} m")
        print(f"Número total de cômodos: {num_comodos}")
        print(f"Número total de paredes: {paredes_total}")
        print(f"Potência do sinal: {potencia_sinal_dBm:.2f} dBm")
        print(f"Posição do roteador: {posicao_roteador.capitalize()}")
        print(f"Tipo de paredes: {', '.join(tipo_paredes)}")
        print(f"Cobertura geral estimada: {porcentagem_cobertura_geral:.2f}%")
        print(f"Número de andares: {andares}")
        print(f"Quantidade de roteadores: {quantidade_roteadores}")
        print(f"Quantidade de internet contratada: {quantidade_internet} Mbps")
        print(f"Frequência do sinal: {frequencia_ghz} GHz")

        # Considerações e Avaliação
        avaliacao = sugerir_cabeamento(porcentagem_cobertura_geral)
        print(f"\nConsiderações Finais:")
        print(avaliacao)

# Widgets para a interface
titulo = widgets.HTML(value="<h1 style='text-align: center; color: #FF6600;'>Análise de Cobertura Wi-Fi</h1>")

# Parâmetros gerais da casa
frequencia_ghz = widgets.Dropdown(
    options=[2.4, 5.0],
    value=2.4,
    description='Frequência (GHz):',
    style={'description_width': 'initial'}
)

area_total = widgets.FloatText(
    value=170,
    description='Área total (m²):',
    style={'description_width': 'initial'}
)

comprimento = widgets.FloatText(
    value=10,
    description='Comprimento (m):',
    style={'description_width': 'initial'}
)

largura = widgets.FloatText(
    value=14,
    description='Largura (m):',
    style={'description_width': 'initial'}
)

num_comodos = widgets.IntSlider(
    value=9,
    min=1,
    max=20,
    step=1,
    description='Número de cômodos:',
    style={'description_width': 'initial'}
)

andares = widgets.IntSlider(
    value=1,
    min=1,
    max=5,
    step=1,
    description='Número de andares:',
    style={'description_width': 'initial'}
)

num_paredes = widgets.IntSlider(
    value=6,
    min=0,
    max=20,
    step=1,
    description='Número total de paredes:',
    style={'description_width': 'initial'}
)

tipo_paredes = widgets.SelectMultiple(
    options=['concreto', 'azulejo', 'metal', 'nenhuma'],
    value=['concreto'],
    description='Tipo de paredes:',
    style={'description_width': 'initial'}
)

potencia_sinal_dBm = widgets.FloatText(
    value=20,
    description='Potência do sinal (dBm):',
    style={'description_width': 'initial'}
)

posicao_roteador = widgets.Dropdown(
    options=['frente', 'meio', 'fundos'],
    value='meio',
    description='Posição do roteador:',
    style={'description_width': 'initial'}
)

quantidade_roteadores = widgets.IntSlider(
    value=2,
    min=1,
    max=5,
    step=1,
    description='Quantidade de roteadores:',
    style={'description_width': 'initial'}
)

quantidade_internet = widgets.IntText(
    value=200,
    description='Quantidade de internet contratada (Mbps):',
    style={'description_width': 'initial'}
)

# Botão para calcular
calcular_button = widgets.Button(description="Calcular Cobertura")
output = widgets.Output()

def on_calcular_button_clicked(b):
    with output:
        clear_output()
        calcular_cobertura_comodos(
            area_total.value,
            comprimento.value,
            largura.value,
            num_comodos.value,
            num_paredes.value,
            list(tipo_paredes.value),
            potencia_sinal_dBm.value,
            posicao_roteador.value,
            andares.value,
            quantidade_roteadores.value,
            quantidade_internet.value,
            frequencia_ghz.value
        )

calcular_button.on_click(on_calcular_button_clicked)

# Exibir widgets
display(titulo, frequencia_ghz, area_total, comprimento, largura, num_comodos, andares, num_paredes, tipo_paredes, potencia_sinal_dBm, posicao_roteador, quantidade_roteadores, quantidade_internet, calcular_button, output)
