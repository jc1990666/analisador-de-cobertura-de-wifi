import streamlit as st

def calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipo_paredes, freq, comprimento, largura, num_comodos, pos_roteador, velocidade_internet):
    sinal_base = 50

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
        sinal_base += 10

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
    cobertura_total = sinal_base - (area_total / 50)

    # Ajuste baseado na velocidade da internet
    if 100 <= velocidade_internet < 200:
        cobertura_total *= 0.8
    elif 200 <= velocidade_internet < 300:
        cobertura_total *= 1.0
    elif 300 <= velocidade_internet <= 500:
        cobertura_total *= 1.2

    cobertura_total = max(0, min(100, cobertura_total))

    return cobertura_total

def main():
    st.title("Análise de Cobertura Wi-Fi")

    potencia_sinal = st.number_input("Potência do sinal (dBm):", -100, 0, 20)
    num_roteadores = st.number_input("Número de roteadores:", 1, 10, 1)
    paredes = st.number_input("Número total de paredes:", 0, 20, 8)
    tipo_paredes = st.selectbox("Tipo de paredes:", ["concreto", "azulejo", "metal", "nenhuma"])
    freq = st.number_input("Frequência (GHz):", 2.4, 5.0, 2.4, step=0.1)
    comprimento = st.number_input("Comprimento (m):", 1.0, 50.0, 10.0, step=0.1)
    largura = st.number_input("Largura (m):", 1.0, 50.0, 14.0, step=0.1)
    num_comodos = st.number_input("Número de cômodos:", 1, 50, 9)
    pos_roteador = st.selectbox("Posição do roteador:", ["meio", "fundo", "frente"])
    velocidade_internet = st.number_input("Velocidade da Internet (Mbps):", 10, 1000, 300)

    if st.button("Calcular"):
        cobertura_total = calcular_cobertura(
            potencia_sinal, num_roteadores, paredes, tipo_paredes,
            freq, comprimento, largura, num_comodos, pos_roteador, velocidade_internet
        )
        cobertura_por_comodo = cobertura_total / num_comodos if num_comodos > 0 else 0

        st.write(f"Cobertura Geral Estimada: {cobertura_total:.2f}%")
        st.write(f"Cobertura por Cômodo: {cobertura_por_comodo:.2f}%")

if __name__ == "__main__":
    main()
