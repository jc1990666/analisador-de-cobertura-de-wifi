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
def calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares):
    perdas_parede_total = calcula_perda_parede(tipo_paredes)

    # Ajuste da potência com base nas paredes e na frequência
    potencia_ajustada_dBm = potencia_sinal_dBm - perdas_parede_total

    # Ajuste adicional com base na posição do roteador
    posicao_fatores = {'frente': 1.2, 'meio': 1.0, 'fundos': 0.8}
    fator_ajuste = posicao_fatores.get(posicao_roteador, 1.0)

    # Ajuste para andares
    potencia_ajustada_dBm -= (andares - 1) * 2  # Perda adicional de sinal por andar

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
def calcular_cobertura_comodos(area_total, quartos, banheiros, salas, cozinhas, areas_externas, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares):
    output.clear_output()
    with output:
        porcentagem_cobertura_geral = calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares)
        print(f"\nCobertura total estimada para a casa: {porcentagem_cobertura_geral:.2f}%\n")

        # Cálculo da área média por tipo de cômodo
        total_comodos = quartos + banheiros + salas + cozinhas + areas_externas
        area_comodo = area_total / total_comodos if total_comodos > 0 else area_total

        # Ajuste da cobertura com base na distância e tipo de cômodo
        tipos_comodos = {
            'Quartos': quartos,
            'Banheiros': banheiros,
            'Salas': salas,
            'Cozinhas': cozinhas,
            'Áreas Externas': areas_externas
        }

        for tipo, quantidade in tipos_comodos.items():
            for i in range(quantidade):
                distancia_impacto = 1 - (i / (quantidade - 1)) if quantidade > 1 else 1
                # Aplicar ajuste na cobertura por tipo de cômodo
                if tipo == 'Quartos':
                    porcentagem_cobertura_comodo = porcentagem_cobertura_geral * (0.8 + 0.2 * distancia_impacto)
                elif tipo == 'Banheiros':
                    porcentagem_cobertura_comodo = porcentagem_cobertura_geral * (0.6 + 0.4 * distancia_impacto)
                elif tipo == 'Salas':
                    porcentagem_cobertura_comodo = porcentagem_cobertura_geral * (0.7 + 0.3 * distancia_impacto)
                elif tipo == 'Cozinhas':
                    porcentagem_cobertura_comodo = porcentagem_cobertura_geral * (0.5 + 0.5 * distancia_impacto)
                elif tipo == 'Áreas Externas':
                    porcentagem_cobertura_comodo = porcentagem_cobertura_geral * (0.4 + 0.6 * distancia_impacto)
                print(f"Cobertura na {tipo} {i + 1} ({area_comodo:.2f} m²): {porcentagem_cobertura_comodo:.2f}%")

        # Relatório final
        print("\nRelatório de Cobertura Wi-Fi:")
        print(f"Área total da casa: {area_total:.2f} m²")
        print(f"Número total de cômodos: {total_comodos}")
        print(f"Número de quartos: {quartos}")
        print(f"Número de banheiros: {banheiros}")
        print(f"Número de salas: {salas}")
        print(f"Número de cozinhas: {cozinhas}")
        print(f"Número de áreas externas: {areas_externas}")
        print(f"Potência do sinal: {potencia_sinal_dBm:.2f} dBm")
        print(f"Posição do roteador: {posicao_roteador.capitalize()}")
        print(f"Tipo de paredes: {', '.join(tipo_paredes)}")
        print(f"Cobertura geral estimada: {porcentagem_cobertura_geral:.2f}%")
        print(f"Número de andares: {andares}")

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
    value=400,
    description='Área total (m²):',
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

quartos = widgets.IntSlider(
    value=4,
    min=0,
    max=20,
    step=1,
    description='Número de quartos:',
    style={'description_width': 'initial'}
)

banheiros = widgets.IntSlider(
    value=2,
    min=0,
    max=20,
    step=1,
    description='Número de banheiros:',
    style={'description_width': 'initial'}
)

salas = widgets.IntSlider(
    value=2,
    min=0,
    max=20,
    step=1,
    description='Número de salas:',
    style={'description_width': 'initial'}
)

cozinhas = widgets.IntSlider(
    value=1,
    min=0,
    max=20,
    step=1,
    description='Número de cozinhas:',
    style={'description_width': 'initial'}
)

areas_externas = widgets.IntSlider(
    value=2,
    min=0,
    max=20,
    step=1,
    description='Número de áreas externas:',
    style={'description_width': 'initial'}
)

num_paredes = widgets.IntSlider(
    value=8,
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

# Botão para calcular
botao = widgets.Button(
    description='Calcular Cobertura',
    button_style='success',
    style={'description_width': 'initial'}
)

output = widgets.Output()

# Função ao clicar no botão
def on_button_click(b):
    calcular_cobertura_comodos(
        area_total.value,
        quartos.value,
        banheiros.value,
        salas.value,
        cozinhas.value,
        areas_externas.value,
        num_paredes.value,
        tipo_paredes.value,
        potencia_sinal_dBm.value,
        posicao_roteador.value,
        andares.value
    )

botao.on_click(on_button_click)

# Exibir widgets
display(titulo, frequencia_ghz, area_total, andares, quartos, banheiros, salas, cozinhas, areas_externas, num_paredes, tipo_paredes, potencia_sinal_dBm, posicao_roteador, botao, output)