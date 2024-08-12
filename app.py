import streamlit as st

def calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipo_paredes, freq, comprimento, largura, altura, num_andares, pos_roteador):
    # Definindo valores padrão
    sinal_base = 100  # Base de sinal padrão para cálculos

    # Ajuste baseado na quantidade de paredes e tipo de paredes
    perdas_por_parede = {
        'alvenaria': 10,
        'metal': 15,
        'plastico_isolante': 5,
        'vidro': 3
    }
    
    perda_por_parede = perdas_por_parede.get(tipo_paredes, 5)
    sinal_base -= paredes * perda_por_parede
    
    # Ajuste baseado na frequência
    if freq == 2.4:
        sinal_base += 15  # Melhor penetração em obstáculos
    elif freq == 5:
        sinal_base -= 10  # Menor penetração, maior interferência

    # Ajuste baseado na posição do roteador
    if pos_roteador == 'meio':
        sinal_base += 10
    elif pos_roteador == 'fundo':
        sinal_base -= 5
    elif pos_roteador == 'frente':
        sinal_base += 5

    # Ajuste baseado no número de roteadores
    sinal_base += num_roteadores * 10

    # Ajuste baseado no número de andares
    sinal_base -= num_andares * 10  # Cada andar adicional reduz a cobertura

    # Ajuste baseado na área total e altura
    area_total = comprimento * largura
    volume_total = area_total * altura
    cobertura_total = max(0, sinal_base - (volume_total / 100))  # Ajuste para refletir a dispersão do sinal no volume

    return cobertura_total

# Interface Streamlit
def main():
    st.title("Análise de Cobertura Wi-Fi")
    
    st.write("Este cálculo considera ambientes com múltiplos andares e diferentes alturas de pé-direito.")

    # Parâmetros de entrada
    freq = st.selectbox("Frequência (GHz):", [2.4, 5])
    comprimento = st.number_input("Comprimento do ambiente (m):", 1, 100, 10)
    largura = st.number_input("Largura do ambiente (m):", 1, 100, 10)
    altura = st.number_input("Altura do pé-direito (m):", 1, 10, 2.5)
    num_andares = st.number_input("Número de andares (incluindo 0 para ambiente sem andares):", 0, 10, 1)
    paredes = st.number_input("Número total de paredes:", 0, 20, 8)
    tipo_paredes = st.selectbox("Tipo de paredes:", ['alvenaria', 'metal', 'plastico_isolante', 'vidro'])
    num_roteadores = st.number_input("Número de roteadores:", 1, 10, 1)
    pos_roteador = st.selectbox("Posição do roteador:", ['meio', 'frente', 'fundo'])

    # Cálculo da cobertura
    cobertura_total = calcular_cobertura(-100, num_roteadores, paredes, tipo_paredes, freq, comprimento, largura, altura, num_andares, pos_roteador)
    st.write(f'Cobertura Geral Estimada: {cobertura_total:.2f}%')

    # Cobertura por cômodo
    def cobertura_por_comodo(cobertura_total, num_comodos):
        if num_comodos == 0:
            return 0
        return cobertura_total / num_comodos

    num_comodos = st.number_input("Número de cômodos:", 1, 20, 1)

    for i in range(1, num_comodos + 1):
        cobertura = cobertura_por_comodo(cobertura_total, num_comodos)
        st.write(f'Cobertura no Cômodo {i}: {cobertura:.2f}%')

if __name__ == "__main__":
    main()
