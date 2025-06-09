import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

# Funções auxiliares

def mdc(a, b):
    while b:
        a, b = b, a % b
    return a

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

# Eliminação de Gauss passo a passo

def gauss_passos(matriz, termos):
    n = len(matriz)
    M = [matriz[i][:] + [termos[i]] for i in range(n)]
    passos = []
    # Equações iniciais
    passos.append('Equações iniciais:')
    for i in range(n):
        row = ' '.join(f"{M[i][j]:>6.2f}" for j in range(n)) + f" | {M[i][n]:>6.2f}"
        passos.append(f"L{i+1}: [{row}]")
    passos.append('')
    # Escalonamento
    for k in range(n):
        # pivoteamento
        maxr = max(range(k,n), key=lambda i: abs(M[i][k]))
        if maxr != k:
            M[k], M[maxr] = M[maxr], M[k]
            passos.append(f"Troca L{k+1} <-> L{maxr+1}")
        # zeragem
        for i in range(k+1, n):
            fator = M[i][k] / M[k][k]
            passos.append(f"L{i+1} = L{i+1} - ({fator:.2f})*L{k+1}")
            for j in range(k, n+1):
                M[i][j] -= fator * M[k][j]
        # estado após passo
        passos.append(f"Matriz após eliminação coluna {k+1}:")
        for i in range(n):
            row = ' '.join(f"{M[i][j]:>6.2f}" for j in range(n)) + f" | {M[i][n]:>6.2f}"
            passos.append(f"L{i+1}: [{row}]")
        passos.append('')
    # retro-substituição
    sol = [0]*n
    passos.append('Substituição retroativa:')
    for i in range(n-1,-1,-1):
        soma = sum(M[i][j]*sol[j] for j in range(i+1,n))
        coef = M[i][i]
        rhs = M[i][n] - soma
        sol[i] = rhs/coef
        passos.append(f"{coef:.2f}*x{i+1} = {rhs:.2f}  => x{i+1} = {rhs:.2f}/{coef:.2f} = {decimal_para_fracao(sol[i])}")
    return M, sol, passos

class App:
    def __init__(self, root):
        self.root = root
        root.title("🔢 Solver de Sistema Linear")
        root.geometry("950x650")
        root.configure(bg="#f0f4f7")

        tk.Label(root, text="🎓 Resolver Sistema Linear", font=("Arial",18,"bold"), bg="#f0f4f7", fg="#333").pack(pady=15)
        top = tk.Frame(root, bg="#f0f4f7")
        top.place(relx=1.0,y=5,anchor="ne")
        tk.Button(top, text="Instruções", font=("Arial",10), bg="#FFC107", fg="black", command=self.mostrar_instrucoes, width=10).pack(padx=5)

        container = tk.Frame(root, bg="#f0f4f7")
        container.pack()
        tk.Label(container, text="Número de variáveis (até 10):", font=("Arial",12), bg="#f0f4f7").pack(side=tk.LEFT, padx=5)
        self.num_var = tk.StringVar(value="2")
        vcmd = root.register(self.validar)
        self.spin = tk.Spinbox(container, from_=2, to=10, textvariable=self.num_var, width=5, font=("Arial",12), validate='key', validatecommand=(vcmd,'%P'))
        self.spin.pack(side=tk.LEFT)
        tk.Button(container, text="➕ Criar Sistema", font=("Arial",11), bg="#4CAF50", fg="white", command=self.criar_entradas).pack(side=tk.LEFT, padx=10)

        self.frame = tk.Frame(root, bg="#f0f4f7")
        self.frame.pack(pady=10)
        tk.Button(root, text="✅ Calcular", font=("Arial",12,"bold"), bg="#2196F3", fg="white", command=self.calcular).pack(pady=5)

        self.text = ScrolledText(root, height=20, bg="#fff", fg="#000", font=("Courier",12))
        self.text.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
        self.text.config(state=tk.DISABLED)

    def validar(self, v):
        return v.isdigit() and 2<=int(v)<=10

    def criar_entradas(self):
        for w in self.frame.winfo_children(): w.destroy()
        self.entries, self.consts = [], []
        n = int(self.num_var.get())
        vars = ['x','y','z','w','v','u','a','b','c','d']
        tk.Label(self.frame, text="", bg="#f0f4f7").grid(row=0,column=0)
        for j in range(n): tk.Label(self.frame,text=vars[j],bg="#f0f4f7",font=("Arial",11,"bold")).grid(row=0,column=j+1)
        tk.Label(self.frame, text="=",bg="#f0f4f7").grid(row=0,column=n+1)
        for i in range(n):
            tk.Label(self.frame, text=f"Eq{i+1}",bg="#f0f4f7").grid(row=i+1,column=0)
            row=[]
            for j in range(n):
                e=tk.Entry(self.frame,width=5,font=("Arial",11),justify="center")
                e.grid(row=i+1,column=j+1,padx=2,pady=2)
                row.append(e)
            self.entries.append(row)
            t=tk.Entry(self.frame,width=5,font=("Arial",11),justify="center")
            t.grid(row=i+1,column=n+1,padx=5)
            self.consts.append(t)

    def calcular(self):
        self.text.config(state=tk.NORMAL)
        self.text.delete('1.0',tk.END)
        try:
            A=[[float(e.get().replace(',','.')) for e in row] for row in self.entries]
            b=[float(c.get().replace(',','.')) for c in self.consts]
        except:
            messagebox.showerror("Erro","Preencha todos os campos corretamente.")
            return
        M, sol, passos = gauss_passos(A,b)
        # Exibir passos
        for p in passos:
            self.text.insert(tk.END,p+"\n")
        # Solução final
        self.text.insert(tk.END,"\nSolução final:\n")
        vars = ['x','y','z','w','v','u','a','b','c','d']
        for i,v in enumerate(sol):
            self.text.insert(tk.END,f"{vars[i]} = {decimal_para_fracao(v)}\n")
        self.text.config(state=tk.DISABLED)

    def mostrar_instrucoes(self):
        win=tk.Toplevel(self.root)
        win.title("📘 Instruções")
        win.geometry("400x250")
        win.configure(bg="#fff")
        texto=(
            "🔶 Preencha o sistema 3×3 e clique em Calcular.\n"
            "🔶 Primeiro: L2 = L2 - L1.\n"
            "🔶 Segundo: L3 = L3 - 2·L1.\n"
            "🔶 Terceiro: L3 = L2 + L3 (correção importante).\n"
            "🔶 Em seguida: resolver z, depois y (substituindo z), e por fim x (substituindo y e z)."
        )

        tk.Label(win,text=texto,font=("Arial",12),bg="#fff",justify="left",wraplength=380).pack(padx=20,pady=20)
        tk.Button(win,text="Fechar",command=win.destroy,bg="#2196F3",fg="white").pack(pady=10)

if __name__ == "__main__":
    root=tk.Tk()
    App(root)
    root.mainloop()
