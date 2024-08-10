import streamlit as st
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
    st.write("\nCobertura total estimada para a casa: {:.2f}%\n".format(calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares)))

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
                porcentagem_cobertura_comodo = calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares) * (0.8 + 0.2 * distancia_impacto)
            elif tipo == 'Banheiros':
                porcentagem_cobertura_comodo = calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares) * (0.6 + 0.4 * distancia_impacto)
            elif tipo == 'Salas':
                porcentagem_cobertura_comodo = calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares) * (0.7 + 0.3 * distancia_impacto)
            elif tipo == 'Cozinhas':
                porcentagem_cobertura_comodo = calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares) * (0.5 + 0.5 * distancia_impacto)
            elif tipo == 'Áreas Externas':
                porcentagem_cobertura_comodo = calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares) * (0.4 + 0.6 * distancia_impacto)
            st.write(f"Cobertura na {tipo} {i + 1} ({area_comodo:.2f} m²): {porcentagem_cobertura_comodo:.2f}%")

    # Relatório final
    st.write("\nRelatório de Cobertura Wi-Fi:")
    st.write(f"Área total da casa: {area_total:.2f} m²")
    st.write(f"Número total de cômodos: {total_comodos}")
    st.write(f"Número de quartos: {quartos}")
    st.write(f"Número de banheiros: {banheiros}")
    st.write(f"Número de salas: {salas}")
    st.write(f"Número de cozinhas: {cozinhas}")
    st.write(f"Número de áreas externas: {areas_externas}")
    st.write(f"Potência do sinal: {potencia_sinal_dBm:.2f} dBm")
    st.write(f"Posição do roteador: {posicao_roteador.capitalize()}")
    st.write(f"Tipo de paredes: {', '.join(tipo_paredes)}")
    st.write(f"Cobertura geral estimada: {calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares):.2f}%")
    st.write(f"Número de andares: {andares}")

    # Considerações e Avaliação
    avaliacao = sugerir_cabeamento(calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares))
    st.write(f"\nConsiderações Finais:")
    st.write(avaliacao)

# Widgets para a interface
st.title("Análise de Cobertura Wi-Fi")

frequencia_ghz = st.selectbox('Frequência (GHz):', [2.4, 5.0], index=0)

area_total = st.number_input('Área total (m²):', value=400)

andares = st.slider('Número de andares:', min_value=1, max_value=5, value=1)

quartos = st.slider('Número de quartos:', min_value=0, max_value=20, value=4)

banheiros = st.slider('Número de banheiros:', min_value=0, max_value=20, value=2)

salas = st.slider('Número de salas:', min_value=0, max_value=20, value=2)

cozinhas = st.slider('Número de cozinhas:', min_value=0, max_value=20, value=1)

areas_externas = st.slider('Número de áreas externas:', min_value=0, max_value=20, value=2)

num_paredes = st.slider('Número total de paredes:', min_value=0, max_value=20, value=8)

tipo_paredes = st.multiselect('Tipo de paredes:', ['concreto', 'azulejo', 'metal', 'nenhuma'], default=['concreto'])

potencia_sinal_dBm = st.number_input('Potência do sinal (dBm):', value=20)

posicao_roteador = st.selectbox('Posição do roteador:', ['frente', 'meio', 'fundos'])

# Calcular e exibir a cobertura
calcular_cobertura_comodos(area_total, quartos, banheiros, salas, cozinhas, areas_externas, num_paredes, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares)
