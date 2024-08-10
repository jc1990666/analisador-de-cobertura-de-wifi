import tkinter as tk

# Fatores de ajuste
fatores_parede = {
    "drywall": 1.1,
    "concreto": 0.7,
    "tijolo": 0.85,
    "vidro": 1.05
}

fatores_frequencia = {
    "2.4 GHz": 1.2,
    "5 GHz": 0.8
}

fatores_roteador = {
    1: 0.8,
    2: 1.1,
    3: 1.3
}

def calcular_probabilidade(tipo_parede, frequencia_roteador, num_roteadores):
    fator_parede = fatores_parede.get(tipo_parede, 1)
    fator_frequencia = fatores_frequencia.get(frequencia_roteador, 1)
    fator_roteador = fatores_roteador.get(num_roteadores, 1)
    
    cobertura_estimativa = 50
    cobertura_ajustada = cobertura_estimativa * fator_parede * fator_frequencia * fator_roteador
    probabilidade_cobertura_boa = min(cobertura_ajustada / 100, 1)
    
    return probabilidade_cobertura_boa

def exibir_resultados():
    resultados = []
    for tipo_parede in tipos_paredes:
        for frequencia in frequencias_roteador:
            for num_roteador in n_roteadores:
                probabilidade = calcular_probabilidade(tipo_parede, frequencia, num_roteador)
                resultados.append({
                    "Tipo de Parede": tipo_parede,
                    "Frequência do Roteador": frequencia,
                    "Número de Roteadores": num_roteador,
                    "Probabilidade de Cobertura Boa": probabilidade
                })
    
    for resultado in resultados:
        texto = (f"Configuração: {resultado['Tipo de Parede']}, {resultado['Frequência do Roteador']}, "
                 f"{resultado['Número de Roteadores']} roteadores\n"
                 f"Probabilidade de Cobertura Boa: {resultado['Probabilidade de Cobertura Boa']:.2%}\n")
        resultado_texto.insert(tk.END, texto)

# Configurações possíveis
tipos_paredes = ["drywall", "concreto", "tijolo", "vidro"]
frequencias_roteador = ["2.4 GHz", "5 GHz"]
n_roteadores = [1, 2, 3]

# Configuração da Interface
root = tk.Tk()
root.title("Analisador de Cobertura Wi-Fi")

resultado_texto = tk.Text(root, height=15, width=80)
resultado_texto.pack()

btn_calcular = tk.Button(root, text="Calcular Cobertura", command=exibir_resultados)
btn_calcular.pack()

root.mainloop()
