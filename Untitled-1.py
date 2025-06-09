import tkinter as tk
from tkinter import messagebox

# Cálculo do máximo divisor comum e conversão para fração

def mdc(a, b):
    while b:
        a, b = b, a % b
    return a


def decimal_para_fracao(valor, max_denominador=1000):
    negativo = valor < 0
    valor = abs(valor)
    melhor_numerador, melhor_denominador, erro_min = 0, 1, float('inf')
    for d in range(1, max_denominador+1):
        n = round(valor * d)
        erro = abs(valor - n / d)
        if erro < erro_min:
            erro_min = erro
            melhor_numerador, melhor_denominador = n, d
    div = mdc(melhor_numerador, melhor_denominador)
    num, den = melhor_numerador//div, melhor_denominador//div
    if negativo: num *= -1
    return f"{num}/{den}" if den != 1 else str(num)

# Função de eliminação de Gauss

def eliminacao_gauss(matriz, termos):
    n = len(matriz)
    A = [row[:] + [termos[i]] for i, row in enumerate(matriz)]
    # triangularização
    for k in range(n):
        maxr = max(range(k, n), key=lambda i: abs(A[i][k]))
        A[k], A[maxr] = A[maxr], A[k]
        for i in range(k+1, n):
            f = A[i][k] / A[k][k]
            for j in range(k, n+1):
                A[i][j] -= f * A[k][j]
    # retro-substituição
    sol = [0]*n
    for i in range(n-1, -1, -1):
        soma = sum(A[i][j] * sol[j] for j in range(i+1, n))
        sol[i] = (A[i][n] - soma) / A[i][i]
    return sol

