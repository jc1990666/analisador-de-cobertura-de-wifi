import streamlit as st
import numpy as np
import pandas as pd

# Configurações iniciais da aplicação
st.set_page_config(
    page_title="Analisador de Cobertura Wi-Fi",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Analisador Avançado de Cobertura Wi-Fi")
st.markdown("""
Este aplicativo foi projetado para ajudar a estimar a cobertura de sinal Wi-Fi em uma casa, levando em consideração a planta baixa, materiais de construção, e outras variáveis que impactam a qualidade do sinal. 
Com isso, é possível fornecer recomendações detalhadas sobre a necessidade de pontos adicionais de acesso ou repetidores.
""")

# Seção 1: Entrada dos Dados da Casa
st.header("1. Informações da Casa")
metragem_total = st.number_input("Metragem Quadrada da Casa:", min_value=10, max_value=2000, step=1, help="Informe a área total da casa em metros quadrados.")
localizacao_roteador = st.selectbox("Localização do Roteador:", ["Meio", "Frente", "Fundos"], help="Escolha a localização onde o roteador será instalado.")
num_andares = st.slider("Número de Andares:", min_value=1, max_value=5, help="Número total de andares na casa.")

# Seção 2: Detalhes dos Cômodos
st.header("2. Detalhes dos Cômodos")
num_quartos = st.number_input("Número de Quartos:", min_value=1, max_value=20, step=1)
num_banheiros = st.number_input("Número de Banheiros:", min_value=1, max_value=10, step=1)
tem_area_externa = st.radio("A casa possui área externa?", ("Não", "Sim"))

# Seção 3: Características das Paredes
st.header("3. Características das Paredes")
num_paredes = st.slider("Número de Paredes Matrizes (Divisórias Principais):", min_value=0, max_value=20)
tipo_paredes = st.selectbox("Material das Paredes:", ["Concreto", "Tijolo", "Madeira", "Gesso"], help="Escolha o material predominante das paredes internas.")

# Seção 4: Detalhes da Internet
st.header("4. Detalhes da Conexão")
velocidade_internet = st.slider("Velocidade Contratada (Mbps):", min_value=1, max_value=1000, step=1)

# Funções de Cálculo
def calcular_perda_sinal(tipo_paredes, num_paredes):
    # Perda de sinal em dB baseada no tipo e quantidade de paredes
    perdas_por_material = {"Concreto": 12, "Tijolo": 8, "Madeira": 4, "Gesso": 2}
    perda_sinal = perdas_por_material[tipo_paredes] * num_paredes
    return perda_sinal

def calcular_cobertura(metragem_total, localizacao_roteador, perda_sinal, num_quartos, num_andares, tem_area_externa):
    # Cálculo da cobertura com base nos dados fornecidos
    base_cobertura = 100 - (metragem_total / 10) - (perda_sinal / 2) - (num_quartos * 2) - (num_andares * 5)
    
    # Ajustes baseados na localização do roteador
    if localizacao_roteador == 'Meio':
        base_cobertura += 10
    elif localizacao_roteador == 'Fundos':
        base_cobertura -= 10

    # Ajustes baseados na área externa
    if tem_area_externa == "Sim":
        base_cobertura -= 5
    
    return max(0, base_cobertura)

# Cálculo da Perda e Cobertura
perda_sinal = calcular_perda_sinal(tipo_paredes, num_paredes)
cobertura_estimada = calcular_cobertura(metragem_total, localizacao_roteador, perda_sinal, num_quartos, num_andares, tem_area_externa)

# Exibição dos Resultados
st.header("5. Resultados da Análise")
st.write(f"### Cobertura Estimada de Sinal Wi-Fi: **{cobertura_estimada:.2f}%**")

# Recomendações
if cobertura_estimada < 50:
    st.warning("⚠️ A cobertura está abaixo do ideal. Recomendamos a instalação de um roteador adicional ou repetidor.")
elif 50 <= cobertura_estimada < 75:
    st.info("ℹ️ A cobertura é razoável, mas pode ser melhorada com a instalação de um repetidor.")
else:
    st.success("✅ A cobertura está excelente! O roteador atual deve ser suficiente.")

# Exibindo recomendações detalhadas
st.subheader("Recomendações Detalhadas")
if cobertura_estimada < 50:
    st.write("""
    - **Posicionar o roteador no centro da casa**: Melhorar a distribuição do sinal.
    - **Adicionar repetidores**: Especialmente em áreas com muitas paredes ou em andares superiores.
    """)
elif 50 <= cobertura_estimada < 75:
    st.write("""
    - **Adicionar um repetidor**: Pode melhorar significativamente a cobertura.
    - **Considerar a instalação de um roteador mais potente**: Se a casa for grande ou tiver paredes espessas.
    """)
else:
    st.write("""
    - **Manter a configuração atual**: A cobertura está adequada para o uso diário.
    """)

# Footer
st.markdown("""
    **Disclaimer:** Esta é uma estimativa básica e pode não refletir com precisão todos os fatores ambientais. Para resultados precisos, considere realizar uma análise de campo.
""")
