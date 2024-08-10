import streamlit as st

def calcular_cobertura(metragem, andares, area_externa, material_paredes, velocidade_mbps, frequencia, latencia_ms, upload_mbps):
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

st.title("Analisador de Cobertura Wi-Fi")

st.header("Informações da Casa")
metragens = st.number_input("Metragem da Casa (em metros quadrados):", min_value=1, value=375)
andares = st.number_input("Número de Andares:", min_value=1, max_value=5, value=1)

st.header("Detalhes dos Cômodos")
area_externa = st.radio("A casa tem área externa?", ["Não", "Sim"]) == "Sim"

st.header("Características das Paredes")
material_paredes = st.selectbox("Material das Paredes:", ["Madeira", "Concreto", "Tijolo", "Drywall"])

st.header("Detalhes da Conexão")
velocidade_mbps = st.number_input("Velocidade da Internet (Mbps):", min_value=1, max_value=1000, value=300)
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])
latencia_ms = st.number_input("Latência (ms):", min_value=0, max_value=1000, value=7)
upload_mbps = st.number_input("Velocidade de Upload (Mbps):", min_value=0, max_value=1000, value=47)

st.header("Resultado")
cobertura = calcular_cobertura(metragens, andares, area_externa, material_paredes, velocidade_mbps, frequencia, latencia_ms, upload_mbps)

st.write(f"Cobertura Estimada de Sinal Wi-Fi: {cobertura:.2f}%")

if cobertura < 30:
    st.warning("⚠️ A cobertura está baixa. Considere adicionar um roteador ou repetidor.")
    st.write("Tente posicionar o roteador no centro da casa para melhor cobertura.")
    st.write("Adicionar repetidores pode ajudar, especialmente em áreas com muitas paredes.")
elif cobertura < 60:
    st.info("ℹ️ A cobertura está abaixo do ideal, mas pode ser suficiente para a maioria das pessoas.")
    st.write("Ajustar o posicionamento do roteador e considerar repetidores pode melhorar a cobertura.")
else:
    st.success("✅ A cobertura está boa. O roteador deve funcionar bem na maioria dos casos.")

st.write("Nota: Esta é uma estimativa. Para resultados mais precisos, considere uma análise profissional.")
