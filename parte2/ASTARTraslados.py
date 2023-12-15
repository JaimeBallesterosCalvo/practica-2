import csv
import copy
import time
import sys
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
    
class Vehiculo:
    #se crea la clase vehículo, la cual llevará a los pacientes y saldrá y volverá al parking
    def __init__(self, datos, posicionActual):
        self.datos = datos
        self.posicionActual= posicionActual #en todo momento, sabe en que posición está, la cual se irá actualizando 
        self.pacientesVehiculo=[] #lista que contiene los pacientes que lleva
        self.llevandoContagiados = [] #lista que contiene los pacientes contagiados que lleva
        self.llevandoNoContagiados = [] #lista que contiene los pacientes NO contagiados que lleva
        self.energia = 50 #energía inicial con la que empieza el vehiculo
        self.hojadeRuta= self.pacientesRecoger(self.datos) #la hoja de ruta indica que pacientes le faltan por recoger +
        self.costeHastaAhora = 0 
        self.camino = [list(posicionActual)]
    
    def pacientesRecoger(self, datos):
        #la función recorrera el mapa, guardando la dirección de donde están cada paciente y los hospitales
        noContagiados= []
        contagiados=[]
        hospitalContagiado = []
        hospitalNoContagiado = []
        parking = []
        contadorFila=-1
        for fila in datos:
            contadorFila+=1
            contadorColumna=-1
            for estado in fila:
                contadorColumna+=1
                if estado =="N":
                    noContagiados.append([contadorFila, contadorColumna])
                elif estado =="C":
                    contagiados.append([contadorFila, contadorColumna ])
                elif estado =="CC":
                    hospitalContagiado.append([contadorFila, contadorColumna ])
                elif estado =="CN":
                    hospitalNoContagiado.append([contadorFila, contadorColumna ])
                elif estado == "P":
                    parking.append([contadorFila, contadorColumna ])
        totalPacientes=noContagiados+contagiados 
        return [totalPacientes, noContagiados, contagiados, hospitalContagiado, hospitalNoContagiado, parking]
    

    
#--------------------------funciones-----------------------------------------------------    
#desarrollo de las funciones que iremos utilizando
def creacionDeHeuristica1(distancia, estado):
    posicionActual = estado[0]
    totalPacientes = estado[5][0]
    llevandoContagiados = estado[3]
    llevandoNoContagiados = estado[2]
    energia = estado[4]
    
    heuristica  = 0
    for paciente in totalPacientes:
        for fila in distancia:
            if fila[0] == posicionActual:
                for columna in fila[1]:
                    if columna[1]== paciente:
                        heuristica= max(heuristica,columna[0])
    totalPacientesARecoger = max(0,len(totalPacientes)-1)
    heuristica += totalPacientesARecoger


    return heuristica

def creacionDeHeuristica2(distancia, estado):
    posicionActual = estado[0]
    totalPacientes = estado[5][0]
    llevandoContagiados = estado[3]
    llevandoNoContagiados = estado[2]
    energia = estado[4]
    
    heuristica  = 0
    totalPacientesARecoger = len(totalPacientes)
    heuristica += totalPacientesARecoger
    
    return heuristica

def buscarCoste(estado,distancias, posicionFinal):
    for fila in distancias:
            #print("la primer posicion de la fila", fila[0])
            #print("el estado es", estado[0])
            if fila[0] == estado[0]:
                #print("estoy en el if")
                for columna in fila[1]:
                    #print("la columna es",columna)
                    #print("la fila es", fila[1])
                    #print("la columna1",columna[1])
                    #print("la posicion final", posicionFinal)
                    if columna[1] == posicionFinal:
                        #print("estoy en el if")
                        costeCasilla = columna[0]
    #print(costeCasilla)
    return costeCasilla

