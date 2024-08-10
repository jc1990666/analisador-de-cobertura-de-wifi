import streamlit as st

# Função para calcular a perda de sinal com base no tipo de parede
def calcular_perda_sinal(tipo_paredes, num_paredes):
    perdas_por_material = {"Concreto": 20, "Tijolo": 15, "Madeira": 7, "Gesso": 5}
    perda_sinal = perdas_por_material.get(tipo_paredes, 0) * num_paredes
    return perda_sinal

# Função para calcular a cobertura estimada de sinal Wi-Fi
def calcular_cobertura(metragem_total, localizacao_roteador, perda_sinal, num_quartos, num_banheiros, num_salas, num_cozinhas, num_andares, tem_area_externa, frequencia):
    # Ajustar perda base com base na metragem
    perda_base = 100 - (metragem_total / 15) - perda_sinal
    
    # Ajuste com base no número de cômodos e andares
    perda_base += (num_quartos * 2) + (num_banheiros * 2) + (num_salas * 2) + (num_cozinhas * 2) + (num_andares * 10)
    
    # Ajuste para área externa
    perda_base -= 10 if tem_area_externa == "Sim" else 0
    
    # Ajuste para frequência da internet
    perda_base -= 10 if frequencia == "5 GHz" else 0
    
    # Garantir que a perda esteja dentro dos limites 0-100%
    cobertura_final = max(0, min(100, perda_base))
    return cobertura_final

# Título do Aplicativo
st.title("Analisador Avançado de Cobertura Wi-Fi")

# Seção para Informações da Casa
st.header("1. Informações da Casa")
metragem_total = st.number_input("Metragem Quadrada da Casa:", min_value=10, max_value=2000, step=1, value=300, help="Informe a área total da casa em metros quadrados.")
localizacao_roteador = st.selectbox("Localização do Roteador:", ["Meio", "Frente", "Fundos"], help="Escolha a localização onde o roteador será instalado.")
num_andares = st.slider("Número de Andares:", min_value=1, max_value=5, help="Número total de andares na casa.", value=1)

# Seção para Detalhes dos Cômodos
st.header("2. Detalhes dos Cômodos")
num_quartos = st.number_input("Número de Quartos:", min_value=1, max_value=20, step=1, value=1)
num_banheiros = st.number_input("Número de Banheiros:", min_value=1, max_value=10, step=1, value=1)
num_salas = st.number_input("Número de Salas:", min_value=0, max_value=10, step=1, value=0)
num_cozinhas = st.number_input("Número de Cozinhas:", min_value=0, max_value=5, step=1, value=0)
tem_area_externa = st.radio("A casa possui área externa?", ("Não", "Sim"))

# Seção para Características das Paredes
st.header("3. Características das Paredes")
num_paredes = st.slider("Número de Paredes Matrizes (Divisórias Principais):", min_value=0, max_value=20, value=0)
tipo_paredes = st.selectbox("Material das Paredes:", ["Concreto", "Tijolo", "Madeira", "Gesso"], help="Escolha o material predominante das paredes internas.")

# Seção para Detalhes da Conexão
st.header("4. Detalhes da Conexão")
velocidade_internet = st.slider("Velocidade Contratada (Mbps):", min_value=1, max_value=1000, step=1, value=100)
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"], help="Selecione a frequência da sua conexão Wi-Fi.")

# Cálculo da Perda de Sinal e Cobertura
perda_sinal = calcular_perda_sinal(tipo_paredes, num_paredes)
cobertura_estimada = calcular_cobertura(metragem_total, localizacao_roteador, perda_sinal, num_quartos, num_banheiros, num_salas, num_cozinhas, num_andares, tem_area_externa, frequencia)

# Resultados da Análise
st.header("5. Resultados da Análise")
st.write(f"### Cobertura Estimada de Sinal Wi-Fi: **{cobertura_estimada:.2f}%**")

# Recomendações Detalhadas
if cobertura_estimada < 50:
    st.warning("⚠️ A cobertura está abaixo do ideal. Recomendamos a instalação de um roteador adicional ou repetidor.")
    st.write("""
    - **Posicionar o roteador no centro da casa**: Melhorar a distribuição do sinal.
    - **Adicionar repetidores**: Especialmente em áreas com muitas paredes ou em andares superiores.
    """)
elif 50 <= cobertura_estimada < 75:
    st.info("ℹ️ A cobertura é razoável, mas pode ser melhorada com a instalação de um repetidor.")
    st.write("""
    - **Adicionar um repetidor**: Pode melhorar significativamente a cobertura.
    - **Considerar a instalação de um roteador mais potente**: Se a casa for grande ou tiver paredes espessas.
    """)
else:
    st.success("✅ A cobertura está boa! O roteador atual deve ser suficiente.")
    st.write("""
    - **Manter a configuração atual**: A cobertura está adequada para o uso diário.
    """)

st.write("Disclaimer: Esta é uma estimativa básica e pode não refletir com precisão todos os fatores ambientais. Para resultados precisos, considere realizar uma análise de campo.")
