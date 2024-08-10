import streamlit as st

# Função para calcular a cobertura Wi-Fi
def calcular_cobertura(potencia_sinal, num_roteadores, comprimento, largura, num_comodos):
    # Exemplo simples de cálculo de cobertura (ajuste conforme necessário)
    area_total = comprimento * largura
    cobertura_base = potencia_sinal / 100  # Simplificação para exemplo
    cobertura_total = min(100, cobertura_base * num_roteadores)
    cobertura_por_comodo = max(0, cobertura_total / num_comodos)
    return cobertura_total, cobertura_por_comodo

# Título do aplicativo
st.title("Análise de Cobertura Wi-Fi")

# Entrada de dados pelo usuário
frequencia = st.selectbox("Frequência (GHz)", [2.4, 5])
comprimento = st.number_input("Comprimento (m)", min_value=1.0, step=0.1)
largura = st.number_input("Largura (m)", min_value=1.0, step=0.1)
num_comodos = st.number_input("Número de cômodos", min_value=1, step=1)
num_andares = st.number_input("Número de andares", min_value=1, step=1)
num_paredes = st.number_input("Número total de paredes", min_value=0, step=1)
tipo_paredes = st.selectbox("Tipo de paredes", ["concreto", "madeira", "drywall"])
potencia_sinal = st.number_input("Potência do sinal (dBm)", min_value=-100, max_value=100, step=1)
posicao_roteador = st.selectbox("Posição do roteador", ["meio", "canto"])
num_roteadores = st.number_input("Quantidade de roteadores", min_value=1, step=1)
internet_contratada = st.number_input("Quantidade de internet contratada (Mbps)", min_value=1, step=1)

# Calculando a cobertura
cobertura_total, cobertura_por_comodo = calcular_cobertura(potencia_sinal, num_roteadores, comprimento, largura, num_comodos)

# Exibindo resultados
st.subheader("Resultados da Análise")
st.write(f"Área total da casa: {comprimento * largura:.2f} m²")
st.write(f"Número total de cômodos: {num_comodos}")
st.write(f"Número total de paredes: {num_paredes}")
st.write(f"Potência do sinal: {potencia_sinal} dBm")
st.write(f"Posição do roteador: {posicao_roteador}")
st.write(f"Quantidade de roteadores: {num_roteadores}")
st.write(f"Quantidade de internet contratada: {internet_contratada} Mbps")
st.write(f"Cobertura geral estimada: {cobertura_total:.2f}%")

for i in range(1, num_comodos + 1):
    st.write(f"Cobertura na Cômodo {i}: {cobertura_por_comodo:.2f}%")

st.write("Considerações Finais:")
st.write("A cobertura Wi-Fi é moderada. Para alcançar uma melhor cobertura, considere a instalação de mais roteadores ou a melhoria do posicionamento dos mesmos.")
