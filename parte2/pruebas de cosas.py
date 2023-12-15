from heapq import heappop, heappush
import csv
class Mapa:
    #se crea la clase mapa
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.datos=self.leer_csv() #lee el csv y lo escribe en una lista de lista 
        self.parking=self.estado_parking() #encuentra la posición del parking
        self.dimensiones=self.calcular_dimensiones() #se calculan las dimensiones del mapa
        self.filas=self.dimensiones[0] #dimensión vertical
        self.columnas=self.dimensiones[1] #dimensión horizontal
        self.distancias = self.DistanciasCalculadas()

    def leer_csv(self):
        #lee el csv y lo escribe en una lista de listas 
        datos = []
        with open(self.nombre_archivo, 'r') as archivo:
            lector_csv = csv.reader(archivo, delimiter=';')
            for fila in lector_csv:
                datos.append(fila)
        return datos
    
    def estado_parking(self):
        #recorre todo el mapa para encontrar la posición del parking
        contadorFila=-1
        for fila in self.datos:
            contadorFila+=1
            contadorColumna=-1
            for estado in fila:
                contadorColumna+=1
                if estado=='P':
                    return (contadorFila, contadorColumna) 
    
    def calcular_dimensiones(self):
        #se calculan las dimensiones reales del mapa
        contadorFila=-1
        for fila in self.datos:
            contadorFila+=1
            contadorColumna=-1
            for estado in fila:
                contadorColumna+=1
        return (contadorFila, contadorColumna)
    
    def distanciaMinima(self, inicio):
        #se calcula la distancia minima que hay desde la posición pasada por parámetros, hasta todas las casillas del mapa
        distanciasMapa=[]
        #se creará una lista de listas del tamaño del mapa, pero en vez de guardar la posición, poserá el coste que se tarda en llegar a él
        for fila in self.datos:
            distancias = [100] * (self.dimensiones[1]+1)
            distanciasMapa.append(distancias)

        abierta = [(0, list(inicio))] 
        distanciasMapa[inicio[0]][inicio[1]] =0
        cerrada=[]   
        while len(abierta) !=0:
            #iremos desarrollando cada posición hacia sus posibles movimientos, sumandole el valor acumulado, y guardando el valor más pequeño
            contador =0
            primeroLista= abierta[0][1]
            #se comprobará que el estado solo se desarrollará si no ha sido desarrollado con anterioridad, evitando bucles
            for estado in cerrada:
                if primeroLista == estado[1]:
                    contador+=1
            if contador ==0:       
                #si no ha sido expandido anteriormente, se llama a la clase estado para poder utilizar las funcionalidades de ese estado   
                expandido = Casilla(primeroLista, self.datos, self.dimensiones)
                costeExpandido = distanciasMapa[expandido.posicion[0]][expandido.posicion[1]]
                vecinos = expandido.operadores_disponibles
                cerrada.append(abierta[0]) #marcaremos este estado expandido como cerrado
                abierta.remove(abierta[0]) 
                for estado in vecinos:
                    if estado!=None:
                        #solo para los movientos posibles, obtendremos cuánto vale el moverse a cada uno de los vecinos
                        tipo = self.datos[estado[0]][estado[1]]
                        if tipo=="2":
                            coste=2
                        else:
                            coste=1
                        coste_actual= distanciasMapa[estado[0]][estado[1]]
                        costeAcumulado = costeExpandido+coste  #este coste de moverse al vecino, se le sumará al coste acumulado que tiene llegar al estado actual
                        if costeAcumulado < coste_actual: #si este coste es menor que el que se tenía antes para llegar a ese estado, se actualiza
                            distanciasMapa[estado[0]][estado[1]] = costeAcumulado
                            abierta.append((costeAcumulado, estado))
                        else:
                            abierta.append((coste_actual, estado))
            else:
                abierta.remove(abierta[0])  #si ya ha sido expandido, simplemente se pasará al siguiente

            #para ir expandiendo los estado menos costosos, se ordena la lista de abiertos de menor a mayor
            #abierta = sorted(abierta, key = lambda tupla:tupla[0])

            #print(distanciasMapa)
            #print("lista abierta", abierta)
            #print("lista cerrada", cerrada) 
        return cerrada #devolviendo una lista de tuplas en la que el primer elemento de la tupla es el coste que se necesita para ir a la posición y el segundo, la posición a la que se iría por ese coste

    def DistanciasCalculadas(self):
        mapaConDistancias = []
        for fila in range(self.filas+1):
            for columna in range(self.columnas+1):
                calculoDistancias = self.distanciaMinima([fila,columna])
                posicion = [fila, columna]
                union = (posicion, calculoDistancias)
                mapaConDistancias.append(union)
        return mapaConDistancias
