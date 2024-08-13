import streamlit as st

def calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipos_paredes, freq, comprimento, largura, num_comodos, pos_roteador, num_andares):
    # Definindo valores padrão
    sinal_base = 100  # Base de sinal padrão para cálculos

    # Ajuste baseado na quantidade e tipo de paredes
    perda_por_parede = 0
    for tipo_parede in tipos_paredes:
        if tipo_parede == 'vidro':
            perda_por_parede += 1
        elif tipo_parede == 'PVC':
            perda_por_parede += 2
        elif tipo_parede == 'alvenaria':
            perda_por_parede += 5
        elif tipo_parede == 'madeira':
            perda_por_parede += 3
        elif tipo_parede == 'metal':
            perda_por_parede += 7
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

    # Ajuste baseado na área total
    area_total = comprimento * largura
    cobertura_total = max(0, sinal_base - (area_total / 50))  # Ajuste para refletir a dispersão do sinal

    return cobertura_total

# Interface Streamlit
def main():
    st.set_page_config(page_title="Análise de Cobertura Wi-Fi", page_icon=":wifi:", layout="wide", initial_sidebar_state="expanded")
    st.title("Análise de Cobertura Wi-Fi")
    
    st.write("Utilize este cálculo para estimar a cobertura Wi-Fi considerando vários tipos de paredes e andares.")

    # Parâmetros de entrada
    freq = st.selectbox("Frequência (GHz):", [2.4, 5])
    comprimento = st.number_input("Comprimento do ambiente (m):", 1, 100, 10)
    largura = st.number_input("Largura do ambiente (m):", 1, 100, 10)
    num_andares = st.number_input("Número de andares:", 1, 10, 1)
    paredes = st.number_input("Número total de paredes:", 0, 20, 8)
    tipos_paredes = st.multiselect("Tipos de paredes:", ['vidro', 'PVC', 'alvenaria', 'madeira', 'metal'])
    num_roteadores = st.number_input("Número de roteadores:", 1, 10, 1)
    pos_roteador = st.selectbox("Posição do roteador:", ['meio', 'frente', 'fundo'])

    # Cálculo da cobertura
    cobertura_total = calcular_cobertura(-100, num_roteadores, paredes, tipos_paredes, freq, comprimento, largura, paredes, pos_roteador, num_andares)
    st.write(f'Cobertura Geral Estimada: {cobertura_total:.2f}%')

    # Cobertura por cômodo
    def cobertura_por_comodo(cobertura_total, num_comodos):
        if num_comodos == 0:
            return 0
        return cobertura_total / num_comodos

    for i in range(1, paredes + 1):
        cobertura = cobertura_por_comodo(cobertura_total, paredes)
        st.write(f'Cobertura na Cômodo {i}: {cobertura:.2f}%')

if __name__ == "__main__":
    main()
