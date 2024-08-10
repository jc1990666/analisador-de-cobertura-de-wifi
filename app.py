# Fatores de ajuste para diferentes tipos de paredes
fatores_parede = {
    "drywall": 1.1,
    "concreto": 0.7,
    "tijolo": 0.85,
    "vidro": 1.05
}

# Fatores de ajuste para frequência do roteador
fatores_frequencia = {
    "2.4 GHz": 1.2,
    "5 GHz": 0.8
}

# Fatores de ajuste para número de roteadores
fatores_roteador = {
    1: 0.8,
    2: 1.1,
    3: 1.3
}

def calcular_probabilidade(tipo_parede, frequencia_roteador, num_roteadores):
    """
    Calcula a probabilidade de uma cobertura Wi-Fi eficaz com base nas variáveis fornecidas.
    """
    fator_parede = fatores_parede.get(tipo_parede, 1)
    fator_frequencia = fatores_frequencia.get(frequencia_roteador, 1)
    fator_roteador = fatores_roteador.get(num_roteadores, 1)
    
    # Estimativa inicial de cobertura
    cobertura_estimativa = 50
    
    # Ajustar cobertura com base nos fatores
    cobertura_ajustada = cobertura_estimativa * fator_parede * fator_frequencia * fator_roteador
    
    # Calcular a probabilidade de ter uma cobertura boa
    probabilidade_cobertura_boa = min(cobertura_ajustada / 100, 1)  # Probabilidade deve ser entre 0 e 1
    
    return probabilidade_cobertura_boa

# Configurações possíveis
tipos_paredes = ["drywall", "concreto", "tijolo", "vidro"]
frequencias_roteador = ["2.4 GHz", "5 GHz"]
n_roteadores = [1, 2, 3]

# Gerar opções e calcular probabilidades
resultados = []
for tipo_parede in tipos_paredes:
    for frequencia in frequencias_roteador:
        for num_roteador in n_roteadores:
            print(f"Calculando para: Parede={tipo_parede}, Frequência={frequencia}, Roteadores={num_roteador}")  # Mensagem de depuração
            probabilidade = calcular_probabilidade(tipo_parede, frequencia, num_roteador)
            resultados.append({
                "Tipo de Parede": tipo_parede,
                "Frequência do Roteador": frequencia,
                "Número de Roteadores": num_roteador,
                "Probabilidade de Cobertura Boa": probabilidade
            })

# Exibir resultados
for resultado in resultados:
    print(f"Configuração: {resultado['Tipo de Parede']}, {resultado['Frequência do Roteador']}, {resultado['Número de Roteadores']} roteadores")
    print(f"Probabilidade de Cobertura Boa: {resultado['Probabilidade de Cobertura Boa']:.2%}")
    print()
