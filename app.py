import streamlit as st

# Função para calcular a cobertura Wi-Fi
def calcular_cobertura(metragem, num_paredes, tipo_parede, frequencia, num_andares, num_roteadores, velocidade_contratada):
    perda_parede = {
        'Drywall (Gesso acartonado)': 2,
        'Concreto': 5,
        'Tijolo': 4,
        'Vidro': 3
    }
    
    perda_frequencia = {
        '2.4 GHz': 3,
        '5 GHz': 5
    }
    
    perda_parede_total = sum(perda_parede[tipo] for tipo in tipo_parede) * num_paredes
    perda_frequencia_valor = perda_frequencia.get(frequencia, 0)
    perda_total = perda_parede_total + perda_frequencia_valor
    
    # Fator de ajuste com base na quantidade de roteadores e velocidade contratada
    ajuste_roteadores = num_roteadores * 1.5
    ajuste_velocidade = min(velocidade_contratada / 100, 2.5)
    
    cobertura_base = max(0, 100 - perda_total) * ajuste_roteadores
    cobertura = min(cobertura_base * (metragem / 350), 100)
    cobertura = (cobertura / num_andares) * ajuste_velocidade
    
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
st.write("""
**Número de Paredes Mestras:** Mais paredes entre o roteador e os dispositivos podem reduzir o sinal Wi-Fi. Por exemplo, uma casa com várias divisões pode ter uma cobertura de sinal mais fraca.
""")
num_paredes = st.number_input("Número de Paredes Mestras:", min_value=1, value=1)

st.write("""
**Tipos de Paredes:** Diferentes tipos de paredes afetam o sinal de forma distinta:
- **Gesso acartonado (Drywall):** Menos bloqueio do sinal.
- **Concreto:** Bloqueio significativo do sinal.
- **Tijolo:** Bloqueio moderado do sinal.
- **Vidro:** Menos bloqueio, mas pode refletir o sinal.
""")
tipo_parede = st.multiselect(
    "Tipos de Paredes (selecione uma ou mais):",
    ["Drywall (Gesso acartonado)", "Concreto", "Tijolo", "Vidro"]
)

st.header("3. Frequência da Internet")
st.write("""
**Frequência do Roteador:** Impacta no alcance e velocidade:
- **2.4 GHz:** Melhor alcance e penetração em paredes.
- **5 GHz:** Maior velocidade, menor alcance.
""")
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])

st.header("4. Quantidade de Roteadores")
st.write("""
**Número de Roteadores:** Adicionar roteadores pode melhorar a cobertura em ambientes grandes.
""")
num_roteadores = st.number_input("Número de Roteadores no Ambiente:", min_value=1, value=1)

st.header("5. Velocidade da Internet Contratada")
st.write("""
**Velocidade da Internet (Mbps):** Influencia a qualidade da conexão. Valores mais altos garantem uma conexão mais estável e rápida.
""")
velocidade_contratada = st.slider("Velocidade da Internet Contratada (Mbps):", min_value=10, max_value=500, value=100, step=10)

st.header("6. Detalhes Adicionais")
st.write("""
**Número de Andares:** Mais andares podem reduzir o sinal. Ajustes adicionais podem ser necessários para melhor cobertura.
""")
num_andares = st.number_input("Número de Andares:", min_value=1, value=1)

st.header("7. Resultado da Análise")
cobertura = calcular_cobertura(metragem, num_paredes, tipo_parede, frequencia, num_andares, num_roteadores, velocidade_contratada)

cobertura_por_metro = cobertura / metragem

classificacao, icone = classificar_cobertura(cobertura_por_metro)

st.write(f"Cobertura Estimada de Sinal Wi-Fi: {cobertura:.2f}%")
st.write(f"Cobertura por Metro Quadrado: {cobertura_por_metro:.2f}% - {icone} {classificacao}")

if classificacao == "Baixa":
    st.warning("⚠️ A cobertura está baixa. Considere adicionar mais roteadores ou repetidores para melhorar a cobertura.")
    st.write("Posicione os roteadores em locais estratégicos e utilize repetidores Wi-Fi em áreas com sinal fraco para melhorar a cobertura.")
elif classificacao == "Boa":
    st.info("ℹ️ A cobertura está moderada. Pode ser suficiente, mas ajustar o posicionamento dos roteadores ou adicionar repetidores pode otimizar a cobertura.")
else:
    st.success("✅ A cobertura está ótima! A configuração atual deve atender bem às suas necessidades.")

st.write("Nota: Esta é uma estimativa. Para resultados mais precisos, consulte um especialista em redes.")
