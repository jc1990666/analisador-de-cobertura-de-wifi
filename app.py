import streamlit as st

def calcular_cobertura(metragem, area_externa, material_paredes, velocidade_download_mbps, velocidade_upload_mbps, frequencia):
    # Fatores de impacto
    fator_area_externa = 1.1 if area_externa else 1
    fator_paredes = 0.8 if material_paredes == 'Concreto' else 1
    fator_frequencia = 0.8 if frequencia == '2.4 GHz' else 1.2

    # Cálculo básico da cobertura de sinal
    cobertura_base = 100 * (velocidade_download_mbps / 1000) * fator_paredes * fator_area_externa * fator_frequencia

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
velocidade_download_mbps = st.number_input("Velocidade de Download (Mbps):", min_value=1, max_value=1000, format="%f", value=124.12)
velocidade_upload_mbps = st.number_input("Velocidade de Upload (Mbps):", min_value=1, max_value=1000, format="%f", value=52.18)
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])

st.header("4. Resultado da Análise")
cobertura = calcular_cobertura(metragens, area_externa == "Sim", material_paredes, velocidade_download_mbps, velocidade_upload_mbps, frequencia)

st.write(f"Cobertura Estimada de Sinal Wi-Fi: {cobertura:.2f}%")

if cobertura < 30:
    st.warning("⚠️ A cobertura está baixa. Considere adicionar um roteador ou repetidor.")
    st.write("Para uma internet mais estável, tente posicionar o roteador no centro da casa. Repetidores podem ser seus aliados, especialmente se a sua casa tem muitas paredes.")
elif cobertura < 60:
    st.info("ℹ️ A cobertura está moderada. Pode ser suficiente, mas você pode querer otimizar o posicionamento do roteador e adicionar repetidores se necessário.")
else:
    st.success("✅ A cobertura está ótima! Seu roteador atual deve estar dando conta do recado.")

st.write("""
    🎉 **Dica Divertida:** Se a sua cobertura está parecendo um pouco fraca, imagine que o sinal do Wi-Fi é como um superpoder! Você quer garantir que esse superpoder alcance todos os cantinhos da sua casa. Posicionar o roteador no centro é como colocar um super-herói no meio da ação, e adicionar repetidores é como ter assistentes superpoderosos para ajudar! 
    Não se preocupe, todos nós já estivemos lá. Com essas dicas, você vai garantir que seu Wi-Fi esteja em forma de campeão! 🚀📶
""")

st.write("Nota: Esta é uma estimativa. Para uma análise ainda mais precisa, considere consultar um especialista em redes.")
