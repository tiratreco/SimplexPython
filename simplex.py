
def lerMatriz():
    tableau = []
    with open('tableau.txt', 'r') as arquivo:
        for linha in arquivo.readlines():
            tableau.append(linha.split(' '))
    for l in range(len(tableau)):
        for n in range(len(tableau[0])):
            if l==len(tableau)-1 and n==len(tableau[-1])-1:
                tipo = tableau[-1][-1]
                tableau[-1][-1] = 0.0
            else: tableau[l][n]=float(tableau[l][n])

    return tableau, tipo



def imprimirTableau(tableau, tipo):
    print('Tableau')
    print('-' * len(tableau[0])*3)
    maiores = [0]*len(tableau[0])
    for c in range(len(tableau[0])):
        maior = 2
        for l in range(len(tableau)):
            if len(str(int(tableau[l][c])))>maior: maior = len(str(int(tableau[l][c])))
            maiores[c]=maior
    for l in range(len(tableau)):
        for n in range(len(tableau[0])):
            aux = len(str(int(tableau[l][n])))
            print('  | ', end ='')
            if l == len(tableau)-1 and n == len(tableau[0])-1: print((' '*(maiores[n]-aux))+tipo, end='')
            else: print((' '*(maiores[n]-aux))+str(tableau[l][n]), end='')
        print()


tableau, tipo = lerMatriz()
imprimirTableau(tableau, tipo)