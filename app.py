import streamlit as st
import numpy as np

# Função para calcular perda de sinal com base no tipo de parede
def calcula_perda_parede(tipo_paredes):
    perdas_parede = {'concreto': 10, 'azulejo': 6, 'metal': 13, 'nenhuma': 0}
    return sum([perdas_parede[parede] for parede in tipo_paredes])

# Função para cálculo de cobertura geral
def calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares):
    perdas_parede_total = calcula_perda_parede(tipo_paredes)
    potencia_ajustada_dBm = potencia_sinal_dBm - perdas_parede_total

    posicao_fatores = {'frente': 1.2, 'meio': 1.0, 'fundos': 0.8}
    fator_ajuste = posicao_fatores.get(posicao_roteador, 1.0)

    potencia_ajustada_dBm -= (andares - 1) * 2
    cobertura_base_dBm = 20
    porcentagem_cobertura = (potencia_ajustada_dBm / cobertura_base_dBm) * 100 * fator_ajuste
    return max(0, min(porcentagem_cobertura, 100))

# Função para sugestão de cabeamento com base na cobertura obtida
def sugerir_cabamento(porcentagem_cobertura_geral):
    if porcentagem_cobertura_geral < 30:
        recomendacao = "A cobertura Wi-Fi é muito baixa. Para melhorar, considere a instalação de roteadores adicionais cabeados."
        quantidade_roteadores = np.ceil((70 - porcentagem_cobertura_geral) / 10)
        recomendacao += f" Para atingir uma cobertura ideal, considere a instalação de aproximadamente {int(quantidade_roteadores)} roteadores adicionais."
    elif porcentagem_cobertura_geral < 60:
        recomendacao = "A cobertura Wi-Fi é moderada. Para melhorar, considere a instalação de alguns roteadores adicionais."
    else:
        recomendacao = "A cobertura Wi-Fi é adequada. No entanto, você pode adicionar mais roteadores se desejar melhorar ainda mais a cobertura."

    return recomendacao

# Função principal do Streamlit
def main():
    st.title('Analisador de Cobertura de Wi-Fi')
    
    # Entrada de dados
    area_total = st.number_input('Área Total (m²)', min_value=0.0, step=0.1)
    paredes_total = st.number_input('Número Total de Paredes', min_value=0)
    tipo_paredes = st.multiselect('Tipo das Paredes', ['concreto', 'azulejo', 'metal', 'nenhuma'])
    potencia_sinal_dBm = st.slider('Potência do Sinal (dBm)', -100, 0)
    posicao_roteador = st.selectbox('Posição do Roteador', ['frente', 'meio', 'fundos'])
    andares = st.number_input('Número de Andares', min_value=1)

    if st.button('Calcular Cobertura'):
        cobertura = calcula_cobertura_geral(area_total, paredes_total, tipo_paredes, potencia_sinal_dBm, posicao_roteador, andares)
        st.write(f'A cobertura estimada é: {cobertura:.2f}%')
        
        recomendacao = sugerir_cabamento(cobertura)
        st.write(recomendacao)

if __name__ == "__main__":
    main()
