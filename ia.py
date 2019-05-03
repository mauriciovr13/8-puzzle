import time

class Problema:
    # tipo abstrato de dado problema definido no capitulo 3 do livro de IA ou nos slides
    # da aula 3

    def __init__(self, estado_inicial, operadores, teste_meta, funcao_custo):
        """
        Construtor de uma classe problema. O construtor recebe como parametros todos
        os componentes de um problema para construir um.
        @param estado_inicial: estado inicial que se encontra o problema (matriz)
        @param operadores: operadores que executam sobre o problema
        @param teste_meta: funcao que testa para ver se alcancamos o estado desejado
        @param funcao_custo: calcula a distancia do estado atual ao estado meta
        """
        self.estado_inicial = estado_inicial
        self.operadores = operadores
        self.teste_meta = teste_meta
        self.funcao_custo = funcao_custo
        self.comparacoes = 0

class No:
    # para realizar o algoritmo de busca em arvore, devemos ter o tipo no. O tipo abstrato
    # esta descrito nos slides da aula 3.

    def __init__(self, estado, no_pai, operador, profundidade, custo_caminho, ultima_expansao):
        """
        Construtor de um no para busca em arvore.
        @param estado: estado associado ao no corrente
        @param no_pai: no que deu origem ao no atual. "None" caso ele seja raiz
        @param operador: operador associado ao no
        @param profundidade: profundidade que no se encontra
        @param custo_caminho: custo do no atual ate o no raiz
        """
        self.estado = estado
        self.no_pai = no_pai
        self.operador = operador
        self.profundidade = profundidade
        self.custo_caminho = custo_caminho
        self.ultima_expansao = ultima_expansao

    def __str__(self):
        retorno = ""
        for linha in range(3):
            for coluna in range(3):
                print(self.estado["pecas"][linha][coluna], end=" ")
                retorno += str(self.estado["pecas"][linha][coluna]) + " "
            print()
            retorno += "\n"
        print("Profundidade: " , self.profundidade)
        print("Custo_caminho: " , self.custo_caminho)
        retorno += "Profundidade: " + str(self.profundidade) + "\n"
        retorno += "Custo_caminho: " + str(self.custo_caminho) + "\n\n"
        return retorno


def movimentacao_contraria(movimentacao):
    if(movimentacao == 'move_baixo'): return 'move_cima'
    elif(movimentacao == 'move_cima'): return 'move_baixo'
    elif(movimentacao == 'move_direita'): return 'move_esquerda'
    elif(movimentacao == 'move_esquerda'): return 'move_direita'
    else: return None

def expande(no, problema):
    """
    Funcao que expande um no e gera um conjunto de filhos
    @param no: no atual a ser expandido
    @param problema: problema no qual o no se encontra
    """
    filhos = [] # conjunto de filhos gerados por um determinado no

    for operacao in problema.operadores:
        resultado = operacao(no.estado)

        # se o no produz algum filho, entao coloque ele no conjunto de filhos
        if (not resultado is None) and (movimentacao_contraria(no.ultima_expansao) != operacao.__name__):
            # criando um novo no a partir da expansao do no atual
            filhos.append(No(resultado, no, operacao, no.profundidade + 1, no.custo_caminho + problema.funcao_custo(resultado), operacao.__name__))

    # retornando o conjunto resultante da expansao
    return filhos

def expande1(no, problema):
    """
    Funcao que expande um no e gera um conjunto de filhos. Essa eh a versao alternativa para a busca gulosa.
    @param no: no atual a ser expandido
    @param problema: problema no qual o no se encontra
    """
    filhos = [] # conjunto de filhos gerados por um determinado no

    for operacao in problema.operadores:
        resultado = operacao(no.estado)

        # se o no produz algum filho, entao coloque ele no conjunto de filhos
        #if not resultado is None:
        if (not resultado is None) and (movimentacao_contraria(no.ultima_expansao) != operacao.__name__):
            # criando um novo no a partir da expansao do no atual
            filhos.append(No(resultado, operacao, no, no.profundidade + 1, problema.funcao_custo(resultado), operacao.__name__))

    # retornando o conjunto resultante da expansao
    return filhos