class Casilla:
    #se crea la clase casilla
    def __init__ (self, posicion, datos, dimensiones):
        self.posicion=posicion #la cual es una lista con [posicionVertical, posicionHorizontal]
        self.datos = datos
        self.dimensiones = dimensiones
        #atributo que permite que movimientos están permitidos y a qué estado llevará
        self.operadores_disponibles = [self.moverArriba(self.posicion, self.datos), self.moverAbajo(self.posicion, self.datos, self.dimensiones), self.moverDerecha(self.posicion, self.datos, self.dimensiones), self.moverIzquierda(self.posicion, self.datos)]
    
    def moverArriba(self, posicion, datos):
        #comprueba si se puede realizar el operador moverArriba
        if posicion[0] > 0:
            posicionArriba= [posicion[0]-1, posicion[1]]
            casillaArriba = datos[posicionArriba[0]][posicionArriba[1]]
            if casillaArriba!="X":
                nuevaPosicion = posicionArriba
                return nuevaPosicion
            return None
        return None
    
    def moverAbajo(self, posicion, datos, dimensiones):
        #comprueba si se puede realizar el operador moverAbajo
        if posicion[0] < dimensiones[0]:
            posicionAbajo= [posicion[0]+1, posicion[1]]
            casillaAbajo = datos[posicionAbajo[0]][posicionAbajo[1]]
            if casillaAbajo!="X":
                nuevaPosicion = posicionAbajo
                return nuevaPosicion
            return None
        return None
    
    def moverDerecha(self, posicion, datos, dimensiones):
        #comprueba si se puede realizar el operador moverDerecha
        if posicion[1] < dimensiones[1]:
            posicionDerecha= [posicion[0] , posicion[1]+1]
            casillaDerecha = datos[posicionDerecha[0]][posicionDerecha[1]]
            if casillaDerecha!="X":
                nuevaPosicion = posicionDerecha
                return nuevaPosicion
            return None
        return None
    
    def moverIzquierda(self, posicion, datos):
        #comprueba si se puede realizar el operador moverIzquierda
        if posicion[1] > 0:
            posicionIzquierda= [posicion[0] , posicion[1]-1]
            casillaIzquierda = datos[posicionIzquierda[0]][posicionIzquierda[1]]
            if casillaIzquierda!="X":
                nuevaPosicion = posicionIzquierda
                return nuevaPosicion
            return None
        return None
    
def pasosRecorridos(inicio, fin, datos, dimensiones):
    #se calcula la distancia minima que hay desde la posición pasada por parámetros, hasta todas las casillas del mapa
        distanciasMapa=[]
        #se creará una lista de listas del tamaño del mapa, pero en vez de guardar la posición, poserá el coste que se tarda en llegar a él
        contador_x = 0
        for fila in datos:
            distancias = [[100, [[contador_x,y]]] for y in range(dimensiones[1]+1)]
            distanciasMapa.append(distancias)
            contador_x += 1

        abierta = [(0, list(inicio))] 
        distanciasMapa[inicio[0]][inicio[1]][0] =0
        distanciasMapa[inicio[0]][inicio[1]][1] = inicio
        cerrada=[]   
        print(distanciasMapa)
        while len(abierta) !=0:
            #print("cerrada:",cerrada)
            #iremos desarrollando cada posición hacia sus posibles movimientos, sumandole el valor acumulado, y guardando el valor más pequeño
            contador =0
            primeroLista= abierta[0][1]
            #se comprobará que el estado solo se desarrollará si no ha sido desarrollado con anterioridad, evitando bucles
            for estado in cerrada:
                if primeroLista == estado[1]:
                    contador+=1
            #print("voy a ver abierta", abierta)
            if contador ==0:
                expandido = Casilla(primeroLista, datos, dimensiones)
                costeExpandido = distanciasMapa[expandido.posicion[0]][expandido.posicion[1]][0]
                print("fallo",costeExpandido)
                vecinos = expandido.operadores_disponibles
                valor = abierta[0]
                cerrada.append(abierta[0]) #marcaremos este estado expandido como cerrado
                abierta.remove(abierta[0])
                for estado in vecinos:
                    if estado!=None:
                        #solo para los movientos posibles, obtendremos cuánto vale el moverse a cada uno de los vecinos
                        tipo = datos[estado[0]][estado[1]]
                        if tipo=="2":
                            coste=2
                        else:
                            coste=1
                        casillasRecorridas = distanciasMapa[estado[0]][estado[1]][1]
                        #print("las casillas recorridas", casillasRecorridas)
                        casillasRecorridasReal = distanciasMapa[valor[1][0]][valor[1][1]][1]
                        #print("las casillas realmente", casillasRecorridasReal)
                        coste_actual= distanciasMapa[estado[0]][estado[1]][0]
                        casillasRecorridasNuevas = casillasRecorridas + [casillasRecorridasReal]
                        #print("las casillas final", casillasRecorridasNuevas)
                        costeAcumulado = costeExpandido+coste  #este coste de moverse al vecino, se le sumará al coste acumulado que tiene llegar al estado actual
                        if costeAcumulado < coste_actual: #si este coste es menor que el que se tenía antes para llegar a ese estado, se actualiza
                            distanciasMapa[estado[0]][estado[1]][0] = costeAcumulado
                            distanciasMapa[estado[0]][estado[1]][1] = casillasRecorridasNuevas
                            abierta.append((costeAcumulado, estado,casillasRecorridasNuevas))
                        else:
                            abierta.append((coste_actual, estado, casillasRecorridas))
            else:
                abierta.remove(abierta[0])  #si ya ha sido expandido, simplemente se pasará al siguiente
        for posicion in cerrada:
            if posicion[1] == fin:
                solucion = posicion
            print(posicion)
        print(solucion)
        aplanada = aplanar_lista(solucion[2])
        coordenadas = juntar(aplanada)
        print(coordenadas)

def aplanar_lista(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(aplanar_lista(item))
        
        else:
            result.append(item)
    return result

def juntar(aplanada):
    contador =0 
    lista = []
    final =[]
    for numero in aplanada:
        if contador == 0:
            lista.append(numero)
            contador+= 1
        elif contador == 1:
            lista.append(numero)
            final.append(lista.copy())
            lista = []
            contador = 0

        print("el numero es", contador)
        
    return final



        

nombre_archivo = 'parte2/entrada2.csv'
#creamos el mapa con ese archivo
grafo = Mapa(nombre_archivo)
hola = pasosRecorridos([0,0],[3,1], grafo.datos, grafo.dimensiones)
