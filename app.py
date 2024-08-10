import streamlit as st

def calcular_cobertura(metragem, area_externa, material_paredes, velocidade_download_mbps, frequencia):
    # Parâmetros de perda de sinal
    perda_por_parede = {
        'Madeira': 1,
        'Concreto': 4,
        'Tijolo': 3,
        'Drywall': 2
    }
    
    perda_frequencia = {
        '2.4 GHz': 3,
        '5 GHz': 5
    }
    
    # Fatores de impacto
    perda_material = perda_por_parede.get(material_paredes, 0)
    perda_frequencia = perda_frequencia.get(frequencia, 0)
    perda_area_externa = 1.1 if area_externa else 1
    
    # Cálculo básico da cobertura de sinal
    cobertura_base = (velocidade_download_mbps / 300) * (100 - perda_material - perda_frequencia) * perda_area_externa
    
    # Ajuste baseado na metragem
    cobertura = min(cobertura_base * (metragens / 350), 100)  # Max 100%

    return cobertura

st.title("Analisador de Cobertura Wi-Fi")

st.header("1. Informações da Casa")
comprimento = st.number_input("Comprimento da Casa (m):", min_value=1, value=10)
largura = st.number_input("Largura da Casa (m):", min_value=1, value=10)
metragens = comprimento * largura
st.write(f"Metragem da Casa: {metragens} m²")

st.header("2. Características das Paredes")
area_externa = st.radio("A casa tem área externa?", ["Não", "Sim"])
material_paredes = st.selectbox("Material das Paredes:", ["Madeira", "Concreto", "Tijolo", "Drywall"])

st.header("3. Detalhes da Conexão")
velocidade_download_mbps = st.number_input("Velocidade de Download (Mbps):", min_value=1, max_value=1000, value=124)
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])

st.header("4. Resultado da Análise")
cobertura = calcular_cobertura(metragens, area_externa == "Sim", material_paredes, velocidade_download_mbps, frequencia)

st.write(f"Cobertura Estimada de Sinal Wi-Fi: {cobertura:.2f}%")

if cobertura < 30:
    st.warning("⚠️ A cobertura está baixa. Considere adicionar um roteador ou repetidor.")
    st.write("Para melhorar a cobertura, posicione o roteador no centro da casa e adicione repetidores se necessário.")
elif cobertura < 60:
    st.info("ℹ️ A cobertura está moderada. Pode ser suficiente, mas você pode otimizar o posicionamento do roteador e considerar repetidores.")
else:
    st.success("✅ A cobertura está boa! Seu roteador deve estar atendendo bem à casa.")

st.write("""
    🎉 **Dica Divertida:** Se a cobertura está parecendo fraca, imagine que o sinal do Wi-Fi é como uma bolha mágica que precisa de espaço para se espalhar! Posicionar o roteador no centro da casa é como colocar a bolha no meio do espaço, e os repetidores são como pequenos ajudantes mágicos que garantem que a bolha alcance todos os cantinhos!
    Com essas dicas, você vai garantir que seu Wi-Fi seja tão forte quanto um super-herói! 🚀📶
""")

st.write("Nota: Esta é uma estimativa. Para resultados mais precisos, consulte um especialista em redes.")
