import tkinter as tk
from tkinter import messagebox

def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def decimal_para_fracao(valor, max_denominador=1000):
    negativo = valor < 0
    valor = abs(valor)

    melhor_numerador = 0
    melhor_denominador = 1
    erro_min = float('inf')

    for denominador in range(1, max_denominador + 1):
        numerador = round(valor * denominador)
        erro = abs(valor - (numerador / denominador))
        if erro < erro_min:
            erro_min = erro
            melhor_numerador = numerador
            melhor_denominador = denominador

    divisor = mdc(melhor_numerador, melhor_denominador)
    numerador = melhor_numerador // divisor
    denominador = melhor_denominador // divisor

    if negativo:
        numerador *= -1

    return f"{numerador}/{denominador}" if denominador != 1 else str(numerador)

def eliminacao_gauss(matriz, termos):
    n = len(matriz)
    for i in range(n):
        matriz[i].append(termos[i])

    for k in range(n):
        max_linha = max(range(k, n), key=lambda i: abs(matriz[i][k]))
        if matriz[max_linha][k] == 0:
            raise ValueError("Sistema sem solução única.")
        matriz[k], matriz[max_linha] = matriz[max_linha], matriz[k]

        for i in range(k + 1, n):
            fator = matriz[i][k] / matriz[k][k]
            for j in range(k, n + 1):
                matriz[i][j] -= fator * matriz[k][j]

    solucao = [0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(matriz[i][j] * solucao[j] for j in range(i + 1, n))
        solucao[i] = (matriz[i][n] - soma) / matriz[i][i]
    return solucao

class App:
    def __init__(self, root):
        self.root = root
        root.title("🔢 Solver de Sistema Linear")
        root.geometry("950x650")
        root.configure(bg="#f0f4f7")

        titulo = tk.Label(root, text="🎓 Resolver Sistema Linear", font=("Arial", 18, "bold"), bg="#f0f4f7", fg="#333")
        titulo.pack(pady=15)

        top_direita = tk.Frame(root, bg="#f0f4f7")
        top_direita.place(relx=1.0, y=5, anchor="ne")
        tk.Button(
            top_direita,
            text="Instruções",
            font=("Arial", 10),
            bg="#FFC107",
            fg="black",
            command=self.mostrar_instrucoes,
            width=10,
            height=1
        ).pack(padx=5)

        self.num_var = tk.StringVar(value="2")
        vcmd = root.register(self.validar_entrada_variaveis)

        container_topo = tk.Frame(root, bg="#f0f4f7")
        container_topo.pack()

        tk.Label(container_topo, text="Número de variáveis (até 10):", font=("Arial", 12), bg="#f0f4f7").pack(side=tk.LEFT, padx=5)

        self.spin = tk.Spinbox(
            container_topo,
            from_=2,
            to=10,
            textvariable=self.num_var,
            width=5,
            font=("Arial", 12),
            validate='key',
            validatecommand=(vcmd, '%P'),
            command=self.validar_variaveis
        )
        self.spin.pack(side=tk.LEFT)
        self.spin.bind("<FocusOut>", lambda e: self.validar_variaveis())
        self.spin.bind("<Return>", lambda e: self.validar_variaveis())

        tk.Button(container_topo, text="➕ Criar Sistema", font=("Arial", 11), bg="#4CAF50", fg="white", command=self.criar_entradas).pack(side=tk.LEFT, padx=10)

        self.entrada_frame = tk.Frame(root, bg="#f0f4f7")
        self.entrada_frame.pack(pady=10)

        tk.Button(root, text="✅ Calcular", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=self.calcular).pack(pady=5)

        self.resultado = tk.Label(root, text="", font=("Courier", 12), bg="#f0f4f7", fg="#000", justify="left")
        self.resultado.pack(pady=10)

    def validar_entrada_variaveis(self, novo_valor):
        if novo_valor.isdigit():
            v = int(novo_valor)
            return 2 <= v <= 10
        return False

    def validar_variaveis(self):
        try:
            valor = int(self.num_var.get())
            if valor > 10:
                messagebox.showwarning("Limite excedido", "O número máximo de variáveis é 10.")
                self.num_var.set("10")
            elif valor < 2:
                messagebox.showwarning("Valor mínimo", "O número mínimo de variáveis é 2.")
                self.num_var.set("2")
        except ValueError:
            messagebox.showerror("Entrada inválida", "Digite um número inteiro entre 2 e 10.")
            self.num_var.set("2")

    def criar_entradas(self):
        for widget in self.entrada_frame.winfo_children():
            widget.destroy()

        self.entradas = []
        self.termos = []

        n = int(self.num_var.get())
        variaveis = ['x', 'y', 'z', 'w', 'v', 'u', 'a', 'b', 'c', 'd']

        tk.Label(self.entrada_frame, text="", bg="#f0f4f7").grid(row=0, column=0, padx=5)
        for j in range(n):
            tk.Label(self.entrada_frame, text=variaveis[j], font=("Arial", 11, "bold"), bg="#f0f4f7").grid(row=0, column=j + 1)

        for i in range(n):
            linha = []
            tk.Label(self.entrada_frame, text=f"Equação {i+1}", bg="#f0f4f7", font=("Arial", 10, "italic")).grid(row=i + 1, column=0, padx=5, pady=3, sticky="e")
            for j in range(n):
                e = tk.Entry(self.entrada_frame, width=5, font=("Arial", 11), justify="center", bg="#fff")
                e.grid(row=i + 1, column=j + 1, padx=2, pady=2)
                linha.append(e)
            self.entradas.append(linha)

            tk.Label(self.entrada_frame, text="=", font=("Arial", 12), bg="#f0f4f7").grid(row=i + 1, column=n + 1, padx=5)
            termo = tk.Entry(self.entrada_frame, width=5, font=("Arial", 11), justify="center", bg="#fff")
            termo.grid(row=i + 1, column=n + 2, padx=2)
            self.termos.append(termo)

    def calcular(self):
        try:
            matriz = [[float(c.get().replace(",", ".")) for c in linha] for linha in self.entradas]
            termos = [float(t.get().replace(",", ".")) for t in self.termos]
            solucao = eliminacao_gauss([linha[:] for linha in matriz], termos[:])
            variaveis = ['x', 'y', 'z', 'w', 'v', 'u', 'a', 'b', 'c', 'd']

            def formatar_numero(num):
                return str(int(num)) if num == int(num) else str(num)

            texto = "Equações Digitadas:\n"
            for i in range(len(matriz)):
                equacao = " + ".join(f"{formatar_numero(matriz[i][j])}{variaveis[j]}" for j in range(len(matriz[i])))
                equacao = equacao.replace("+ -", "- ")
                texto += f"{equacao} = {formatar_numero(termos[i])}\n"

            texto += "\nSoluções:\n"
            for i, val in enumerate(solucao):
                fracao = decimal_para_fracao(val)
                texto += f"{variaveis[i]} = {fracao}\n"

            self.resultado.config(text=texto)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def mostrar_instrucoes(self):
        janela = tk.Toplevel(self.root)
        janela.title("📘 Instruções")
        janela.configure(bg="#fff")
        janela.geometry("500x350")
        janela.resizable(False, False)

        texto = (
            "📘 COMO USAR O PROGRAMA:\n\n"
            "(1) Escolha o número de variáveis (entre 2 e 10).\n"
            "(2) Clique em 'Criar Sistema' para gerar os campos.\n"
            "(3) Preencha os coeficientes e os termos independentes.\n"
            "(4) Clique em 'Calcular' para ver o sistema resolvido.\n\n"
            "🧠 O programa usa Eliminação de Gauss.\n"
            "🧾 As equações e soluções aparecerão abaixo."
        )

        label = tk.Label(janela, text=texto, font=("Arial", 14), bg="#fff", justify="left", wraplength=460)
        label.pack(padx=20, pady=20)
        tk.Button(janela, text="Fechar", command=janela.destroy, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()