def expande2(no, problema):
    """
    Funcao que expande um no e gera um conjunto de filhos. Essa eh a versao alternativa para a busca A*.
    @param no: no atual a ser expandido
    @param problema: problema no qual o no se encontra
    """
    filhos = [] # conjunto de filhos gerados por um determinado no

    for operacao in problema.operadores:
        resultado = operacao(no.estado)

        # se o no produz algum filho, entao coloque ele no conjunto de filhos
        if (not resultado is None) and (movimentacao_contraria(no.ultima_expansao) != operacao.__name__):
            # criando um novo no a partir da expansao do no atual
            #filhos.append(No(resultado, operacao, no, no.profundidade + 1,no.profundidade + 1 + problema.funcao_custo(resultado), operacao.__name__))
            filhos.append(No(resultado, no, operacao, no.profundidade + 1, problema.funcao_custo(resultado), operacao.__name__))

    # retornando o conjunto resultante da expansao
    return filhos



def busca(problema, enfileira):
    c = 0
    """
    Funcao que realiza um algoritmo de busca. A estrategia de busca depende da
    funcao enfileira passada como argumento. Ex: FIFO representa busca em largura
    LIFO representa busca em profundidade.
    @param problema: problema a ser resolvido
    @param enfileira: funcao de enfileiramento de nos
    """
    nos = [No(problema.estado_inicial, None, None, 0, 0, None)] # criando uma fila com o estado inicial
    visitados = [] # mantem os nos que já foram visitados para nao visitá-los novamente
    while (True):
        if nos == []: return None # retorna fracasso caso a lista seja vazia

        no = nos.pop(0)
        #print(problema.teste_meta(no.estado))
        
        c = c + 1
        problema.comparacoes = c
        
        #print(no)
        noSTR = no.__str__()
        #print(noSTR)
        #escrever no arquivo
        arquivo = open('log.txt', 'r') # Abra o arquivo (leitura)
        conteudo = arquivo.readlines()
        conteudo.append(noSTR)   # insira seu conteúdo

        arquivo = open('log.txt', 'w') # Abre novamente o arquivo (escrita)
        arquivo.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.

        arquivo.close()

        #time.sleep(10)
        
        if problema.teste_meta(no.estado): return no.estado # verifica se o estado atual e a meta
        
        # caso nao seja a meta, o no e expandido
        if not no.estado in visitados:
            nos = enfileira(expande(no, problema), nos)
            visitados.append(no.estado)
            #print(visitados)
        #print (len(nos))

def tira_melhor(nos):
    '''
    Função que recebe uma lista de nos e retira o nó com o menor custo, retira da lista e retorna
    pra quem chamou
    @param nos: lista de nos
    @return aux: no com o menor custo de caminho
    '''
    aux = nos[0]
    for i in nos:
        if aux.custo_caminho > i.custo_caminho:
            aux = i
    nos.remove(aux)
    return aux



def buscagulosa(problema, enfileira):
    c = 0
    """
    Funcao que realiza um algoritmo de busca. A estrategia de busca depende da
    funcao enfileira passada como argumento. Ex: FIFO representa busca em largura
    LIFO representa busca em profundidade.
    @param problema: problema a ser resolvido
    @param enfileira: funcao de enfileiramento de nos
    """
    nos = [No(problema.estado_inicial, None, None, 0, 0)] # criando uma fila com o estado inicial
    visitados = []
    while (True):
        if nos == []: return None # retorna fracasso caso a lista seja vazia

        no = tira_melhor(nos)
        #print no.custo_caminho
        #print(problema.teste_meta(no.estado))
        # verifica se o estado atual e a meta
        c = c + 1
        problema.comparacoes = c
        if problema.teste_meta(no.estado): return no.estado
        # caso nao seja a meta, o no e expandido
        if not no.estado in visitados:
            nos = enfileira(expande1(no, problema), nos)
            visitados.append(no.estado)



def buscaaestrela(problema, enfileira):
    c = 0
    """
    Funcao que realiza um algoritmo de busca. A estrategia de busca depende da
    funcao enfileira passada como argumento. Ex: FIFO representa busca em largura
    LIFO representa busca em profundidade.
    @param problema: problema a ser resolvido
    @param enfileira: funcao de enfileiramento de nos
    """
    nos = [No(problema.estado_inicial, None, None, 0, 0, None)] # criando uma fila com o estado inicial
    visitados = [] # lista com os vertices já visitados
    while (True):
        if nos == []: return None # retorna fracasso caso a lista seja vazia

        no = tira_melhor(nos) # pega o no com o menor custo do caminho

        #print no.custo_caminho
        #print(problema.teste_meta(no.estado))
        noSTR = no.__str__()
        
        c = c + 1
        problema.comparacoes = c
        # verifica se o estado atual e a meta
        if problema.teste_meta(no.estado): return no.estado

        # caso nao seja a meta, o no e expandido
        if not no.estado in visitados:
            #nos = enfileira(expande2(no, problema), nos)
            nos = expande2(no, problema)
            visitados.append(no.estado)
            # print(visitados)
        #print len(nos)
