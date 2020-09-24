
def lerMatriz():
    restricao = []
    with open('dados.txt', 'r') as arquivo:
        objetivo = arquivo.readline()
        for linha in arquivo.readlines():
            restricao.append(linha.split(' '))
    return objetivo, restricao


def listaVariaveis(restricao):
    var = []
    for r in restricao:
        for n in r:
            if 'x' in n and 'x'+n.split('x')[1] not in var:
                var.append('x'+n.split('x')[1])
    return var

def formaPadrao(objetivo, restricao):
    numVariaveis = len(listaVariaveis(restricao))

    #variavel de folga ou de excesso
    padrao = []
    for r in restricao[:-1]:
        linha = []
        for e in r:
            if e == '<=':
                numVariaveis += 1
                linha.append('+')
                linha.append('x'+ str(numVariaveis))
                linha.append('=')
            elif e == '>=':
                numVariaveis += 1
                linha.append('-')
                linha.append('x'+ str(numVariaveis))
                linha.append('=')
            else:
                linha.append(e)
        padrao.append(linha)

    for r in padrao:
        for e in range(len(r)-1):
            if r[e] == '=' and r[e+1] == '-':
                #multiplicar restricao por -1
                if r[0]=='-':
                    del(r[0])
                else:
                    r.insert(0, '-')
                el = 1
                while el < len(r):
                    if r[el]=='-':
                        r[el]='+'
                    elif r[el]=='+':
                        r[el]='-'
                    el+=1
        if r[-2] == '+': del(r[-2])
        
    #restrição de negatividade
    linha = []
    for v in listaVariaveis(padrao)[:-1]:
        linha.append(v)
        linha.append(',')
    linha.append(listaVariaveis(padrao)[-1])
    linha.append('>=')
    linha.append('0')
    padrao.append(linha)

    return padrao
            
def escreverSaida(objetivo, padrao):
    with open('saida.txt', 'w') as arquivo:
        arquivo.write(objetivo)
        for linha in padrao:
            for e in linha:
                if '\n' not in e:
                    arquivo.write(e + ' ')
                else:
                    arquivo.write(e)
    return objetivo, restricao

objetivo, restricao = lerMatriz()
padrao = formaPadrao(objetivo, restricao)


#print(objetivo)
#print(restricao)

#print(padrao)

escreverSaida(objetivo, padrao)