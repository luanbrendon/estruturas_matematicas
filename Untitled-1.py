import tkinter as tk
from tkinter import messagebox

def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def decimal_para_fracao(valor, max_denominador=1000):
    negativo = valor < 0
    valor = abs(valor)
    melhor_numerador, melhor_denominador, erro_min = 0, 1, float('inf')
    for d in range(1, max_denominador + 1):
        numerador = round(valor * d)
        erro = abs(valor - numerador / d)
        if erro < erro_min:
            erro_min = erro
            melhor_numerador, melhor_denominador = numerador, d
    div = mdc(melhor_numerador, melhor_denominador)
    num, den = melhor_numerador // div, melhor_denominador // div
    if negativo: num *= -1
    return f"{num}/{den}" if den != 1 else str(num)

def eliminacao_gauss(matriz, termos):
    n = len(matriz)
    M = [matriz[i][:] + [termos[i]] for i in range(n)]
    for k in range(n):
        max_linha = max(range(k, n), key=lambda i: abs(M[i][k]))
        M[k], M[max_linha] = M[max_linha], M[k]
        for i in range(k + 1, n):
            fator = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] -= fator * M[k][j]
    sol = [0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(M[i][j] * sol[j] for j in range(i + 1, n))
        sol[i] = (M[i][n] - soma) / M[i][i]
    return sol

class App:
    def __init__(self, root):
        self.root = root
        root.title("🔢 Solver de Sistema Linear")
        root.geometry("950x650")
        root.configure(bg="#f0f4f7")

        tk.Label(root, text="🎓 Resolver Sistema Linear", font=("Arial", 18, "bold"), bg="#f0f4f7", fg="#333").pack(pady=15)

        top = tk.Frame(root, bg="#f0f4f7")
        top.place(relx=1.0, y=5, anchor="ne")
        tk.Button(top, text="Instruções", font=("Arial", 10), bg="#FFC107", fg="black", command=self.mostrar_instrucoes, width=10).pack(padx=5)

        container = tk.Frame(root, bg="#f0f4f7")
        container.pack()
        tk.Label(container, text="Número de variáveis (até 10):", font=("Arial",12), bg="#f0f4f7").pack(side=tk.LEFT, padx=5)
        self.num_var = tk.StringVar(value="2")
        vcmd = root.register(self.validar_entrada)
        self.spin = tk.Spinbox(container, from_=2, to=10, textvariable=self.num_var, width=5, font=("Arial",12), validate='key', validatecommand=(vcmd,'%P'))
        self.spin.pack(side=tk.LEFT)
        tk.Button(container, text="➕ Criar Sistema", font=("Arial",11), bg="#4CAF50", fg="white", command=self.criar_entradas).pack(side=tk.LEFT, padx=10)

        self.entrada_frame = tk.Frame(root, bg="#f0f4f7")
        self.entrada_frame.pack(pady=10)
        tk.Button(root, text="✅ Calcular", font=("Arial",12,"bold"), bg="#2196F3", fg="white", command=self.calcular).pack(pady=5)

        self.resultado = tk.Text(root, height=20, bg="#fff", fg="#000", font=("Courier",12))
        self.resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.resultado.config(state=tk.DISABLED)

    def validar_entrada(self, valor):
        if valor.isdigit():
            return 2 <= int(valor) <= 10
        return False

    def criar_entradas(self):
        for w in self.entrada_frame.winfo_children(): w.destroy()
        self.entradas, self.consts = [], []
        n = int(self.num_var.get())
        vars = ['x','y','z','w','v','u','a','b','c','d']
        tk.Label(self.entrada_frame, text="", bg="#f0f4f7").grid(row=0,column=0)
        for j in range(n): tk.Label(self.entrada_frame, text=vars[j], bg="#f0f4f7", font=("Arial",11,"bold")).grid(row=0,column=j+1)
        tk.Label(self.entrada_frame, text="=", bg="#f0f4f7").grid(row=0,column=n+1)
        for i in range(n):
            tk.Label(self.entrada_frame, text=f"Eq{i+1}", bg="#f0f4f7").grid(row=i+1,column=0)
            row=[]
            for j in range(n):
                e = tk.Entry(self.entrada_frame, width=5, font=("Arial",11), justify="center")
                e.grid(row=i+1,column=j+1,padx=2, pady=2)
                row.append(e)
            self.entradas.append(row)
            t = tk.Entry(self.entrada_frame, width=5, font=("Arial",11), justify="center")
            t.grid(row=i+1, column=n+1, padx=5)
            self.consts.append(t)

    def calcular(self):
        self.resultado.config(state=tk.NORMAL)
        self.resultado.delete('1.0', tk.END)
        try:
            A = [[float(e.get().replace(',','.')) for e in row] for row in self.entradas]
            b = [float(c.get().replace(',','.')) for c in self.consts]
        except:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
            return
        n = len(A)
        vars = ['x','y','z','w','v','u','a','b','c','d']
        # Equações originais
        self.resultado.insert(tk.END, "Equações Digitadas:\n")
        for i in range(n):
            eq = " + ".join(f"{int(A[i][j])}{vars[j]}" for j in range(n)).replace("+ -","- ")
            self.resultado.insert(tk.END, f"{eq} = {int(b[i])}\n")
        # Executar eliminação
        sol = eliminacao_gauss([row[:] for row in A], b[:])
        # Substituições passo a passo
        self.resultado.insert(tk.END, "\nSubstituições (retro):\n")
        for i in range(n-1, -1, -1):
            termo = b[i] - sum(A[i][j] * sol[j] for j in range(i+1, n))
            self.resultado.insert(tk.END, f"Eq{i+1}: {termo} = {int(A[i][i])}{vars[i]}\n")
            self.resultado.insert(tk.END, f"{vars[i]} = {termo}/{int(A[i][i])} = {decimal_para_fracao(sol[i])}\n\n")
        # Solução final
        sol_text = ', '.join(f"{vars[i]}={decimal_para_fracao(sol[i])}" for i in range(n))
        self.resultado.insert(tk.END, f"Solução final: {sol_text}\n")
        self.resultado.config(state=tk.DISABLED)

    def mostrar_instrucoes(self):
        win = tk.Toplevel(self.root)
        win.title("📘 Instruções")
        win.geometry("500x350")
        win.configure(bg="#fff")
        texto = (
            "1) Escolha n e Gere o Sistema.\n"
            "2) Preencha coeficientes e constantes.\n"
            "3) Calcular: mostra eliminação e depois substituições.\n"
            "4) Cada Eq_i se isola substituindo retroativamente."
        )
        tk.Label(win, text=texto, font=("Arial",12), bg="#fff", justify="left", wraplength=460).pack(padx=20, pady=20)
        tk.Button(win, text="Fechar", command=win.destroy, bg="#2196F3", fg="white").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
