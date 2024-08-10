import streamlit as st

# Função para calcular a cobertura Wi-Fi
def calcular_cobertura(metragem, num_paredes, tipo_parede, frequencia, num_andares):
    perda_parede = {
        'Drywall': 2,
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
    
    cobertura_base = max(0, 100 - perda_total)
    cobertura = min(cobertura_base * (metragem / 350), 100)
    cobertura /= num_andares
    
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
**Número de Paredes Mestras:** Paredes afetam significativamente a propagação do sinal Wi-Fi. Quanto mais paredes houver entre o roteador e os dispositivos, maior será a perda de sinal. Se você estiver em um ambiente com muitas divisões, como em um escritório ou uma casa grande, o sinal pode ter dificuldades para alcançar todos os cantos.
""")
num_paredes = st.number_input("Número de Paredes Mestras:", min_value=1, value=1)

st.write("""
**Tipos de Paredes:** Diferentes materiais de parede têm diferentes níveis de interferência no sinal Wi-Fi. Aqui estão alguns exemplos:
- **Drywall:** Comum em residências modernas, drywall bloqueia o sinal de forma moderada. Se suas paredes são de drywall, você pode esperar uma boa penetração do sinal, mas não ideal.
- **Concreto:** Paredes de concreto são muito densas e podem bloquear grande parte do sinal Wi-Fi. Se você tiver muitas dessas paredes, considere utilizar repetidores de sinal.
- **Tijolo:** Tijolos são densos, mas não tanto quanto o concreto. Eles ainda bloqueiam o sinal, mas de forma menos severa.
- **Vidro:** Paredes de vidro interferem menos no sinal, mas ainda assim podem refletir e dispersar o Wi-Fi, dependendo do tamanho e da espessura.
""")
tipo_parede = st.multiselect(
    "Tipos de Paredes (selecione uma ou mais):",
    ["Drywall", "Concreto", "Tijolo", "Vidro"]
)

st.header("3. Frequência da Internet")
st.write("""
**Frequência da Internet:** A frequência do seu roteador Wi-Fi tem um grande impacto na cobertura:
- **2.4 GHz:** Esta frequência tem um alcance maior e penetra melhor em paredes e outros obstáculos. No entanto, ela tem uma velocidade de dados mais baixa em comparação com a 5 GHz. Se você precisa de cobertura em uma área grande e com muitas paredes, essa pode ser a melhor escolha.
- **5 GHz:** Esta frequência oferece velocidades de dados mais rápidas, mas tem um alcance menor e menos penetração em obstáculos como paredes. É ideal para ambientes mais abertos ou para áreas pequenas onde a velocidade é uma prioridade.
""")
frequencia = st.selectbox("Frequência da Internet:", ["2.4 GHz", "5 GHz"])

st.header("4. Detalhes Adicionais")
st.write("""
**Número de Andares:** Se sua casa ou edifício tem mais de um andar, o sinal Wi-Fi pode enfraquecer significativamente ao subir ou descer um nível. Nesse caso, você pode precisar de um roteador mais potente ou de repetidores Wi-Fi em cada andar.
""")
num_andares = st.number_input("Número de Andares:", min_value=1, value=1)

st.header("5. Resultado da Análise")
cobertura = calcular_cobertura(metragem, num_paredes, tipo_parede, frequencia, num_andares)

cobertura_por_metro = cobertura / metragem

classificacao, icone = classificar_cobertura(cobertura_por_metro)

st.write(f"Cobertura Estimada de Sinal Wi-Fi: {cobertura:.2f}%")
st.write(f"Cobertura por Metro Quadrado: {cobertura_por_metro:.2f}% - {icone} {classificacao}")

if classificacao == "Baixa":
    st.warning("⚠️ A cobertura está baixa. Considere adicionar um roteador ou repetidor.")
    st.write("Para melhorar a cobertura, posicione o roteador no centro do ambiente e adicione repetidores se necessário.")
elif classificacao == "Boa":
    st.info("ℹ️ A cobertura está moderada. Pode ser suficiente, mas você pode otimizar o posicionamento do roteador e considerar repetidores.")
else:
    st.success("✅ A cobertura está ótima! Seu roteador deve estar atendendo bem ao ambiente.")

st.write("Nota: Esta é uma estimativa. Para resultados mais precisos, consulte um especialista em redes.")
