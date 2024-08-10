import streamlit as st

def calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipo_paredes, freq, comprimento, largura, num_comodos, pos_roteador, velocidade_internet):
    # Definindo valores padrão
    sinal_base = 50  # Base de sinal padrão para cálculos

    # Ajuste baseado na potência do sinal
    if potencia_sinal < -70:
        sinal_base -= 10
    elif potencia_sinal < -50:
        sinal_base -= 5
    
    # Ajuste baseado na quantidade de paredes
    perda_por_parede = 5 if tipo_paredes == 'concreto' else 2
    sinal_base -= paredes * perda_por_parede
    
    # Ajuste baseado na frequência
    if freq == 5:
        sinal_base += 10  # Frequência de 5 GHz pode ter melhor desempenho em ambientes abertos
    
    # Ajuste baseado na posição do roteador
    if pos_roteador == 'meio':
        sinal_base += 10
    elif pos_roteador == 'fundo':
        sinal_base -= 5
    elif pos_roteador == 'frente':
        sinal_base += 5
    
    # Ajuste baseado no número de roteadores
    sinal_base += num_roteadores * 5
    
    # Ajuste baseado na área total
    area_total = comprimento * largura
    cobertura_total = min(100, sinal_base - (area_total / 100))  # Simplificação
    
    # Ajuste baseado na velocidade da internet
    if 100 <= velocidade_internet < 200:
        cobertura_total *= 0.8
    elif 200 <= velocidade_internet < 300:
        cobertura_total *= 1.0
    elif 300 <= velocidade_internet <= 500:
        cobertura_total *= 1.2
    
    return cobertura_total

def main():
    st.title("Análise de Cobertura Wi-Fi")
    
    # Frequência
    freq = st.selectbox("Frequência (GHz):", [2.4, 5.0])
    
    # Área total
    comprimento = st.number_input("Comprimento da área (m):", min_value=1.0, max_value=100.0, value=10.0)
    largura = st.number_input("Largura da área (m):", min_value=1.0, max_value=100.0, value=10.0)
    
    # Quantidade de cômodos
    num_comodos = st.number_input("Número de cômodos:", min_value=1, max_value=20, value=9)
    
    # Número de roteadores
    num_roteadores = st.number_input("Número de roteadores:", min_value=1, max_value=10, value=2)
    
    # Número de paredes
    paredes = st.number_input("Número de paredes:", min_value=0, max_value=50, value=6)
    
    # Tipo de paredes
    tipo_paredes = st.selectbox("Tipo de paredes:", ["concreto", "azulejo", "metal", "nenhuma"])
    
    # Potência do sinal
    potencia_sinal = st.slider("Potência do sinal (dBm):", min_value=-100, max_value=0, value=-60)
    
    # Posição do roteador
    pos_roteador = st.selectbox("Posição do roteador:", ["meio", "fundo", "frente"])
    
    # Velocidade da internet
    velocidade_internet = st.number_input("Velocidade da internet (Mbps):", min_value=50, max_value=500, value=300)

    # Calcular cobertura total
    cobertura_total = calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipo_paredes, freq, comprimento, largura, num_comodos, pos_roteador, velocidade_internet)
    st.write(f'Cobertura Geral Estimada: {cobertura_total:.2f}%')

    # Calcular e exibir cobertura por cômodo
    def cobertura_por_comodo(cobertura_total, num_comodos):
        if num_comodos == 0:
            return 0
        return cobertura_total / num_comodos

    for i in range(1, num_comodos + 1):
        cobertura = cobertura_por_comodo(cobertura_total, num_comodos)
        st.write(f'Cobertura na Cômodo {i}: {cobertura:.2f}%')

if __name__ == "__main__":
    main()
