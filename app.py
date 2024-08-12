import streamlit as st

def calcular_cobertura(freq, comprimento, largura, altura, num_andares, tipos_paredes, num_roteadores, pos_roteador):
    # Definindo valores base
    sinal_base = 100  # Base de sinal padrão para cálculos

    # Ajuste baseado no número de andares
    sinal_base -= num_andares * 10  # Cada andar adicional reduz a cobertura

    # Ajuste baseado na frequência
    if freq == 2.4:
        sinal_base += 10  # Melhor penetração em obstáculos
    elif freq == 5:
        sinal_base -= 15  # Menor penetração, maior interferência

    # Ajuste baseado na posição do roteador
    if pos_roteador == 'meio':
        sinal_base += 10
    elif pos_roteador == 'fundo':
        sinal_base -= 10
    elif pos_roteador == 'frente':
        sinal_base += 5

    # Ajuste baseado no número de roteadores
    sinal_base += num_roteadores * 10

    # Ajuste baseado nos tipos de paredes
    perdas_por_parede = {
        'alvenaria': 10,
        'vidro': 5,
        'metal': 20,
        'plástico': 3,
        'PVC': 5
    }
    perda_total_paredes = sum(perdas_por_parede.get(parede, 0) for parede in tipos_paredes)
    sinal_base -= perda_total_paredes

    # Ajuste baseado na área total e altura do pé-direito
    area_total = comprimento * largura
    volume_total = area_total * altura
    cobertura_total = max(0, sinal_base - (volume_total / 100))  # Ajuste para refletir a dispersão do sinal

    # Ajustar para garantir que a cobertura esteja dentro da faixa de 0 a 100%
    cobertura_total = min(max(cobertura_total, 0), 100)

    return cobertura_total

# Interface Streamlit
def main():
    st.title("Análise de Cobertura Wi-Fi")
    st.write("Este cálculo considera ambientes com múltiplos andares e diferentes alturas de pé-direito.")

    # Parâmetros de entrada
    freq = st.selectbox("Frequência (GHz):", [2.4, 5])
    comprimento = st.number_input("Comprimento do ambiente (m):", 1, 100, 30)
    largura = st.number_input("Largura do ambiente (m):", 1, 100, 6)
    altura = st.number_input("Altura do pé-direito (m):", 1, 10, 2)
    num_andares = st.number_input("Número de andares (incluindo 0 para ambiente sem andares):", 0, 10, 1)
    tipos_paredes = st.multiselect("Tipos de paredes (selecione todos que se aplicam):", 
                                    ['alvenaria', 'vidro', 'metal', 'plástico', 'PVC'])
    num_roteadores = st.number_input("Número de roteadores:", 1, 10, 1)
    pos_roteador = st.selectbox("Posição do roteador:", ['meio', 'frente', 'fundo'])

    # Cálculo da cobertura
    cobertura_total = calcular_cobertura(freq, comprimento, largura, altura, num_andares, tipos_paredes, num_roteadores, pos_roteador)
    st.write(f'Cobertura Geral Estimada: {cobertura_total:.2f}%')

    # Cobertura por cômodo
    num_comodos = st.number_input("Número de cômodos:", 1, 20, 4)
    def cobertura_por_comodo(cobertura_total, num_comodos):
        if num_comodos == 0:
            return 0
        return cobertura_total / num_comodos

    for i in range(1, num_comodos + 1):
        cobertura = cobertura_por_comodo(cobertura_total, num_comodos)
        st.write(f'Cobertura no Cômodo {i}: {cobertura:.2f}%')

    # Sugestões baseadas na cobertura
    if cobertura_total < 20:
        st.warning("⚠️ Atenção: A cobertura Wi-Fi está muito baixa. Isso pode ser causado por muitos obstáculos, configuração inadequada do roteador ou baixa potência do sinal.")
        st.write("Aqui estão algumas sugestões para melhorar a cobertura:")
        st.write("- **Reavalie a posição do roteador:** Coloque-o em um local centralizado e elevado.")
        st.write("- **Considere adicionar mais roteadores ou repetidores:** Eles podem ajudar a expandir a cobertura.")
        st.write("- **Reduza o número de obstáculos:** Se possível, remova ou reduza barreiras entre o roteador e as áreas de uso.")
        st.write("- **Use um roteador com suporte a bandas de 5 GHz:** Pode melhorar a cobertura em áreas menos congestionadas.")
    elif cobertura_total < 50:
        st.info("A cobertura Wi-Fi está abaixo do ideal. Considere as seguintes melhorias:")
        st.write("- **Verifique a posição do roteador:** Ajuste para uma melhor centralização.")
        st.write("- **Considere a instalação de repetidores:** Eles podem ajudar a melhorar a cobertura em áreas específicas.")
    else:
        st.success("A cobertura Wi-Fi está adequada, mas sempre é bom verificar e ajustar para obter a melhor performance possível.")

if __name__ == "__main__":
    main()
