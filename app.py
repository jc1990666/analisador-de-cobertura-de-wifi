import streamlit as st

def calcular_cobertura(metragem, localizacao, andares, num_quartos, num_banheiros, num_salas, num_cozinhas, area_externa, num_paredes, material_paredes, velocidade_mbps, frequencia, latencia_ms, upload_mbps):
    # Fatores de impacto
    fator_andar = 0.9 if andares > 1 else 1
    fator_paredes = 0.8 if material_paredes == 'Concreto' else 1
    fator_area_externa = 1.1 if area_externa else 1
    fator_frequencia = 0.8 if frequencia == '2.4 GHz' else 1.2

    # Ajuste da metragem e fatores
    ajuste_metragem = min(metragem / 375, 1)  # Ajuste para metragem de 25 x 15 metros
    cobertura_base = 100 * (velocidade_mbps / 1000) * fator_andar * fator_paredes * fator_area_externa * fator_frequencia

    # Ajuste baseado na latência e velocidade de upload
    fator_latencia = 0.8 if latencia_ms < 50 else 0.6  # Melhor desempenho com latência menor
    fator_upload = min(upload_mbps / 100, 1)  # Maximizar fator de upload

    # Cálculo da cobertura
    cobertura = cobertura_base * ajuste_metragem * fator_latencia * fator_upload

    return min(cobertura, 100)  # Garantir que a cobertura não exceda 100%

st.title("Analisador Avançado de Cobertura Wi-Fi")

st.header("1. Informações da Casa")
metragens = st.number_input("Metragem Quadrada da Casa (ex.: 375 para 25x15 metros):", min_value=1, value=375)
localizacao = st.selectbox("Localização do Roteador:", ["Meio", "Frente", "Fundo"])
andares = st.number_input("Número de Andares:", min_value=1, max_value=5, value=1)

st.header("2. Detalhes dos Cômodos")
num_quartos = st.number_input("Número de Quartos:", min_value=0, value=5)
num_banheiros = st.number_input("Número de Banheiros:", min_value=0, value=1)
num_salas = st.number_input("Número de Salas:", min_value=0, value=1)
num_cozinhas = st.number_input("Número de Cozinhas:", min_value=0, value=1)
area_externa = st.radio("A casa possui área externa?", ["Não", "Sim"]) == "Sim"

st.header("3. Características das Paredes")
num_paredes = st.number_input("Número de Paredes Matrizes (Divisórias Principais):", min_value=0, max_value=20, value=0)
material_paredes = st.selectbox("Material das Paredes:", ["Madeira", "Concreto", "Tijolo", "Drywall"])

st.header("4. Detalhes da Conexão")
velocidade_mbps = st.number_input("Velocidade Contratada (Mbps):", min_value=1, max_value=1000, value=100)
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])
latencia_ms = st.number_input("Latência (ms):", min_value=0, max_value=1000, value=7)
upload_mbps = st.number_input("Velocidade de Upload (Mbps):", min_value=0, max_value=1000, value=47)

st.header("5. Resultados da Análise")
cobertura = calcular_cobertura(metragens, localizacao, andares, num_quartos, num_banheiros, num_salas, num_cozinhas, area_externa, num_paredes, material_paredes, velocidade_mbps, frequencia, latencia_ms, upload_mbps)

st.write(f"Cobertura Estimada de Sinal Wi-Fi: {cobertura:.2f}%")

if cobertura < 30:
    st.warning("⚠️ A cobertura está abaixo do ideal. Recomendamos a instalação de um roteador adicional ou repetidor.")
    st.write("Posicione o roteador no centro da casa para melhorar a distribuição do sinal.")
    st.write("Considere adicionar repetidores, especialmente em áreas com muitas paredes ou em andares superiores.")
elif cobertura < 60:
    st.info("ℹ️ A cobertura está abaixo do ideal, mas pode ser adequada para a maioria dos usos. Considere otimizar o posicionamento do roteador e adicionar repetidores se necessário.")
else:
    st.success("✅ A cobertura está adequada. O roteador atual deve ser suficiente para a maioria dos usos.")

st.write("Disclaimer: Esta é uma estimativa básica e pode não refletir com precisão todos os fatores ambientais. Para resultados precisos, considere realizar uma análise de campo.")