def expandir(estado, distancias, parking):
    estadoActual = estado[0]
    expandidos = []
    hojadeRuta = estado[5]
    ruta = estado[1]
    rutaContagiados = estado[2]
    #print("cargamos los nodos que vamos a expandir:", expandidos)
    #print("la hoja de ruta es:",hojadeRuta)
    #print("los pacientes recogidos son:", ruta)
    #print("los pacientes contagiados recogidos son:", rutaContagiados)
    if len(ruta) == 10: 
        if len(rutaContagiados) != 0:
            costeCasillaHospitalContagiado = buscarCoste(estado, distancias, hojadeRuta[3][0])
            estadoHospitalContagiado = hojadeRuta[3][0], estado[3],[], estado[3], estado[4] - costeCasillaHospitalContagiado, estado[5], estado[6] + costeCasillaHospitalContagiado, estado[7] + [hojadeRuta[3][0]]
            expandidos.append(estadoHospitalContagiado) #expandimos a hospitalContagiado

            costeCasillaParking = buscarCoste(estado, distancias, hojadeRuta[5][0])
            estadoParking = hojadeRuta[5][0], estado[1],estado[2], estado[3], 50, estado[5], estado[6] + costeCasillaParking, estado[7] + [hojadeRuta[5][0]]
            expandidos.append(estadoParking) #expandimos a parking
        else:
            costeCasillaHospitalNoContagiado = buscarCoste(estado, distancias, hojadeRuta[4][0])
            estadoHospitalNoContagiado = hojadeRuta[4][0], [],[], [], estado[4] - costeCasillaHospitalNoContagiado, estado[5], estado[6] + costeCasillaHospitalNoContagiado, estado[7] + [hojadeRuta[4][0]]
            expandidos.append(estadoHospitalNoContagiado) #expandimos a hospitalNoContagiado

            costeCasillaParking = buscarCoste(estado, distancias, hojadeRuta[5][0])
            estadoParking = hojadeRuta[5][0], estado[1],estado[2], estado[3], 50, estado[5], estado[6] + costeCasillaParking, estado[7] + [hojadeRuta[5][0]]
            expandidos.append(estadoParking) #expandimos a parking
            
    
    else:
        if len(ruta) == 0:
            if estadoActual != list(parking):
                #print("me meto en el caso de que no hay pacientes en el vehiculo")
                for paciente in hojadeRuta[1]:#No contagiados
                    #print("los pacientes no contagiados son:", paciente)
                    #print("la hoja de ruta  es", hojadeRuta[1])
                    costeCasillaPacienteNoContagiado = buscarCoste(estado, distancias, paciente)
                    contador_i = -1
                    CopiaEstado5 = copy.deepcopy(estado[5])
                    for elemento in estado[5]:
                        contador_i += 1
                        contador_j = -1
                        for paso in elemento:
                            contador_j += 1
                            if paso == paciente:
                                del CopiaEstado5[contador_i][contador_j]
                    estadoPacienteNoContagiado = paciente, ruta +[paciente], estado[2], estado[3] + [paciente], estado[4]- costeCasillaPacienteNoContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteNoContagiado, estado[7] + [paciente]
                    #print("el estado que vamos a introducir es:", estadoPacienteNoContagiado)
                    expandidos.append(estadoPacienteNoContagiado)

                for paciente in hojadeRuta[2]:#contagiados
                    costeCasillaPacienteContagiado = buscarCoste(estado, distancias, paciente)
                    contador_i = -1
                    CopiaEstado5 = copy.deepcopy(estado[5])
                    for elemento in estado[5]:
                        contador_i += 1
                        contador_j = -1
                        for paso in elemento:
                            contador_j += 1
                            if paso == paciente:
                                del CopiaEstado5[contador_i][contador_j]
                    estadoPacienteContagiado = paciente, ruta +[paciente], estado[2] + [paciente], estado[3], estado[4]- costeCasillaPacienteContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteContagiado, estado[7] + [paciente]
                    #print("el estado que vamos a introducir es:", estadoPacienteContagiado)
                    expandidos.append(estadoPacienteContagiado)

                costeCasillaParking = buscarCoste(estado, distancias, hojadeRuta[5][0])
                estadoParking = hojadeRuta[5][0], estado[1],estado[2], estado[3], 50, estado[5], estado[6] + costeCasillaParking, estado[7] + [hojadeRuta[5][0]]
                expandidos.append(estadoParking) #expandimos a parking
                #print("salgo de este caso")
                #print("el estado del parking es", estadoParking)
                #print("expandidos",expandidos)
            else:
                #print("me meto en el caso de que no hay pacientes en el vehiculo")
                for paciente in hojadeRuta[1]:#No contagiados
                    #print("los pacientes no contagiados son:", paciente)
                    #print("la hoja de ruta  es", hojadeRuta[1])
                    costeCasillaPacienteNoContagiado = buscarCoste(estado, distancias, paciente)
                    contador_i = -1
                    CopiaEstado5 = copy.deepcopy(estado[5])
                    for elemento in estado[5]:
                        contador_i += 1
                        contador_j = -1
                        for paso in elemento:
                            contador_j += 1
                            if paso == paciente:
                                del CopiaEstado5[contador_i][contador_j]
                    estadoPacienteNoContagiado = paciente, ruta +[paciente], estado[2], estado[3] + [paciente], estado[4]- costeCasillaPacienteNoContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteNoContagiado, estado[7] + [paciente]
                    #print("el estado que vamos a introducir es:", estadoPacienteNoContagiado)
                    expandidos.append(estadoPacienteNoContagiado)

                for paciente in hojadeRuta[2]:#contagiados
                    costeCasillaPacienteContagiado = buscarCoste(estado, distancias, paciente)
                    contador_i = -1
                    CopiaEstado5 = copy.deepcopy(estado[5])
                    for elemento in estado[5]:
                        contador_i += 1
                        contador_j = -1
                        for paso in elemento:
                            contador_j += 1
                            if paso == paciente:
                                del CopiaEstado5[contador_i][contador_j]
                    estadoPacienteContagiado = paciente, ruta +[paciente], estado[2] + [paciente], estado[3], estado[4]- costeCasillaPacienteContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteContagiado, estado[7] + [paciente]
                    #print("el estado que vamos a introducir es:", estadoPacienteContagiado)
                    expandidos.append(estadoPacienteContagiado)

        else:
            if estadoActual != list(parking):
                if len(rutaContagiados) == 0:
                    #print("me meto en el caso de en el que tengo un no contagiado")
                    for paciente in hojadeRuta[1]:#No contagiados
                        costeCasillaPacienteNoContagiado = buscarCoste(estado, distancias, paciente)
                        contador_i = -1
                        CopiaEstado5 = copy.deepcopy(estado[5])
                        #print("estado 5 ",estado[5])
                        for elemento in estado[5]:
                            contador_i += 1
                            contador_j = -1
                            for paso in elemento:
                                contador_j += 1
                                if paso == paciente:
                                    del CopiaEstado5[contador_i][contador_j]
                        #print("estado 5 copiado borrado ",CopiaEstado5)
                        estadoPacienteNoContagiado = paciente, ruta +[paciente], estado[2], estado[3] + [paciente], estado[4]- costeCasillaPacienteNoContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteNoContagiado, estado[7] + [paciente]
                        expandidos.append(estadoPacienteNoContagiado)

                    for paciente in hojadeRuta[2]:#contagiados
                        costeCasillaPacienteContagiado = buscarCoste(estado, distancias, paciente)
                        contador_i = -1
                        CopiaEstado5 = copy.deepcopy(estado[5])
                        #print("estado 5 ",estado[5])
                        for elemento in estado[5]:
                            contador_i += 1
                            contador_j = -1
                            for paso in elemento:
                                contador_j += 1
                                if paso == paciente:
                                    del CopiaEstado5[contador_i][contador_j]
                        #print("estado 5 copiado borrado ",CopiaEstado5)
                        estadoPacienteContagiado = paciente, ruta +[paciente], estado[2] + [paciente], estado[3], estado[4]- costeCasillaPacienteContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteContagiado, estado[7] + [paciente]
                        expandidos.append(estadoPacienteContagiado)

                    costeCasillaHospitalNoContagiado = buscarCoste(estado, distancias, hojadeRuta[4][0])
                    estadoHospitalNoContagiado = hojadeRuta[4][0], [],[], [], estado[4] - costeCasillaHospitalNoContagiado, estado[5], estado[6] + costeCasillaHospitalNoContagiado, estado[7] + [hojadeRuta[4][0]]
                    expandidos.append(estadoHospitalNoContagiado) #expandimos a hospitalNoContagiado

                    costeCasillaParking = buscarCoste(estado, distancias, hojadeRuta[5][0])
                    estadoParking = hojadeRuta[5][0], estado[1],estado[2], estado[3], 50, estado[5], estado[6] + costeCasillaParking, estado[7] + [hojadeRuta[5][0]]
                    expandidos.append(estadoParking) #expandimos a parking
                    #print("salgo del caso en el que tengo pacientes no contagiados")
                    #print("el estado del parking es", estadoParking)
                    #print("expandidos",expandidos)

                if len(rutaContagiados) == 1:
                    for paciente in hojadeRuta[2]:#contagiados
                        costeCasillaPacienteContagiado = buscarCoste(estado, distancias, paciente)
                        contador_i = -1
                        CopiaEstado5 = copy.deepcopy(estado[5])
                        #print("estado 5 ",estado[5])
                        for elemento in estado[5]:
                            contador_i += 1
                            contador_j = -1
                            for paso in elemento:
                                contador_j += 1
                                if paso == paciente:
                                    del CopiaEstado5[contador_i][contador_j]
                        #print("estado 5 copiado borrado ",CopiaEstado5)
                        estadoPacienteContagiado = paciente, ruta +[paciente], estado[2] + [paciente], estado[3], estado[4]- costeCasillaPacienteContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteContagiado, estado[7] + [paciente]
                        expandidos.append(estadoPacienteContagiado)

                    costeCasillaHospitalContagiado = buscarCoste(estado, distancias, hojadeRuta[3][0])
                    estadoHospitalContagiado = hojadeRuta[3][0], estado[3],[], estado[3], estado[4] - costeCasillaHospitalContagiado, estado[5], estado[6] + costeCasillaHospitalContagiado, estado[7] + [hojadeRuta[3][0]]
                    expandidos.append(estadoHospitalContagiado) #expandimos a hospitalContagiado

                    costeCasillaParking = buscarCoste(estado, distancias, hojadeRuta[5][0])
                    estadoParking = hojadeRuta[5][0], estado[1],estado[2], estado[3], 50, estado[5], estado[6] + costeCasillaParking, estado[7] + [hojadeRuta[5][0]]
                    expandidos.append(estadoParking) #expandimos a parking
                
                if len(rutaContagiados) == 2: 
                    costeCasillaHospitalContagiado = buscarCoste(estado, distancias, hojadeRuta[3][0])
                    estadoHospitalContagiado = hojadeRuta[3][0], estado[3],[], estado[3], estado[4] - costeCasillaHospitalContagiado, estado[5], estado[6] + costeCasillaHospitalContagiado, estado[7] + [hojadeRuta[3][0]]
                    expandidos.append(estadoHospitalContagiado) #expandimos a hospitalContagiado

                    costeCasillaParking = buscarCoste(estado, distancias, hojadeRuta[5][0])
                    estadoParking = hojadeRuta[5][0], estado[1],estado[2], estado[3], 50, estado[5], estado[6] + costeCasillaParking, estado[7] + [hojadeRuta[5][0]]
                    expandidos.append(estadoParking) #expandimos a parking
            else:
                if len(rutaContagiados) == 0:
                    #print("me meto en el caso de en el que tengo un no contagiado")
                    for paciente in hojadeRuta[1]:#No contagiados
                        costeCasillaPacienteNoContagiado = buscarCoste(estado, distancias, paciente)
                        contador_i = -1
                        CopiaEstado5 = copy.deepcopy(estado[5])
                        #print("estado 5 ",estado[5])
                        for elemento in estado[5]:
                            contador_i += 1
                            contador_j = -1
                            for paso in elemento:
                                contador_j += 1
                                if paso == paciente:
                                    del CopiaEstado5[contador_i][contador_j]
                        #print("estado 5 copiado borrado ",CopiaEstado5)
                        estadoPacienteNoContagiado = paciente, ruta +[paciente], estado[2], estado[3] + [paciente], estado[4]- costeCasillaPacienteNoContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteNoContagiado, estado[7] + [paciente]
                        expandidos.append(estadoPacienteNoContagiado)

                    for paciente in hojadeRuta[2]:#contagiados
                        costeCasillaPacienteContagiado = buscarCoste(estado, distancias, paciente)
                        contador_i = -1
                        CopiaEstado5 = copy.deepcopy(estado[5])
                        #print("estado 5 ",estado[5])
                        for elemento in estado[5]:
                            contador_i += 1
                            contador_j = -1
                            for paso in elemento:
                                contador_j += 1
                                if paso == paciente:
                                    del CopiaEstado5[contador_i][contador_j]
                        #print("estado 5 copiado borrado ",CopiaEstado5)
                        estadoPacienteContagiado = paciente, ruta +[paciente], estado[2] + [paciente], estado[3], estado[4]- costeCasillaPacienteContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteContagiado, estado[7] + [paciente]
                        expandidos.append(estadoPacienteContagiado)

                    costeCasillaHospitalNoContagiado = buscarCoste(estado, distancias, hojadeRuta[4][0])
                    estadoHospitalNoContagiado = hojadeRuta[4][0], [],[], [], estado[4] - costeCasillaHospitalNoContagiado, estado[5], estado[6] + costeCasillaHospitalNoContagiado, estado[7] + [hojadeRuta[4][0]]
                    expandidos.append(estadoHospitalNoContagiado) #expandimos a hospitalNoContagiado

                if len(rutaContagiados) == 1:
                    for paciente in hojadeRuta[2]:#contagiados
                        costeCasillaPacienteContagiado = buscarCoste(estado, distancias, paciente)
                        contador_i = -1
                        CopiaEstado5 = copy.deepcopy(estado[5])
                        #print("estado 5 ",estado[5])
                        for elemento in estado[5]:
                            contador_i += 1
                            contador_j = -1
                            for paso in elemento:
                                contador_j += 1
                                if paso == paciente:
                                    del CopiaEstado5[contador_i][contador_j]
                        estadoPacienteContagiado = paciente, ruta +[paciente], estado[2] + [paciente], estado[3], estado[4]- costeCasillaPacienteContagiado, CopiaEstado5, estado[6]+ costeCasillaPacienteContagiado, estado[7] + [paciente]
                        expandidos.append(estadoPacienteContagiado)

                    costeCasillaHospitalContagiado = buscarCoste(estado, distancias, hojadeRuta[3][0])
                    estadoHospitalContagiado = hojadeRuta[3][0], estado[3],[], estado[3], estado[4] - costeCasillaHospitalContagiado, estado[5], estado[6] + costeCasillaHospitalContagiado, estado[7] + [hojadeRuta[3][0]]
                    expandidos.append(estadoHospitalContagiado) #expandimos a hospitalContagiado
                
                if len(rutaContagiados) == 2: 
                    costeCasillaHospitalContagiado = buscarCoste(estado, distancias, hojadeRuta[3][0])
                    estadoHospitalContagiado = hojadeRuta[3][0], estado[3],[], estado[3], estado[4] - costeCasillaHospitalContagiado, estado[5], estado[6] + costeCasillaHospitalContagiado, estado[7] + [hojadeRuta[3][0]]
                    expandidos.append(estadoHospitalContagiado) #expandimos a hospitalContagiado

    return expandidos

