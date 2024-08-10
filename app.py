import streamlit as st
import pickle
import os

# Função para calcular a cobertura Wi-Fi
def calcular_cobertura(metragem, num_paredes, frequencia, num_comodos, num_andares):
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
    
    # Ajuste para quantidade de cômodos e andares
    cobertura /= num_andares  # Divida a cobertura por andares
    cobertura_comodos = cobertura / num_comodos  # Distribuir a cobertura entre os cômodos
    
    return cobertura, cobertura_comodos

# Função para atualizar o modelo de auto-aprendizado
def atualizar_modelo(dados):
    if os.path.exists("modelo.pkl"):
        with open("modelo.pkl", "rb") as f:
            modelo = pickle.load(f)
    else:
        modelo = {"total_casos": 0, "soma_cobertura": 0}
    
    modelo["total_casos"] += 1
    modelo["soma_cobertura"] += dados["cobertura"]
    
    with open("modelo.pkl", "wb") as f:
        pickle.dump(modelo, f)

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

st.header("4. Detalhes Adicionais")
num_comodos = st.number_input("Número de Cômodos:", min_value=1, value=5)
num_andares = st.number_input("Número de Andares:", min_value=1, value=1)

st.header("5. Resultado da Análise")
cobertura, cobertura_comodos = calcular_cobertura(metragens, num_paredes, frequencia, num_comodos, num_andares)

st.write(f"Cobertura Estimada de Sinal Wi-Fi Total: {cobertura:.2f}%")
st.write(f"Cobertura Estimada de Sinal Wi-Fi por Cômodo: {cobertura_comodos:.2f}%")

# Atualizar o modelo de auto-aprendizado com os dados do usuário
dados = {"cobertura": cobertura}
atualizar_modelo(dados)

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
