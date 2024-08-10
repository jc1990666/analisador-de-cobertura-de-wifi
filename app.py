import streamlit as st

# Função para calcular a cobertura Wi-Fi
def calcular_cobertura(metragem, num_paredes, tipo_parede, frequencia, num_andares, num_roteadores, velocidade_contratada):
    perda_parede = {
        'Drywall (Gesso acartonado)': 5,
        'Concreto': 15,
        'Tijolo': 10,
        'Vidro': 3
    }
    
    perda_frequencia = {
        '2.4 GHz': 10,
        '5 GHz': 20
    }
    
    perda_parede_total = sum(perda_parede.get(tipo, 0) for tipo in tipo_parede) * num_paredes
    perda_frequencia_valor = perda_frequencia.get(frequencia, 0)
    perda_total = perda_parede_total + perda_frequencia_valor
    
    # Ajusta a cobertura com base no número de roteadores e velocidade contratada
    ajuste_roteadores = num_roteadores * 10
    ajuste_velocidade = min(velocidade_contratada / 50, 10)
    
    cobertura_base = max(0, 100 - perda_total) * (1 + ajuste_roteadores / 100)
    cobertura = min(cobertura_base * (metragem / 300), 100)
    cobertura = cobertura * (num_andares / 2) * (ajuste_velocidade / 5)
    
    return cobertura

# Função para classificar a cobertura
def classificar_cobertura(cobertura):
    if cobertura < 30:
        return "Baixa", "⚠️"
    elif 30 <= cobertura < 70:
        return "Boa", "ℹ️"
    else:
        return "Ótima", "✅"

# Função para comparação
def comparacao_cobertura(cobertura):
    if cobertura < 30:
        comparacao = "A cobertura é baixa. Isso geralmente significa que há áreas significativas com sinal fraco ou inexistente."
    elif 30 <= cobertura < 70:
        comparacao = "A cobertura é boa. A maioria dos dispositivos deve funcionar bem, mas pode haver áreas com sinal mais fraco."
    else:
        comparacao = "A cobertura é ótima. O sinal Wi-Fi deve ser forte e confiável em toda a área."

    return comparacao

st.title("Analisador de Cobertura Wi-Fi")

st.header("1. Informações do Ambiente")
comprimento = st.number_input("Comprimento do Ambiente (m):", min_value=1, value=10)
largura = st.number_input("Largura do Ambiente (m):", min_value=1, value=10)
metragem = comprimento * largura
st.write(f"Metragem do Ambiente: {metragem} m²")

st.header("2. Características das Paredes")
st.write("""
**Número de Paredes Mestras:** Mais paredes entre o roteador e os dispositivos podem reduzir o sinal Wi-Fi. 
**Tipos de Paredes:** Diferentes tipos de paredes afetam o sinal de forma distinta:
- **Drywall (Gesso acartonado):** Menos bloqueio do sinal.
- **Concreto:** Bloqueio significativo do sinal.
- **Tijolo:** Bloqueio moderado do sinal.
- **Vidro:** Menos bloqueio, mas pode refletir o sinal.
""")
num_paredes = st.number_input("Número de Paredes Mestras:", min_value=1, value=1)
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

classificacao, icone = classificar_cobertura(cobertura)
comparacao = comparacao_cobertura(cobertura)

st.write(f"Cobertura Estimada de Sinal Wi-Fi: {cobertura:.2f}%")
st.write(f"Classificação: {icone} {classificacao}")
st.write(f"Comparação: {comparacao}")

if classificacao == "Baixa":
    st.warning("⚠️ A cobertura está baixa. Considere adicionar mais roteadores ou repetidores. Posicione os roteadores estrategicamente e considere usar repetidores em áreas com sinal fraco.")
elif classificacao == "Boa":
    st.info("ℹ️ A cobertura está moderada. A configuração atual pode ser suficiente, mas otimizar o posicionamento dos roteadores ou adicionar repetidores pode melhorar a cobertura.")
else:
    st.success("✅ A cobertura está ótima! A configuração atual deve atender bem às suas necessidades.")

st.write("Nota: Esta é uma estimativa. Para resultados mais precisos, consulte um especialista em redes.")
