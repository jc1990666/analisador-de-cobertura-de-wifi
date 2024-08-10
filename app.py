import streamlit as st

def calcular_cobertura(metragem, area_externa, material_paredes, velocidade_mbps, frequencia):
    # Fatores de impacto
    fator_area_externa = 1.1 if area_externa else 1
    fator_paredes = 0.8 if material_paredes == 'Concreto' else 1
    fator_frequencia = 0.8 if frequencia == '2.4 GHz' else 1.2

    # Cálculo básico da cobertura de sinal
    cobertura_base = 100 * (velocidade_mbps / 1000) * fator_paredes * fator_area_externa * fator_frequencia

    # Ajuste baseado na metragem
    cobertura = min(cobertura_base * (metragens / 350), 100)  # Max 100%

    return cobertura

st.title("Analisador de Cobertura Wi-Fi")

st.header("1. Informações da Casa")
metragens = st.number_input("Metragem da Casa (m²):", min_value=0, value=375)
area_externa = st.radio("A casa tem área externa?", ["Não", "Sim"])

st.header("2. Características das Paredes")
material_paredes = st.selectbox("Material das Paredes:", ["Madeira", "Concreto", "Tijolo", "Drywall"])

st.header("3. Detalhes da Conexão")
velocidade_mbps = st.number_input("Velocidade da Internet (Mbps):", min_value=1, max_value=1000, value=300)
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])

st.header("4. Resultado da Análise")
cobertura = calcular_cobertura(metragens, area_externa == "Sim", material_paredes, velocidade_mbps, frequencia)

st.write(f"Cobertura Estimada de Sinal Wi-Fi: {cobertura:.2f}%")

if cobertura < 30:
    st.warning("⚠️ A cobertura está baixa. Considere adicionar um roteador ou repetidor.")
    st.write("Tente posicionar o roteador no centro da casa para melhor cobertura.")
    st.write("Adicionar repetidores pode ajudar em áreas com muitas paredes.")
elif cobertura < 60:
    st.info("ℹ️ A cobertura está moderada. Pode ser adequada, mas considere otimizar o posicionamento do roteador e adicionar repetidores.")
else:
    st.success("✅ A cobertura está boa. O roteador atual deve ser suficiente.")

st.write("Nota: Esta é uma estimativa. Para resultados mais precisos, considere uma análise profissional.")
