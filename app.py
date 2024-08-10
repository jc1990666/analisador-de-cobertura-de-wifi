import streamlit as st

def calcular_cobertura(metragem, num_paredes, frequencia):
    # Parâmetros de perda de sinal
    perda_por_parede = 3  # Perda padrão por parede em dB
    perda_frequencia = {
        '2.4 GHz': 3,  # Perda adicional em dB
        '5 GHz': 5  # Perda adicional em dB
    }
    
    # Fatores de impacto
    perda_frequencia_valor = perda_frequencia.get(frequencia, 0)
    
    # Cálculo da perda total de sinal
    perda_total = perda_por_parede * num_paredes + perda_frequencia_valor
    
    # Cálculo básico da cobertura de sinal
    cobertura_base = max(0, 100 - perda_total)  # Máximo de 100%
    
    # Ajuste baseado na metragem da casa
    cobertura = min(cobertura_base * (metragens / 350), 100)  # Max 100%

    return cobertura

st.title("Analisador de Cobertura Wi-Fi")

st.header("1. Informações da Casa")
comprimento = st.number_input("Comprimento da Casa (m):", min_value=1, value=10)
largura = st.number_input("Largura da Casa (m):", min_value=1, value=10)
metragens = comprimento * largura
st.write(f"Metragem da Casa: {metragens} m²")

st.header("2. Características das Paredes")
num_paredes = st.number_input("Número de Paredes Principais:", min_value=1, value=6)

st.header("3. Frequência da Internet")
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])

st.header("4. Resultado da Análise")
cobertura = calcular_cobertura(metragens, num_paredes, frequencia)

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
