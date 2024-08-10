def calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipo_paredes, freq, comprimento, largura, num_comodos, pos_roteador, velocidade_internet):
    # Definindo valores padrão
    sinal_base = 50  # Base de sinal padrão para cálculos
    
    # Ajuste baseado na potência do sinal
    if potencia_sinal < -70:
        sinal_base -= 10
    elif potencia_sinal < -50:
        sinal_base -= 5
    
    # Ajuste baseado na quantidade de paredes
    perda_por_parede = 5 if tipo_paredes == 'concreto' else 2
    sinal_base -= paredes * perda_por_parede
    
    # Ajuste baseado na frequência
    if freq == 5:
        sinal_base += 10  # Frequência de 5 GHz pode ter melhor desempenho em ambientes abertos
    
    # Ajuste baseado na posição do roteador
    if pos_roteador == 'meio':
        sinal_base += 10
    elif pos_roteador == 'fundo':
        sinal_base -= 5
    elif pos_roteador == 'frente':
        sinal_base += 5
    
    # Ajuste baseado no número de roteadores
    sinal_base += num_roteadores * 5
    
    # Ajuste baseado na área total
    area_total = comprimento * largura
    cobertura_total = min(100, sinal_base - (area_total / 100))  # Simplificação
    
    # Ajuste baseado na velocidade da internet
    if 100 <= velocidade_internet < 200:
        cobertura_total *= 0.8
    elif 200 <= velocidade_internet < 300:
        cobertura_total *= 1.0
    elif 300 <= velocidade_internet <= 500:
        cobertura_total *= 1.2
    
    return max(0, cobertura_total)  # Garantir que a cobertura não seja negativa

# Exemplo de dados
potencia_sinal = -60  # dBm
num_roteadores = 2
paredes = 6
tipo_paredes = 'concreto'
freq = 2.4  # GHz
comprimento = 10  # metros
largura = 14  # metros
num_comodos = 9
pos_roteador = 'meio'
velocidade_internet = 300  # Mbps

cobertura_total = calcular_cobertura(potencia_sinal, num_roteadores, paredes, tipo_paredes, freq, comprimento, largura, num_comodos, pos_roteador, velocidade_internet)
print(f'Cobertura Geral Estimada: {cobertura_total:.2f}%')

# Cobertura por cômodo
def cobertura_por_comodo(cobertura_total, num_comodos):
    if num_comodos > 0:
        return cobertura_total / num_comodos
    return 0

for i in range(1, num_comodos + 1):
    cobertura = cobertura_por_comodo(cobertura_total, num_comodos)
    print(f'Cobertura na Cômodo {i}: {cobertura:.2f}%')
