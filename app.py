import streamlit as st

def calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipo_paredes, freq, comprimento, largura, num_comodos, pos_roteadores, velocidade_internet):
    # Calcula a cobertura geral com base nos fatores fornecidos
    area_total = comprimento * largura
    perda_parede = tipo_paredes * paredes
    perda_freq = 0
    if freq == 2.4:
        perda_freq = 2  # Padrão para 2.4 GHz
    elif freq == 5:
        perda_freq = 5  # Padrão para 5 GHz
    
    cobertura_total = (potencia_sinal - perda_parede - perda_freq) / (num_roteadores * area_total) * 100
    return max(min(cobertura_total, 100), 0)  # Garantir que a cobertura esteja entre 0 e 100%

def cobertura_por_comodo(cobertura_total, num_comodos):
    if num_comodos == 0:
        return 0
    return cobertura_total / num_comodos

def main():
    st.title('Análise de Cobertura Wi-Fi')
    
    freq = st.selectbox("Frequência (GHz):", [2.4, 5])
    comprimento = st.number_input("Comprimento total do ambiente (m):", min_value=1, value=20)
    largura = st.number_input("Largura total do ambiente (m):", min_value=1, value=20)
    num_andares = st.number_input("Número de andares:", min_value=1, value=1)
    num_comodos = st.number_input("Número total de cômodos:", min_value=1, value=10)
    paredes = st.number_input("Número total de paredes:", min_value=0, value=8)
    tipo_paredes = st.selectbox("Tipo de paredes:", ["concreto", "azulejo", "metal", "nenhuma"])
    potencia_sinal = 20  # Padrão de mercado fixo
    velocidade_internet = st.number_input("Velocidade da Internet (Mbps):", min_value=1, value=300)
    
    num_roteadores = st.number_input("Número de roteadores:", min_value=1, value=1)
    
    pos_roteadores = []
    for i in range(num_roteadores):
        st.write(f"Posição do Roteador {i+1}:")
        andar = st.selectbox(f"Andar do Roteador {i+1}:", [f"Primeiro andar", f"Segundo andar"], index=0)
        posicao = st.selectbox(f"Posição no {andar}:", ["frente", "meio", "fundo"], index=1)
        pos_roteadores.append((andar, posicao))

    cobertura_total = calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipo_paredes, freq, comprimento, largura, num_comodos, pos_roteadores, velocidade_internet)
    st.write(f'Cobertura Geral Estimada: {cobertura_total:.2f}%')

    for i in range(1, num_comodos + 1):
        cobertura = cobertura_por_comodo(cobertura_total, num_comodos)
        st.write(f'Cobertura no Cômodo {i}: {cobertura:.2f}%')

if __name__ == "__main__":
    main()
