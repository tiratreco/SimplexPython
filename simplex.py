
def lerMatriz(entrada):
    tableau = []
    with open(entrada, 'r') as arquivo:
        for linha in arquivo.readlines():
            tableau.append(linha.split(' '))
    for l in range(len(tableau)):
        for n in range(len(tableau[0])):
            if l==len(tableau)-1 and n==len(tableau[-1])-1:
                if 'max' in tableau[-1][-1]:
                    tipo = 'max'
                    try: tableau[-1][-1] = float(tableau[-1][-1].replace('max', ''))
                    except:tableau[-1][-1] = 0.0
                else:
                    tipo = 'min'
                    try: tableau[-1][-1] = float(tableau[-1][-1].replace('min', ''))
                    except: tableau[-1][-1] = 0.0
            else: tableau[l][n]=float(tableau[l][n])
    return tableau, tipo

#imprime a tabela (precisão de 2 casas)
def imprimirTableau(tableau, tipo, bases):
    maiores = [0]*len(tableau[0])
    for c in range(len(tableau[0])):
        maior = 2
        for l in range(len(tableau)):
            if len('{:.2f}'.format(tableau[l][c]))>maior: maior = len('{:.2f}'.format(tableau[l][c]))
            maiores[c]=maior
    print('base  |', end = '')
    for c in range(len(tableau[0])):
        if c==len(tableau[0])-1:print(''+(' '*maiores[c])+'b', end='')
        else:print(''+(' '*maiores[c])+'x'+str(c+1)+' |', end='')
    print('\n-', end='')
    for c in range(len(tableau[0])):
        print('-'*(5+maiores[c]), end='')
    print()
    for l in range(len(tableau)):
        if l<len(tableau)-1: print(' '*(4-len(bases[l])) + bases[l] , end='')
        else: print('    ', end='')
        for n in range(len(tableau[0])):
            aux = len('{:.2f}'.format(tableau[l][n]))
            print('  | ', end ='')
            if l == len(tableau)-1 and n == len(tableau[0])-1 and tableau[-1][-1]==0: print(('  '*(maiores[n]-aux))+'L', end='')
            elif l == len(tableau)-1 and n == len(tableau[0])-1 and tableau[-1][-1]>0: print(('  '*(maiores[n]-aux))+'L+'+str(tableau[-1][-1]), end='')
            elif l == len(tableau)-1 and n == len(tableau[0])-1: print((' '*(maiores[n]-aux))+' L'+'{:.2f}'.format(tableau[-1][-1]), end='')
            else: print((' '*(maiores[n]-aux))+'{:.2f}'.format(tableau[l][n]), end='')
        print()
    print()

def canonizar(tableau, bases):
    for b in range(len(bases)):
        coluna = int(bases[b][1:])-1
        if not tableau[-1][coluna] == 0:
            aux = tableau[-1][coluna]*-1
            for n in range(len(tableau[0])):
                tableau[-1][n]=tableau[-1][n]+tableau[b][n]*aux

#retorna o indice da coluna para a nova base
#returna None caso esteja na melhor solução
#deve estar na forma canonica
def novaBase(tableau, tipo):
    aux = 0
    aux2 = 0
    if tipo=='max':
        for n in range(len(tableau[-1])):
            if tableau[-1][n]>aux:
                aux=tableau[-1][n]
                aux2=n
        if aux==0: return None
        return aux2
    for n in range(len(tableau[-1])-1):
        if tableau[-1][n]<aux:
            aux=tableau[-1][n]
            aux2=n
    if aux==0: return None
    return aux2

#retorna a linha da base que deve sair
#retorna None quando não há linha para sair
def testeRazao(tableau, saindo):
    menor = []
    coluna = []
    for n in range(len(tableau)-1):
        if tableau[n][saindo] > 0:
            menor.append(tableau[n][-1]/tableau[n][saindo])
            coluna.append(n)
    if len(coluna)==0: return None
    return coluna[menor.index(min(menor, key=float))]
    
def escalonar(tableau, entra, sai):
    if not tableau[sai][entra]==1:
        aux = (tableau[sai][entra])
        for n in range(len(tableau[0])):
            tableau[sai][n]=tableau[sai][n]/aux
    for l in range(len(tableau)):
        if not l == sai:
            aux = tableau[l][entra]*-1
            for n in range(len(tableau[0])):
                tableau[l][n]=tableau[l][n]+(tableau[sai][n]*aux)

def simplex(tableau, tipo):
    base = acharBases(tableau)
    if (not len(base)==len(tableau)-1):
        print('Não foi encontrada uma base inicial para o problema.')
        return
    for l in tableau: 
        for n in range(len(l[:-1])):
            if l[-1] < 0:
                print('O problema não está na forma padrão.')
                return
    print('\nBase inicial: ', end='')
    print(base)
    imprimirTableau(tableau, tipo, base)
    print('\nColocando na forma canônica:')
    canonizar(tableau, base)
    imprimirTableau(tableau, tipo, base)
    while True:
        baseEntra = novaBase(tableau, tipo)
        if baseEntra == None:
            print('Melhor solução encontrada')
            return
        baseSai = testeRazao(tableau, baseEntra)
        if baseSai == None:
            print('Não foi encontrada uma base para sair')
            return
        print('Saindo '+str(base[baseSai])+' e entrando x'+ str(baseEntra+1))
        escalonar(tableau, baseEntra, baseSai)
        base[baseSai]='x'+str(baseEntra+1)
        imprimirTableau(tableau, tipo, base)

def acharBases(tableau):
    bases = []
    for c in range(len(tableau[0])-1):
        aux = 0
        aux2 = 0
        for l in range(len(tableau)-1):
            if not tableau[l][c]==0 and not tableau[l][c]==1:
                aux=-1
            elif tableau[l][c]==1 and not aux==-1:
                aux+=1
                aux2=c
        if aux==1:
            bases.append('x'+str(aux2+1))
    base=[]
    print(bases)
    for l in range(len(tableau)-1):
        for n in range(len(tableau[0])):
            for b in range(len(bases)):
                if tableau[l][n]==1 and ('x'+str(n+1) in bases[b]):
                    base.append(bases[b])
    return base

while True:
    entrada = input('Entre com um arquivo (vazio:sair): ')
    if entrada=='': break
    try: 
        tableau, tipo = lerMatriz(entrada)
        erro=False
    except:
        print('Erro de leitura do arquivo!')
        erro=True
    if not erro:
        simplex(tableau, tipo)