# Interface do app
class App:
    def __init__(self, root):
        self.root = root
        root.title("🔢 Solver de Sistemas 3×3")
        root.geometry("960x700")
        root.configure(bg="#e0f7fa")  # azul claro

        # Título
        tk.Label(root, text="🎓 Elimin. de Gauss 3×3", font=("Arial",20,"bold"), bg="#e0f7fa", fg="#006064").pack(pady=10)

        # Botão de instruções colorido
        top = tk.Frame(root, bg="#e0f7fa")
        top.place(relx=1.0, y=5, anchor="ne")
        tk.Button(top, text="❔ Instruções", font=("Arial",10), bg="#ffca28", fg="#000",
                  command=self.mostrar_instrucoes).pack(padx=5)

        # Seleção fixa para 3 variáveis
        ctrl = tk.Frame(root, bg="#e0f7fa")
        ctrl.pack(pady=5)
        tk.Label(ctrl, text="Sistemas 3×3", font=("Arial",12), bg="#e0f7fa").pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="Criar Entradas", font=("Arial",11), bg="#00796b", fg="white",
                  command=self.criar_entradas).pack(side=tk.LEFT, padx=5)

        # Frame de entradas
        self.frame = tk.Frame(root, bg="#e0f7fa")
        self.frame.pack(pady=10)
        # Botão calcular
        tk.Button(root, text="✅ Calcular", font=("Arial",12,"bold"), bg="#0288d1", fg="white",
                  command=self.calcular).pack(pady=5)

        # Resultado exibido em área de texto colorida
        self.res = tk.Text(root, height=20, bg="#ffffff", fg="#004d40", font=("Courier",12))
        self.res.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.res.config(state=tk.DISABLED)

    def mostrar_instrucoes(self):
        win = tk.Toplevel(self.root)
        win.title("📘 Instruções")
        win.geometry("500x350")
        win.configure(bg="#fffde7")  # amarelo claro
        steps = (
            "🔶 Preencha o sistema 3×3 e clique em Calcular.\n"
            "🔶 Primeiro: L2 = L2 - L1.\n"
            "🔶 Segundo: L3 = L3 - 2·L1.\n"
            "🔶 Terceiro: L3 = L2 + L3 (correção importante).\n"
            "🔶 Em seguida: resolver z, depois y (substituindo z), e por fim x (substituindo y e z)."
        )
        tk.Label(win, text=steps, bg="#fffde7", font=("Arial",12), justify="left").pack(padx=15, pady=15)
        tk.Button(win, text="👍 Entendi", bg="#388e3c", fg="white", command=win.destroy).pack(pady=10)

    def criar_entradas(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.entries, self.termos = [], []
        vars = ['x','y','z']
        # Cabeçalhos coloridos
        for j, v in enumerate(vars):
            tk.Label(self.frame, text=v, font=("Arial",12,"bold"), bg="#e0f7fa").grid(row=0, column=j)
        tk.Label(self.frame, text='=', font=("Arial",12,"bold"), bg="#e0f7fa").grid(row=0, column=3)
        # Entradas para cada linha
        for i in range(3):
            row=[]
            for j in range(3):
                e=tk.Entry(self.frame, width=6, justify="center")
                e.grid(row=i+1, column=j, padx=5, pady=5)
                row.append(e)
            self.entries.append(row)
            t=tk.Entry(self.frame, width=6, justify="center")
            t.grid(row=i+1, column=3, padx=5)
            self.termos.append(t)

    def calcular(self):
        # limpar texto
        self.res.config(state=tk.NORMAL)
        self.res.delete('1.0', tk.END)
        try:
            A=[[int(e.get()) for e in row] for row in self.entries]
            b=[int(t.get()) for t in self.termos]
        except:
            messagebox.showerror("Erro","Preencha todos os coeficientes.")
            return
        vars=['x','y','z']
        # Mostrar equações iniciais
        self.res.insert(tk.END,"Equações Digitadas:\n")
        for i in range(3):
            eq = " + ".join(f"{A[i][j]}{vars[j]}" for j in range(3)).replace("+ -","- ")
            self.res.insert(tk.END, f"{eq} = {b[i]}\n")
        # Escalonamento passo a passo
        # L2 = L2 - L1
        self.res.insert(tk.END,"\nPasso 1: L2 = L2 - L1\n")
        for j in range(3): A[1][j] -= A[0][j]
        b[1] -= b[0]
        self.res.insert(tk.END, f"Nova L2: { ' + '.join(f'{A[1][j]}{vars[j]}' for j in range(3)).replace('+ -','- ')} = {b[1]}\n")
        # L3 = L3 - 2·L1
        self.res.insert(tk.END,"\nPasso 2: L3 = L3 - 2·L1\n")
        for j in range(3): A[2][j] -= 2*A[0][j]
        b[2] -= 2*b[0]
        self.res.insert(tk.END, f"Nova L3: { ' + '.join(f'{A[2][j]}{vars[j]}' for j in range(3)).replace('+ -','- ')} = {b[2]}\n")
        # L3 = L2 + L3 (correção)
        self.res.insert(tk.END,"\nPasso 3: L3 = L2 + L3\n")
        for j in range(3): A[2][j] += A[1][j]
        b[2] += b[1]
        self.res.insert(tk.END, f"Corrigida L3: { ' + '.join(f'{A[2][j]}{vars[j]}' for j in range(3)).replace('+ -','- ')} = {b[2]}\n")
        # Mostrar matriz atualizada
        self.res.insert(tk.END,"\nMatriz Atualizada (A | b):\n")
        for i in range(3):
            row_str = "[" + " ".join(f"{A[i][j]:>3}" for j in range(3)) + " |" + f" {b[i]:>3}" + "]\n"
            self.res.insert(tk.END, row_str)
        # Cálculo z, y, x com substituições
        # z
        coef_z, rhs_z = A[2][2], b[2]
        val_z = rhs_z/coef_z
        self.res.insert(tk.END, f"\nCálculo de z: {coef_z}z = {rhs_z} -> z = {rhs_z}/{coef_z} = {decimal_para_fracao(val_z)}\n")
        # y
        coef_y, coef_yz = A[1][1], A[1][2]
        self.res.insert(tk.END, f"\nCálculo de y: {coef_y}y + {coef_yz}*({decimal_para_fracao(val_z)}) = {b[1]}\n")
        rhs_y = b[1] - coef_yz*val_z
        self.res.insert(tk.END, f"{coef_y}y = {rhs_y} -> y = {rhs_y}/{coef_y} = {decimal_para_fracao(rhs_y/coef_y)}\n")
        # x
        coef_x, coef_xy, coef_xz = A[0][0], A[0][1], A[0][2]
        self.res.insert(tk.END, f"\nCálculo de x: {coef_x}x + {coef_xy}*({decimal_para_fracao(rhs_y/coef_y)}) + {coef_xz}*({decimal_para_fracao(val_z)}) = {b[0]}\n")
        rhs_x = b[0] - coef_xy*(rhs_y/coef_y) - coef_xz*val_z
        self.res.insert(tk.END, f"x = ({b[0]} - {coef_xy}*{decimal_para_fracao(rhs_y/coef_y)} - {coef_xz}*{decimal_para_fracao(val_z)})/{coef_x} = {decimal_para_fracao(rhs_x/coef_x)}\n")
        # Solução final
        self.res.insert(tk.END, "\nSolução final:\n")
        self.res.insert(tk.END, f"x = {decimal_para_fracao(rhs_x/coef_x)}\n")
        self.res.insert(tk.END, f"y = {decimal_para_fracao(rhs_y/coef_y)}\n")
        self.res.insert(tk.END, f"z = {decimal_para_fracao(val_z)}\n")
        self.res.config(state=tk.DISABLED)

if __name__ == "__main__":
    root=tk.Tk()
    App(root)
    root.mainloop()
