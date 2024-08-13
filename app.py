import streamlit as st

def calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipos_paredes, freq, comprimento, largura, altura_pedireito, num_comodos, pos_roteador, num_andares):
    # Definindo valores padrão
    sinal_base = 100  # Base de sinal padrão para cálculos

    # Ajuste baseado na frequência
    if freq == 2.4:
        sinal_base += 15  # Melhor penetração em obstáculos
    elif freq == 5:
        sinal_base -= 10  # Menor penetração, maior interferência

    # Ajuste baseado na posição do roteador
    if pos_roteador == 'meio':
        sinal_base += 10
    elif pos_roteador == 'fundo':
        sinal_base -= 5
    elif pos_roteador == 'frente':
        sinal_base += 5

    # Ajuste baseado no número de roteadores
    sinal_base += num_roteadores * 10

    # Ajuste baseado no número de andares
    sinal_base -= num_andares * 10  # Cada andar adicional reduz a cobertura

    # Ajuste baseado na combinação de tipos de paredes
    perda_por_parede = {'concreto': 10, 'drywall': 5, 'madeira': 3, 'vidro': 2}
    perda_total = 0
    for parede in tipos_paredes:
        perda_total += perda_por_parede.get(parede, 0)
    
    sinal_base -= paredes * perda_total

    # Ajuste baseado na metragem de pé-direito
    ajuste_pedireito = altura_pedireito / 3
    sinal_base -= ajuste_pedireito

    # Ajuste baseado na área total
    area_total = comprimento * largura
    cobertura_total = max(0, sinal_base - (area_total / 50))  # Ajuste para refletir a dispersão do sinal

    # Normalizando cobertura para 0 a 100%
    cobertura_total = min(max(cobertura_total, 0), 100)

    return cobertura_total

# Interface Streamlit
def main():
    st.title("Análise de Cobertura Wi-Fi")
    
    st.write("Avalie a cobertura Wi-Fi do seu ambiente com base nas suas configurações e receba sugestões para melhorar a qualidade do sinal.")

    # Parâmetros de entrada
    freq = st.selectbox("Frequência (GHz):", [2.4, 5])
    comprimento = st.number_input("Comprimento do ambiente (m):", 1, 100, 30)
    largura = st.number_input("Largura do ambiente (m):", 1, 100, 6)
    altura_pedireito = st.number_input("Altura do pé-direito (m):", 1, 10, 3)
    num_andares = st.number_input("Número de andares (incluindo 0 para ambiente sem andares):", 0, 10, 1)
    paredes = st.number_input("Número total de paredes:", 0, 20, 8)
    tipos_paredes = st.multiselect("Tipos de paredes (selecione todos que se aplicam):", 
                                   ['concreto', 'drywall', 'madeira', 'vidro'])
    num_roteadores = st.number_input("Número de roteadores:", 1, 10, 1)
    pos_roteador = st.selectbox("Posição do roteador:", ['meio', 'frente', 'fundo'])

    # Cálculo da cobertura
    cobertura_total = calcular_cobertura(-100, num_roteadores, paredes, tipos_paredes, freq, comprimento, largura, altura_pedireito, paredes, pos_roteador, num_andares)
    st.write(f'**Cobertura Geral Estimada:** {cobertura_total:.2f}%')

    # Cobertura por cômodo
    num_comodos = st.number_input("Número de cômodos:", 1, 20, 13)
    
    def cobertura_por_comodo(cobertura_total, num_comodos):
        if num_comodos == 0:
            return 0
        return cobertura_total / num_comodos

    for i in range(1, num_comodos + 1):
        cobertura = cobertura_por_comodo(cobertura_total, num_comodos)
        st.write(f'Cobertura no Cômodo {i}: {cobertura:.2f}%')

    # Sugestões baseadas na cobertura
    if cobertura_total < 20:
        st.markdown("<h3 style='color: red;'>⚠️ Atenção: A cobertura Wi-Fi está muito baixa. Isso pode ser causado por muitos obstáculos, configuração inadequada do roteador ou baixa potência do sinal.</h3>", unsafe_allow_html=True)
        st.write("Aqui estão algumas sugestões para melhorar a cobertura:")
        st.write("- **Reavalie a posição do roteador:** Coloque-o em um local centralizado e elevado.")
        st.write("- **Considere adicionar mais roteadores ou repetidores:** Eles podem ajudar a expandir a cobertura.")
        st.write("- **Reduza o número de obstáculos:** Se possível, remova ou reduza barreiras entre o roteador e as áreas de uso.")
        st.write("- **Use um roteador com suporte a bandas de 5 GHz:** Pode melhorar a cobertura em áreas menos congestionadas.")
    elif cobertura_total < 50:
        st.markdown("<h3 style='color: orange;'>A cobertura Wi-Fi está abaixo dos níveis ideais. Considere as seguintes melhorias:</h3>", unsafe_allow_html=True)
        st.write("- **Verifique a posição do roteador:** Ajuste para melhorar a centralização.")
        st.write("- **Considere instalar repetidores:** Eles podem melhorar a cobertura em áreas específicas.")
    else:
        st.markdown("<h3 style='color: green;'>A cobertura Wi-Fi está adequada, mas é sempre bom verificar e ajustar para obter o melhor desempenho possível.</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
