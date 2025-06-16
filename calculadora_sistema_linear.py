import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText


# Calcula o máximo divisor comum entre dois números (usado para simplificar frações)
def mdc(a, b):
    while b:
        a, b = b, a % b
    return a


# Converte um número decimal em fração, com denominador máximo permitido
def decimal_para_fracao(valor, max_denominador=1000):
    negativo = valor < 0
    valor = abs(valor)
    numerador, denominador, erro_min = 0, 1, float('inf')
    for d in range(1, max_denominador + 1):
        n = round(valor * d)
        erro = abs(valor - n / d)
        if erro < erro_min:
            erro_min = erro
            numerador, denominador = n, d
    div = mdc(numerador, denominador)
    num, den = numerador // div, denominador // div
    if negativo: num *= -1
    return f"{num}/{den}" if den != 1 else str(num)


# Executa o método de Eliminação de Gauss com registro dos passos
def gauss_passos(matriz, termos):
    n = len(matriz)
    M = [matriz[i][:] + [termos[i]] for i in range(n)]
    passos = ['Equações iniciais:']

    # Exibe sistema original
    for i in range(n):
        row = ' '.join(f"{M[i][j]:>6.2f}" for j in range(n)) + f" | {M[i][n]:>6.2f}"
        passos.append(f"L{i + 1}: [{row}]")
    passos.append('')

    # Etapa de eliminação
    for k in range(n):
        maxr = max(range(k, n), key=lambda i: abs(M[i][k]))  # Pivoteamento parcial
        if maxr != k:
            M[k], M[maxr] = M[maxr], M[k]
            passos.append(f"Troca L{k + 1} <-> L{maxr + 1}")
        for i in range(k + 1, n):
            fator = M[i][k] / M[k][k]
            passos.append(f"L{i + 1} = L{i + 1} - ({fator:.2f})*L{k + 1}")
            for j in range(k, n + 1):
                M[i][j] -= fator * M[k][j]
        passos.append(f"Matriz após eliminação coluna {k + 1}:")
        for i in range(n):
            row = ' '.join(f"{M[i][j]:>6.2f}" for j in range(n)) + f" | {M[i][n]:>6.2f}"
            passos.append(f"L{i + 1}: [{row}]")
        passos.append('')

    # Substituição retroativa para encontrar soluções
    sol = [0] * n
    passos.append('Substituição retroativa:')
    for i in range(n - 1, -1, -1):
        soma = sum(M[i][j] * sol[j] for j in range(i + 1, n))
        coef = M[i][i]
        rhs = M[i][n] - soma
        sol[i] = rhs / coef
        passos.append(f"{coef:.2f}·x{i + 1} = {rhs:.2f}  => x{i + 1} = {decimal_para_fracao(sol[i])}")
    return M, sol, passos


