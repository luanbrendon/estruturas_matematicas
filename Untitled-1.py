import sys

def print_matriz(M):
    """Imprime a matriz aumentada M linha a linha, arredondando para 6 casas decimais."""
    for row in M:
        linha = []
        for elem in row:
            if isinstance(elem, float):
                linha.append(round(elem, 6))
            else:
                linha.append(elem)
        print(linha)
    print()


def eliminacao_gaussiana(A, b):
    """
    Resolve Ax=b pelo método de eliminação de Gauss com pivoteamento parcial,
    exibindo cada etapa e arredondando cálculos para evitar imprecisões.
    """
    n = len(A)
    # Converte para float e cria matriz aumentada
    M = [[float(val) for val in row] + [float(b_i)] for row, b_i in zip(A, b)]
    print('\nMatriz aumentada inicial:')
    print_matriz(M)

    # Eliminação por colunas
    for k in range(n):
        max_row = max(range(k, n), key=lambda i: abs(M[i][k]))
        print(f'Selecionando pivô na coluna {k}, linha {max_row}')
        M[k], M[max_row] = M[max_row], M[k]
        print('Matriz após troca de linhas:')
        print_matriz(M)

        for i in range(k+1, n):
            fator = M[i][k] / M[k][k]
            print(f'Eliminando M[{i}][{k}] com fator = {round(fator,6)}')
            for j in range(k, n+1):
                antes = M[i][j]
                M[i][j] -= fator * M[k][j]
                print(f'  M[{i}][{j}] = {round(antes,6)} - {round(fator,6)}*{round(M[k][j],6)} = {round(M[i][j],6)}')
        print(f'Matriz após eliminação da coluna {k}:')
        print_matriz(M)

    # Substituição retroativa
    x = [0]*n
    print('Substituição retroativa:')
    for i in range(n-1, -1, -1):
        soma = sum(M[i][j]*x[j] for j in range(i+1, n))
        print(f' Soma para x[{i}] = {round(soma,6)}')
        raw = (M[i][n] - soma) / M[i][i]
        x[i] = round(raw, 6)
        print(f' x[{i}] = ({round(M[i][n],6)} - {round(soma,6)}) / {round(M[i][i],6)} = {x[i]}')

    # Impressão formatada da solução
    print('\nSolução final:')
    # Gera rótulos para as variáveis
    if n == 3:
        labels = ['x', 'y', 'z']
    else:
        labels = [f'x{i+1}' for i in range(n)]
    for label, val in zip(labels, x):
        print(f' {label} = {val}')
    return x


def main():
    """Interface de linha de comando para resolver sistemas lineares pelo método de Gauss."""
    while True:
        try:
            n = int(input('Digite o número de equações (n): '))
        except ValueError:
            print('Valor inválido. Digite um inteiro.')
            continue
        
        A = []
        print(f'Informe os {n} coeficientes de cada linha, separados por espaço:')
        for i in range(n):
            while True:
                linha = input(f'Linha {i+1}: ').strip().split()
                if len(linha) != n:
                    print(f'Precisam ser {n} valores. Tente novamente.')
                    continue
                try:
                    A.append([float(x) for x in linha])
                    break
                except ValueError:
                    print('Entradas inválidas. Digite números.')
        
        while True:
            b_vals = input(f'Digite os {n} termos independentes (b), separados por espaço: ').strip().split()
            if len(b_vals) != n:
                print(f'Precisam ser {n} valores. Tente novamente.')
                continue
            try:
                b = [float(x) for x in b_vals]
                break
            except ValueError:
                print('Entradas inválidas. Digite números.')

        eliminacao_gaussiana(A, b)

        again = input('Deseja resolver outro sistema? (s/n): ').strip().lower()
        if again != 's':
            print('Encerrando.')
            break

if __name__ == '__main__':
    main()