def A_estrella(datos,parking,distancias, heuristicaUtilizada):
    contador = 0
    abierta = []
    vehiculo = Vehiculo(datos, parking)
    estadoPrimero = [list(vehiculo.posicionActual), vehiculo.pacientesVehiculo, vehiculo.llevandoContagiados, vehiculo.llevandoNoContagiados, vehiculo.energia, vehiculo.hojadeRuta, vehiculo.costeHastaAhora, vehiculo.camino]
    estadoInicial = (0, estadoPrimero)
    abierta.append(estadoInicial)
    estadoActual = estadoPrimero
    while len(abierta) != 0 and (estadoActual[0] != list(parking) or len(estadoActual[1]) != 0 or len(estadoActual[5][0]) != 0): 
        estadoActual = abierta[0][1]
        #print("antes de todo la lista abierta", abierta[0])
        #print("siendo su estado actual",estadoActual[0])
        abierta.remove(abierta[0])
        contador += 1
        vecinos = expandir(estadoActual, distancias, parking)
        for sucesores in vecinos:
            sucesor = list(sucesores)
            if heuristicaUtilizada == 1:
                heuristica = creacionDeHeuristica1(distancias,sucesor)
            else:
                heuristica = creacionDeHeuristica2(distancias,sucesor)
            clave = sucesor[6] + heuristica
            abierta.append((clave, sucesor))
        #print("la lista de expandidos es", abierta[0])
        #print("condicion final",estadoActual[0],len(estadoActual[1]),len(estadoActual[5][0]))
        abierta = sorted(abierta, key=lambda x:x[0])
    return estadoActual[7], contador

