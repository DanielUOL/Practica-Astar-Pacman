def readFileretList(file):
    archivo = open(input_file,'r') 
    return [[ch for ch in line.strip()] for line in archivo.readlines()]

def genVertices(list_):
    return [(i,j) for i in range(len(list_)) for j in range(len(list_[0]))
    if list_[i][j] != '%']

def retAristas(list_):
    A = []
    for i in range(len(list_)):
        for j in range(len(list_[0])):

            if j == (len(list_[0]) - 1):
                if list_[i][j] != '%' and list_[i][0] != '%':
                    A.append([(i,j),(i,0)])
            elif list_[i][j] != '%' and list_[i][j + 1] != '%':
                A.append([(i,j),(i,j + 1)])

            if i == (len(list_) - 1):
                if list_[i][j] != '%' and list_[0][j] != '%': 
                    A.append([(i,j),(0,j)])
            elif list_[i][j] != '%' and list_[i + 1][j] != '%': 
                A.append([(i,j),(i + 1,j)])
    return A

class Nodo:
    def __init__(self, posicion):
        self.r = posicion[0] # Renglon
        self.c = posicion[1] # Columna
        self.pos = (self.r,self.c) #Tupla (Renglon,Columna)
        self.distancia = 0
        self.h = 0
        self.costo = 0
    
    def Expandir(self, distpadre, fruta):
        self.distancia = distpadre + 1 # Distancia Recorrida
        self.h = abs(fruta[0]-self.r) + abs(fruta[1]-self.c) # Distancia Manhattan
        self.costo = self.distancia + self.h # Costo Total = Distancia Recorrida + Distancia Manhattan

def GenerarHijosA(pacman,aristas,visitados):
    hijos = []
    
    #Verificamos si se puede mover hacia arriba
    if (pacman.r-1,pacman.c) not in visitados:
        if [(pacman.r-1,pacman.c),(pacman.r,pacman.c)] in aristas:
            hijos.append((pacman.r-1,pacman.c))
            
    #Verificamos si se puede mover hacia la izquierda
    if (pacman.r,pacman.c-1) not in visitados:
        if [(pacman.r,pacman.c-1),(pacman.r,pacman.c)] in aristas:
            hijos.append((pacman.r,pacman.c-1))
            
    #Verificamos si se puede mover hacia la derecha
    if (pacman.r,pacman.c+1) not in visitados:
        if [(pacman.r,pacman.c),(pacman.r,pacman.c+1)] in aristas:
            hijos.append((pacman.r,pacman.c+1))
            
    #Verificamos si se puede mover hacia abajo
    if (pacman.r+1,pacman.c) not in visitados:
        if [(pacman.r,pacman.c),(pacman.r+1,pacman.c)] in aristas:
            hijos.append((pacman.r+1,pacman.c))
            
    return hijos

def A_STAR(grafo, pacman, fruta):
    aristas = grafo[0]
    expandidos = [] # Lista para los nodos disponibles para moverse
    visitados = [] # Lista para los nodos que ya se visitaron
    hijos = []
    padres = {} # Diccionario para guardar la relación de Hijo-Padre de cada nodo expandido
    ruta = []
    nodo = Nodo(pacman)
    expandidos.append(nodo)
    # Mientras haya nodos disponibles para moverse se iterará el algoritmo
    while ( expandidos ):
        mincost = 1000 # Se establece un costo mínimo muy alto para encontrar el menor en la lista de expandidos
        # Se busca el nodo expandido con el menor costo
		for n in expandidos:
            if n.costo < mincost:
                nodo = n
                mincost = n.costo
        # Se verifica si el nodo actual es la posición de la fruta
        if nodo.pos == fruta:
            nd = nodo.pos
            while ( nd in padres ):
                ruta.append(padres[nd])
                nd = padres[nd]
            ruta.reverse()
            print(len(ruta))
            for r in ruta:
                print(r[0], r[1])
            print(fruta[0], fruta[1])
            break
        expandidos.remove(nodo) # Se elimina el nodo actual de explorados
        visitados.append(nodo.pos) # El nodo actual se agrega a visitados
        #Se generan los hijos del nodo actual,
        #con la condición de que no se ecnuentren en visitados.
        hijos = GenerarHijosA(nodo,aristas,visitados)
        for h in hijos:
            repetido = False
            h = Nodo(h)
            # Si el hijo generado no se encuentra en el diccionario de Hijo-Padre, se agrega
            if h.pos not in padres:
                padres[h.pos] = nodo.pos
            h.Expandir(nodo.distancia,fruta)
            # Si el nodo hijo ya se encuentra en expandidos,
            # se comparan los costos de los hijos repetidos
            # El nodo con el menor costo se queda en la lista
            # y su padre se sustituye en el diccionario de Hijo-Padre.
            for n in expandidos:
                if h.pos == n.pos:
                    repetido = True
                    if h.costo < n.costo:
                        n = h
                        padres[h.pos] = nodo.pos
                        break
            if repetido == False:
                expandidos.append(h)

input_file = 'tablero1.txt' # Nombre del archvio de texto que contiene los datos de entrada para el programa
archivo = open(input_file,'r')

# Se leen las posiciones de Pacman y la fruta
pacmanlst = ((archivo.readline()).strip()).split(' ')
frutalst = ((archivo.readline()).strip()).split(' ')

# Se guardan todas líneas del archivo de texto en una lista,
# eliminando las primeras 3 líneas, para dejar sólo el tablero
lista1 = readFileretList(input_file)
lista1.pop(0)
lista1.pop(0)
lista1.pop(0)

# Se crean tuplas de números enteros para representar las posiciones de pacman y fruta
pacman = (int(pacmanlst[0]),int(pacmanlst[1]))
fruta = (int(frutalst[0]),int(frutalst[1]))

# Se generan los vértices y aristas para el grafo
vertices = genVertices(lista1)
aristas = retAristas(lista1)

# Se crea un grafo con los vertices y aristas obtenidos
grafo = (aristas,vertices)

# Se llama la función de A_STAR enviando el grafo, la posición de pacman y la posición de la fruta
A_STAR(grafo,(pacman[0],pacman[1]),(fruta[0],fruta[1]))