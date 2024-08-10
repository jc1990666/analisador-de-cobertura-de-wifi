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
    ajuste_roteadores = num_roteadores * 1.5  # Assumindo que cada roteador adicional aumenta a cobertura em 50%
    ajuste_velocidade = min(velocidade_contratada / 100, 5)  # Assume que velocidades acima de 100 Mbps têm menos impacto adicional
    
    cobertura_base = max(0, (100 - perda_total) * ajuste_roteadores)
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
**Número de Paredes Mestras:** Paredes podem interferir no sinal Wi-Fi. Quanto mais paredes houver entre o roteador e os dispositivos, maior será a perda de sinal. Por exemplo, em uma casa grande ou escritório com muitas divisões, o sinal pode ter dificuldades para alcançar todos os pontos.
""")
num_paredes = st.number_input("Número de Paredes Mestras:", min_value=1, value=1)

st.write("""
**Tipos de Paredes:** Diferentes tipos de parede podem interferir no sinal Wi-Fi de maneiras diferentes. Veja os exemplos:
- **Gesso acartonado (Drywall):** Um tipo de parede comum em construções modernas. Ela não bloqueia tanto o sinal quanto paredes de concreto ou tijolo, mas ainda pode reduzir a força do Wi-Fi.
- **Concreto:** Paredes de concreto são densas e podem bloquear grande parte do sinal Wi-Fi. Se sua casa ou prédio tem muitas dessas paredes, você pode precisar de repetidores.
- **Tijolo:** Embora os tijolos também sejam densos, eles bloqueiam menos o sinal em comparação ao concreto, mas ainda causam alguma perda de força.
- **Vidro:** Paredes de vidro bloqueiam menos o sinal, mas ainda podem refletir e dispersar o Wi-Fi, especialmente em paredes espessas.
""")
tipo_parede = st.multiselect(
    "Tipos de Paredes (selecione uma ou mais):",
    ["Drywall (Gesso acartonado)", "Concreto", "Tijolo", "Vidro"]
)

st.header("3. Frequência da Internet")
st.write("""
**Frequência da Internet:** A escolha da frequência do roteador pode afetar a cobertura:
- **2.4 GHz:** Frequência que oferece maior alcance e melhor penetração em obstáculos como paredes. Ideal para áreas maiores ou com muitas divisões.
- **5 GHz:** Frequência que oferece velocidades mais rápidas, mas com menor alcance. Melhor para ambientes mais abertos ou onde a velocidade é prioritária.
""")
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])

st.header("4. Quantidade de Roteadores")
st.write("""
**Número de Roteadores:** Mais roteadores no ambiente podem melhorar significativamente a cobertura, especialmente em casas ou edifícios grandes. Um roteador adicional pode ajudar a cobrir áreas onde o sinal é fraco.
""")
num_roteadores = st.number_input("Número de Roteadores no Ambiente:", min_value=1, value=1)

st.header("5. Velocidade da Internet Contratada")
st.write("""
**Velocidade da Internet:** A velocidade contratada (em Mbps) influencia a qualidade e a estabilidade da sua conexão. Se você tem uma internet mais rápida, poderá ter uma experiência melhor, especialmente em atividades que exigem alta velocidade, como streaming e jogos online.
""")
velocidade_contratada = st.slider("Velocidade da Internet Contratada (Mbps):", min_value=10, max_value=500, value=100, step=10)

st.header("6. Detalhes Adicionais")
st.write("""
**Número de Andares:** Se sua casa ou edifício tem mais de um andar, o sinal Wi-Fi pode enfraquecer ao subir ou descer entre os andares. Nesses casos, um roteador mais potente ou repetidores Wi-Fi podem ser necessários.
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
    st.write("Posicione os roteadores estrategicamente para maximizar o alcance, e considere utilizar repetidores Wi-Fi para áreas com sinal fraco.")
elif classificacao == "Boa":
    st.info("ℹ️ A cobertura está moderada. Pode ser suficiente, mas ajustes no posicionamento dos roteadores ou a adição de repetidores podem otimizar ainda mais a cobertura.")
else:
    st.success("✅ A cobertura está ótima! A configuração atual deve atender bem às suas necessidades.")

st.write("Nota: Esta é uma estimativa. Para resultados mais precisos, consulte um especialista em redes.")
