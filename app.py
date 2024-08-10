import streamlit as st
import pickle
import os

# Função para calcular a cobertura Wi-Fi
def calcular_cobertura(metragem, num_paredes, tipo_parede, frequencia, num_andares):
    # Parâmetros de perda de sinal baseados em tipos de paredes
    perda_parede = {
        'Drywall': 2,  # Perda padrão por parede em dB
        'Concreto': 5,  # Perda padrão por parede em dB
        'Tijolo': 4,  # Perda padrão por parede em dB
        'Vidro': 3  # Perda padrão por parede em dB
    }
    
    # Parâmetros de perda de sinal baseados em frequências
    perda_frequencia = {
        '2.4 GHz': 3,  # Perda adicional em dB
        '5 GHz': 5  # Perda adicional em dB
    }
    
    # Calculando a perda de sinal com base nas paredes
    perda_parede_total = sum(perda_parede[tipo] for tipo in tipo_parede) * num_paredes
    
    # Calculando a perda de sinal com base na frequência
    perda_frequencia_valor = perda_frequencia.get(frequencia, 0)
    
    # Cálculo da perda total de sinal
    perda_total = perda_parede_total + perda_frequencia_valor
    
    # Cálculo básico da cobertura de sinal
    cobertura_base = max(0, 100 - perda_total)  # Máximo de 100%
    
    # Ajuste baseado na metragem do ambiente
    cobertura = min(cobertura_base * (metragem / 350), 100)  # Max 100%
    
    # Ajuste para número de andares
    cobertura /= num_andares  # Divida a cobertura por andares
    
    return cobertura

# Função para classificar a cobertura por metro quadrado
def classificar_cobertura(cobertura_por_metro):
    if cobertura_por_metro < 30:
        return "Baixa", "⚠️"
    elif 30 <= cobertura_por_metro <= 60:
        return "Boa", "ℹ️"
    else:
        return "Ótima", "✅"

st.title("Analisador de Cobertura Wi-Fi")

st.header("1. Informações do Ambiente")
comprimento = st.number_input("Comprimento do Ambiente (m):", min_value=1, value=10)
largura = st.number_input("Largura do Ambiente (m):", min_value=1, value=10)
metragem = comprimento * largura
st.write(f"Metragem do Ambiente: {metragem} m²")

st.header("2. Características das Paredes")
num_paredes = st.number_input("Número de Paredes Mestras:", min_value=1, value=1)

tipo_parede = st.multiselect(
    "Tipos de Paredes (selecione uma ou mais):",
    ["Drywall", "Concreto", "Tijolo", "Vidro"]
)

st.header("3. Frequência da Internet")
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])

st.header("4. Detalhes Adicionais")
num_andares = st.number_input("Número de Andares:", min_value=1, value=1)

st.header("5. Resultado da Análise")
cobertura = calcular_cobertura(metragem, num_paredes, tipo_parede, frequencia, num_andares)

# Calcular a cobertura por metro quadrado
cobertura_por_metro = cobertura / metragem

# Classificar a cobertura
classificacao, icone = classificar_cobertura(cobertura_por_metro)

st.write(f"Cobertura Estimada de Sinal Wi-Fi: {cobertura:.2f}%")
st.write(f"Cobertura por Metro Quadrado: {cobertura_por_metro:.2f}% - {icone} {classificacao}")

# Sugestões com base na classificação
if classificacao == "Baixa":
    st.warning("⚠️ A cobertura está baixa. Considere adicionar um roteador ou repetidor.")
    st.write("Para melhorar a cobertura, posicione o roteador no centro do ambiente e adicione repetidores se necessário.")
elif classificacao == "Boa":
    st.info("ℹ️ A cobertura está moderada. Pode ser suficiente, mas você pode otimizar o posicionamento do roteador e considerar repetidores.")
else:
    st.success("✅ A cobertura está ótima! Seu roteador deve estar atendendo bem ao ambiente.")

st.write("Nota: Esta é uma estimativa. Para resultados mais precisos, consulte um especialista em redes.")
