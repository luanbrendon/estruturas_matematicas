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
    print('Matriz aumentada inicial:')
    print_matriz(M)

    # Eliminação
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
    print('Solução final:', x)
    return x


if __name__ == '__main__':
    A = [
        [3, 2, -4],
        [2, 3,  3],
        [5, -3, 1]
    ]
    b = [3, 15, 14]
    eliminacao_gaussiana(A, b)