# Desenha botões arredondados com borda no hover
def desenhar_botao(canvas, texto, cor, comando):
    largura, altura, raio = 124, 39, 15
    borda_espessura = 3

    # Desenha o botão com ou sem borda
    def desenhar(cor_fundo, mostrar_borda):
        canvas.delete("all")
        if mostrar_borda:
            # Borda preta arredondada
            canvas.create_arc(0, 0, raio * 2, raio * 2, start=90, extent=90, fill="black", outline="black")
            canvas.create_arc(largura - raio * 2, 0, largura, raio * 2, start=0, extent=90, fill="black",
                              outline="black")
            canvas.create_arc(0, altura - raio * 2, raio * 2, altura, start=180, extent=90, fill="black",
                              outline="black")
            canvas.create_arc(largura - raio * 2, altura - raio * 2, largura, altura, start=270, extent=90,
                              fill="black", outline="black")
            canvas.create_rectangle(raio, 0, largura - raio, altura, fill="black", outline="black")
            canvas.create_rectangle(0, raio, largura, altura - raio, fill="black", outline="black")

        # Botão interno colorido
        p = borda_espessura if mostrar_borda else 0
        canvas.create_arc(p, p, raio * 2 - p, raio * 2 - p, start=90, extent=90, fill=cor_fundo, outline=cor_fundo)
        canvas.create_arc(largura - raio * 2 + p, p, largura - p, raio * 2 - p, start=0, extent=90, fill=cor_fundo,
                          outline=cor_fundo)
        canvas.create_arc(p, altura - raio * 2 + p, raio * 2 - p, altura - p, start=180, extent=90, fill=cor_fundo,
                          outline=cor_fundo)
        canvas.create_arc(largura - raio * 2 + p, altura - raio * 2 + p, largura - p, altura - p, start=270, extent=90,
                          fill=cor_fundo, outline=cor_fundo)
        canvas.create_rectangle(raio, p, largura - raio, altura - p, fill=cor_fundo, outline=cor_fundo)
        canvas.create_rectangle(p, raio, largura - p, altura - raio, fill=cor_fundo, outline=cor_fundo)

        # Texto do botão
        canvas.create_text(largura // 2, altura // 2, text=texto, font=("Arial", 10, "bold"), fill="white")

    canvas.config(width=largura, height=altura, highlightthickness=0)
    desenhar(cor, mostrar_borda=False)
    canvas.bind("<Enter>", lambda e: desenhar(cor, mostrar_borda=True))
    canvas.bind("<Leave>", lambda e: desenhar(cor, mostrar_borda=False))
    canvas.bind("<Button-1>", lambda e: comando())


class App:
    def __init__(self, root):
        # Inicializa a janela principal
        self.root = root
        root.title("🔢 Calculadora de Sistema Linear")
        root.geometry("950x650")
        root.configure(bg="#f0f4f7")

        # Título da janela
        tk.Label(root, text="🎓 Resolver Sistema Linear", font=("Arial", 18, "bold"), bg="#f0f4f7", fg="#333").pack(pady=15)

        # Botão de instruções no canto superior direito
        top = tk.Frame(root, bg="#f0f4f7")
        top.place(relx=1.0, y=5, anchor="ne")
        btn_instr = tk.Canvas(top, bg="#f0f4f7", highlightthickness=0)
        btn_instr.pack(padx=5)
        desenhar_botao(btn_instr, "Instruções", "#FFC107", self.mostrar_instrucoes)

        # Área para selecionar o número de variáveis e criar sistema
        container = tk.Frame(root, bg="#f0f4f7")
        container.pack()
        tk.Label(container, text="Número de variáveis (até 10):", font=("Arial", 12), bg="#f0f4f7").pack(side=tk.LEFT, padx=5)
        self.num_var = tk.StringVar(value="2")
        vcmd = root.register(self.validar)  # Validação para o Spinbox
        self.spin = tk.Spinbox(container, from_=2, to=10, textvariable=self.num_var, width=5, font=("Arial", 12), validate='key', validatecommand=(vcmd, '%P'))
        self.spin.pack(side=tk.LEFT)

        # Botão para criar os campos do sistema
        btn_criar = tk.Canvas(container, bg="#f0f4f7", highlightthickness=0)
        btn_criar.pack(side=tk.LEFT, padx=10)
        desenhar_botao(btn_criar, "➕ Criar Sistema", "#4CAF50", self.criar_entradas)

        # Área onde os campos de entrada das equações aparecerão
        self.frame = tk.Frame(root, bg="#f0f4f7")
        self.frame.pack(pady=10)

        # Botão para resolver o sistema
        btn_calc = tk.Canvas(root, bg="#f0f4f7", highlightthickness=0)
        btn_calc.pack(pady=5)
        desenhar_botao(btn_calc, "✅ Calcular", "#1E88E5", self.calcular)

        # Área de texto para exibir os passos e a solução final
        self.text = ScrolledText(root, height=20, bg="#fff", fg="#000", font=("Courier", 12))
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text.config(state=tk.DISABLED)


    def validar(self, v):
        # Verifica se o valor digitado é um número entre 2 e 10 (para o Spinbox)
        return v.isdigit() and 2 <= int(v) <= 10

    def criar_entradas(self):
        # Cria os campos para inserir os coeficientes e termos independentes
        for w in self.frame.winfo_children():
            w.destroy()  # Limpa os campos anteriores

        self.entries, self.consts = [], []
        n = int(self.num_var.get())
        vars = ['x', 'y', 'z', 'w', 'v', 'u', 'a', 'b', 'c', 'd']  # Nomes das variáveis

        # Cabeçalho da matriz (nomes das variáveis)
        tk.Label(self.frame, text="", bg="#f0f4f7").grid(row=0, column=0)
        for j in range(n):
            tk.Label(self.frame, text=vars[j], bg="#f0f4f7", font=("Arial", 11, "bold")).grid(row=0, column=j + 1)
        tk.Label(self.frame, text="=", bg="#f0f4f7").grid(row=0, column=n + 1)

        # Campos para digitar os coeficientes
        for i in range(n):
            tk.Label(self.frame, text=f"Eq{i + 1}", bg="#f0f4f7").grid(row=i + 1, column=0)
            row = []
            for j in range(n):
                e = tk.Entry(self.frame, width=5, font=("Arial", 11), justify="center")
                e.grid(row=i + 1, column=j + 1, padx=2, pady=2)
                row.append(e)
            self.entries.append(row)

            # Campo para termo independente
            t = tk.Entry(self.frame, width=5, font=("Arial", 11), justify="center")
            t.grid(row=i + 1, column=n + 1, padx=5)
            self.consts.append(t)

    def calcular(self):
        # Lê os valores dos campos e resolve o sistema
        self.text.config(state=tk.NORMAL)
        self.text.delete('1.0', tk.END)
        try:
            # Lê a matriz dos coeficientes e o vetor de constantes
            A = [[float(e.get().replace(',', '.')) for e in row] for row in self.entries]
            b = [float(c.get().replace(',', '.')) for c in self.consts]
        except:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return

        # Chama a função de resolução e exibe os passos
        M, sol, passos = gauss_passos(A, b)
        for p in passos:
            self.text.insert(tk.END, p + "\n")

        # Exibe solução final
        self.text.insert(tk.END, "\n📌 Solução Final:\n\n")
        vars = ['x', 'y', 'z', 'w', 'v', 'u', 'a', 'b', 'c', 'd']
        for i, v in enumerate(sol):
            self.text.insert(tk.END, f"{vars[i]} = {decimal_para_fracao(v)}\n")
        self.text.config(state=tk.DISABLED)

    def mostrar_instrucoes(self):
        # Abre uma nova janela com instruções de uso
        win = tk.Toplevel(self.root)
        win.title("Instruções de Uso")
        centralizar_janela(win, 550, 500)
        win.configure(bg="#ffffff")

        frame = tk.Frame(win, bg="#ffffff")
        frame.pack(padx=20, pady=30, fill="both", expand=True)

        # Título
        tk.Label(frame, text="Como utilizar o aplicativo:", font=("Arial", 14, "bold"),
                 bg="#ffffff", fg="black").pack(anchor="w", pady=(0, 25))

        # Instrução 1
        tk.Label(frame, text="1. Escolha o número de variáveis (entre 2 e 10).",
                 font=("Arial", 11, "bold"), bg="#ffffff", fg="black").pack(anchor="w", pady=6)

        # Instrução 2 - Criar sistema
        linha2 = tk.Frame(frame, bg="#ffffff")
        linha2.pack(anchor="w", pady=6)
        tk.Label(linha2, text="2. Clique em ", font=("Arial", 11, "bold"),
                 bg="#ffffff", fg="black").pack(side="left")
        tk.Label(linha2, text="➕ Criar Sistema", font=("Arial", 11, "bold"),
                 bg="#ffffff", fg="green").pack(side="left")
        tk.Label(linha2, text=" para gerar os campos das equações.",
                 font=("Arial", 11, "bold"), bg="#ffffff", fg="black").pack(side="left")

        # Instrução 3
        tk.Label(frame, text="3. Preencha os coeficientes das variáveis e o termo independente.",
                 font=("Arial", 11, "bold"), bg="#ffffff", fg="black").pack(anchor="w", pady=6)

        # Instrução 4 - Calcular
        linha4 = tk.Frame(frame, bg="#ffffff")
        linha4.pack(anchor="w", pady=6)
        tk.Label(linha4, text="4. Clique em ", font=("Arial", 11, "bold"),
                 bg="#ffffff", fg="black").pack(side="left")
        tk.Label(linha4, text="✅ Calcular", font=("Arial", 11, "bold"),
                 bg="#ffffff", fg="blue").pack(side="left")
        tk.Label(linha4, text=" para resolver o sistema.",
                 font=("Arial", 11, "bold"), bg="#ffffff", fg="black").pack(side="left")

        # Instrução 5
        tk.Label(frame, text="5. Os passos do método de Eliminação de Gauss serão exibidos abaixo.",
                 font=("Arial", 11, "bold"), bg="#ffffff", fg="black").pack(anchor="w", pady=6)

        # Botão para fechar a janela de instruções
        canvas = tk.Canvas(frame, bg="#ffffff", highlightthickness=0)
        canvas.pack(pady=(10, 20))
        desenhar_botao(canvas, "Fechar", "#cccccc", win.destroy)

# Centraliza a janela na tela
def centralizar_janela(janela, largura, altura):
    janela.update_idletasks()
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    centralizar_janela(root, 950, 650)
    App(root)
    root.mainloop()