def ficheroSalida(pasos, expandidos, dimensiones, datos, tiempo, nombre_stat, nombre_output):
    LongitudDelPlan = len(pasos)
    NodosExpandidos = expandidos
    TiempoTranscurrido = tiempo
    PasosRecorridos = []
    TiposPosicion = []
    PasosEnergia = []
    CosteFinal = 0

    #print("los pasos que recibe", pasos)
    coordenada_i= 0
    coordenada_j =1
    for paso in pasos[:-1]:
        #print(pasos[coordenada_i])
        #print(pasos[coordenada_j])
        caminos = pasosRecorridos(pasos[coordenada_i], pasos[coordenada_j], datos, dimensiones)
        caminos.reverse()
        #print(caminos)
        coordenada_i += 1
        coordenada_j += 1
        for estado in caminos:
            if not PasosRecorridos or PasosRecorridos[-1] != estado:
                PasosRecorridos.append(estado)
    #print(PasosRecorridos)
    for casillas in PasosRecorridos:
        tipo = datos[casillas[0]][casillas[1]]
        TiposPosicion.append(tipo)
    #print(TiposPosicion)
    for costesFinales in TiposPosicion:
        if costesFinales == 'P':
            energia = 50
            PasosEnergia.append(energia)
        else:
            if costesFinales == '2':
                energia = PasosEnergia[-1] -2
                PasosEnergia.append(energia)
            else:
                energia = PasosEnergia[-1] -1
                PasosEnergia.append(energia)
    for costesFinales in TiposPosicion[1:]:
        if costesFinales == '2':
            CosteFinal += 2
        else:
            CosteFinal += 1
    #print(CosteFinal)
    #print(PasosEnergia)
    # Escribir la información en un archivo
    with open(nombre_stat, 'w') as archivo:
        archivo.write(f"Tiempo total: {TiempoTranscurrido}\n")
        archivo.write(f"Coste total: {CosteFinal}\n")
        archivo.write(f"Longitud del plan: {LongitudDelPlan}\n")
        archivo.write(f"Nodos expandidos: {NodosExpandidos}\n")

    # Escribir la información detallada en otro archivo
    with open(nombre_output, 'w') as archivo:
        for paso, tipo, energia in zip(PasosRecorridos, TiposPosicion, PasosEnergia):
            fila = f"{paso}: {tipo}: {energia}\n"
            archivo.write(fila)






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
    #print(datos)
    #print(distanciasMapa)
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
            #print("expandidos", primeroLista, datos, dimensiones)
            expandido = Casilla(primeroLista, datos, dimensiones)
            costeExpandido = distanciasMapa[expandido.posicion[0]][expandido.posicion[1]][0]
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
        #print(posicion)
    #print(solucion)
    aplanada = aplanar_lista(solucion[2])
    coordenadas = juntar(aplanada)
    return coordenadas

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

        #print("el numero es", contador)
    return final

        

#--------------------------main-----------------------------------------------------    
#aqui es donde ejecutaremos el programa
if __name__ == '__main__':
    if len(sys.argv) != 3:
        #print("Uso: python script.py <path_mapa.csv> <num-h>")
        sys.exit(1)
    #lo primero es cargar el csv donde tenemos el mapa de prueba
    nombre_archivo = sys.argv[1]
    heuristicaUtilizada = sys.argv[2]
    #creamos el mapa con ese archivo
    grafo = Mapa(nombre_archivo)
    tiempo_inicio = time.time()
    algoritmo = A_estrella(grafo.datos, grafo.parking, grafo.distancias, heuristicaUtilizada)
    tiempo_fin = time.time()
    tiempo_transcurrido = tiempo_fin - tiempo_inicio
    #print(tiempo_transcurrido)
    #print(algoritmo)
    resultado = ficheroSalida(algoritmo[0],algoritmo[1], grafo.dimensiones, grafo.datos, tiempo_transcurrido, f"{nombre_archivo}-{heuristicaUtilizada}.stat",f"{nombre_archivo}-{heuristicaUtilizada}.output")