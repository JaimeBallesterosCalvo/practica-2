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
    
class State:
    #se crea la clase estado
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
        self.hojadeRuta= self.pacientesRecoger(self.datos) #la hoja de ruta indica que pacientes le faltan por recoger 
    
    def pacientesRecoger(self, datos):
        #la función recorrera el mapa, guardando la dirección de donde están cada paciente y los hospitales
        noContagiados= []
        contagiados=[]
        hospitalContagiado = []
        hospitalNoContagiado = []
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
        totalPacientes=noContagiados+contagiados 
        return totalPacientes, noContagiados, contagiados, hospitalContagiado, hospitalNoContagiado


#--------------------------funciones-----------------------------------------------------    
#desarrollo de las funciones que iremos utilizando

def distanciaMinima(datos, dimensiones, inicio):
    #se calcula la distancia minima que hay desde la posición pasada por parámetros, hasta todas las casillas del mapa
    distanciasMapa=[]
    #se creará una lista de listas del tamaño del mapa, pero en vez de guardar la posición, poserá el coste que se tarda en llegar a él
    for fila in datos:
        distancias = [100] * (dimensiones[1]+1)
        distanciasMapa.append(distancias)

    abierta = [(0, inicio)] 
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
            expandido =State(primeroLista, datos, dimensiones)
            costeExpandido = distanciasMapa[expandido.posicion[0]][expandido.posicion[1]]
            vecinos = expandido.operadores_disponibles
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
        abierta = sorted(abierta, key = lambda tupla:tupla[0])

        #print(distanciasMapa)
        #print("lista abierta", abierta)
        #print("lista cerrada", cerrada) 
    return cerrada #devolviendo una lista de tuplas en la que el primer elemento de la tupla es el coste que se necesita para ir a la posición y el segundo, la posición a la que se iría por ese coste


def recorrerListas(listaAComprobar, listaCerrada):
    #función auxiliar que recorrará la lista donde solo se tenga la posición para obtener cuánto es el movimiento menos costoso y a que posición es
    valorNumerico = 100
    valorMasPequeño = 0
    for paciente in listaAComprobar:
        for elemento in listaCerrada:
            if paciente == elemento[1]:
                distanciaListaAComprobar = elemento[0]
                if distanciaListaAComprobar < valorNumerico:
                    valorNumerico = distanciaListaAComprobar
                    valorMasPequeño = elemento
    return valorNumerico, valorMasPequeño

def lugarMasCercano(cerrada, Nocontagiados, Contagiados, hospitalContagiado, hospitalNoContagiado):
    #función que determina cual es el paciente más cercano a la posición actual y determina la distancia al parking
    valorNumericoContagiados, valorContagiados = recorrerListas(Contagiados, cerrada)
    valorNumericoNoContagiados, valorNoContagiados = recorrerListas(Nocontagiados, cerrada)
    valorNumericoHospitalContagiados, valorHospitalContagiados = recorrerListas(hospitalContagiado, cerrada)
    valorNumericoHospitalNoContagiados, valorHospitalNoContagiados = recorrerListas(hospitalNoContagiado, cerrada)

    #dependiendo de si el paciente más cercano es contagiado o no, se devolverá primero uno u otro
    #en caso de empate, se da preferencia a los pacientes NoContagiados
    if valorNumericoContagiados  < valorNumericoNoContagiados:
        return valorContagiados, valorNoContagiados, valorHospitalContagiados, valorHospitalNoContagiados
    if valorNumericoContagiados  >= valorNumericoNoContagiados:
        return  valorNoContagiados, valorContagiados, valorHospitalContagiados, valorHospitalNoContagiados
    
    
def A_estrella(datos, parking, dimensiones):
    vehiculo = Vehiculo(datos, parking)
    hojaRuta = vehiculo.hojadeRuta
    ruta = vehiculo.pacientesVehiculo 
    rutaContagiados = vehiculo.llevandoContagiados
    rutaNoContagiados = vehiculo.llevandoNoContagiados
    coste_total = 0

    while len(hojaRuta[0]) != 0 or vehiculo.posicionActual != parking:
        print(coste_total)
        if len(hojaRuta[0]) != 0:
            camino = distanciaMinima(datos, dimensiones, vehiculo.posicionActual)
            cercano = lugarMasCercano(camino, hojaRuta[1], hojaRuta[2], hojaRuta[3], hojaRuta[4])
            #print(camino)
            #print(cercano)
            #print("lista de pacientes:",hojaRuta[0])
            #print("lista de los pacientes No Contagiados",hojaRuta[1])
            #print("lista de los pacientes Contagiados",hojaRuta[2])
            if len(ruta) ==10:
                if len(rutaContagiados) == 0:
                    if vehiculo.posicionActual != parking:
                        hospital = hojaRuta[4] 
                        costeHospital = cercano[3][0]
                        nuevoEstado = hospital[0]
                        distanciaSeguridad = distanciaMinima(datos, dimensiones, nuevoEstado)
                        costeVolverDelHospitalNoContagiados = 0
                        for elemento in distanciaSeguridad:
                            if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                                costeVolverDelHospitalNoContagiados = elemento[0]
                        costeFuturo = vehiculo.energia - cercano[3][0] 
                        if costeVolverDelHospitalNoContagiados <= costeFuturo:
                            vehiculo.energia -= costeHospital
                            coste_total += costeHospital
                            rutaNoContagiados.clear()
                            ruta.clear()
                            vehiculo.posicionActual = nuevoEstado
                            print("el coste al hospital:",cercano[3][0])
                            print("el coste futuro es.",costeFuturo)
                            print("el coste de volver es.",costeVolverDelHospitalNoContagiados)
                        else:
                            vehiculo.energia = 50
                            coste_total += costeVolverDelHospitalNoContagiados
                            vehiculo.posicionActual = parking
                            print("el coste al cercano:",cercano[3][0])
                            print("el coste futuro es.",costeFuturo)
                            print("el coste de volver es.",costeVolverDelHospitalNoContagiados)
                    else:
                        hospital = hojaRuta[4] 
                        costeHospital = cercano[3][0]
                        nuevoEstado = hospital[0]
                        vehiculo.energia -= costeHospital
                        coste_total += costeHospital
                        rutaNoContagiados.clear()
                        ruta.clear()
                        vehiculo.posicionActual = nuevoEstado
                        print("el coste al hospital:",cercano[3][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)

                else:
                    if vehiculo.posicionActual != parking:
                        hospital = hojaRuta[3] 
                        costeHospital = cercano[2][0]
                        nuevoEstado = hospital[0]
                        distanciaSeguridad = distanciaMinima(datos, dimensiones, nuevoEstado)
                        costeVolver1 = 0
                        for elemento in distanciaSeguridad:
                            if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                                costeVolver1 = elemento[0]
                        costeFuturo = vehiculo.energia - cercano[2][0] 
                        if costeVolver1 <= costeFuturo:
                            vehiculo.energia -= costeHospital
                            coste_total += costeHospital
                            for pasajeros in ruta:
                                if pasajeros in rutaContagiados:
                                    ruta.remove(pasajeros)
                            rutaContagiados.clear()
                            vehiculo.posicionActual = nuevoEstado
                            print("el coste al hospital:",cercano[2][0])
                            print("el coste futuro es.",costeFuturo)
                            print("el coste de volver es.",costeVolver1)
                        else:
                            vehiculo.energia = 50
                            coste_total += costeVolver1
                            vehiculo.posicionActual = parking
                            print("el coste al hospital:",cercano[2][0])
                            print("el coste futuro es.",costeFuturo)
                            print("el coste de volver es.",costeVolver1)
                    else:
                        hospital = hojaRuta[3] 
                        costeHospital = cercano[2][0]
                        nuevoEstado = hospital[0]
                        vehiculo.energia -= costeHospital
                        coste_total += costeHospital
                        for pasajeros in ruta:
                            if pasajeros in rutaContagiados:
                                ruta.remove(pasajeros)
                        rutaContagiados.clear()
                        vehiculo.posicionActual = nuevoEstado
                        print("el coste al hospital:",cercano[2][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)

                
            else:
                if len(rutaContagiados) == 0:
                    nuevoEstado = cercano[0][1]
                    distanciaSeguridad = distanciaMinima(datos, dimensiones, nuevoEstado)
                    costeVolver1 = 0
                    for elemento in distanciaSeguridad:
                        if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                            costeVolver1 = elemento[0]
                    costeFuturo = vehiculo.energia - cercano[0][0] 
                    if costeVolver1 <= costeFuturo:
                        print("el coste al cercano:",cercano[0][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)
                        if datos[nuevoEstado[0]][nuevoEstado[1]] == "N":
                            hojaRuta[0].remove(nuevoEstado)
                            hojaRuta[1].remove(nuevoEstado)
                            rutaNoContagiados.append(nuevoEstado)
                        elif datos[nuevoEstado[0]][nuevoEstado[1]] == "C":
                            hojaRuta[0].remove(nuevoEstado)
                            hojaRuta[2].remove(nuevoEstado)
                            rutaContagiados.append(nuevoEstado)
                        vehiculo.energia -= cercano[0][0]
                        coste_total += cercano[0][0]
                        vehiculo.posicionActual = nuevoEstado
                        ruta.append(vehiculo.posicionActual)
                    else:
                        print("el coste al cercano:",cercano[0][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)
                        vehiculo.energia = 50
                        coste_total += costeVolver1
                        vehiculo.posicionActual = parking

                elif len(rutaContagiados) == 1:
                    contagiadosCercanos = []
                    for enfermos in hojaRuta[2]:
                        for elemento in cercano:
                            if enfermos == elemento[1]:
                                contagiadosCercanos.append(elemento)
                    if len(contagiadosCercanos) != 0:
                        contagiadoMasCercano = contagiadosCercanos[0]
                        costeHospitalC = cercano[2][0]
                        if costeHospitalC < contagiadoMasCercano[0]:
                            nuevoEstado = cercano[2][1]
                            distanciaSeguridad = distanciaMinima(datos, dimensiones, nuevoEstado)
                            costeVolver1 = 0
                            for elemento in distanciaSeguridad:
                                if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                                    costeVolver1 = elemento[0]
                            costeFuturo = vehiculo.energia - cercano[2][0] 
                            if costeVolver1 <= costeFuturo:
                                vehiculo.posicionActual = nuevoEstado
                                vehiculo.energia -= costeHospital
                                coste_total += costeHospital
                                print("el coste al cercano:",cercano[2][0])
                                print("el coste futuro es.",costeFuturo)
                                print("el coste de volver es.",costeVolver1)

                            else:
                                vehiculo.energia = 50
                                coste_total += costeVolver1
                                vehiculo.posicionActual = parking
                                print("el coste al cercano:",cercano[0][0])
                                print("el coste futuro es.",costeFuturo)
                                print("el coste de volver es.",costeVolver1)
                        else:
                            nuevoEstado = contagiadoMasCercano[1]
                            distanciaSeguridad = distanciaMinima(datos, dimensiones, nuevoEstado)
                            costeVolver1 = 0
                            for elemento in distanciaSeguridad:
                                if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                                    costeVolver1 = elemento[0]
                            costeFuturo = vehiculo.energia - contagiadoMasCercano[0] 
                            if costeVolver1 <= costeFuturo:
                                hojaRuta[0].remove(nuevoEstado)
                                hojaRuta[2].remove(nuevoEstado)
                                rutaContagiados.append(nuevoEstado)
                                vehiculo.posicionActual = nuevoEstado
                                ruta.append(vehiculo.posicionActual)
                                vehiculo.energia -= contagiadoMasCercano[0]
                                coste_total += costeVolver1
                                print("el coste al cercano:",contagiadoMasCercano[0])
                                print("el coste futuro es.",costeFuturo)
                                print("el coste de volver es.",costeVolver1)
                            else:
                                vehiculo.energia = 50
                                coste_total += costeVolver1
                                vehiculo.posicionActual = parking
                                print("el coste al cercano:",contagiadoMasCercano[0])
                                print("el coste futuro es.",costeFuturo)
                                print("el coste de volver es.",costeVolver1)
                    else: 
                        hospital = hojaRuta[3] 
                        costeHospital = cercano[2][0]
                        nuevoEstado = hospital[0]
                        distanciaSeguridad = distanciaMinima(datos, dimensiones, nuevoEstado)
                        costeVolver1 = 0
                        for elemento in distanciaSeguridad:
                            if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                                costeVolver1 = elemento[0]
                        costeFuturo = vehiculo.energia - cercano[2][0] 
                        if costeVolver1 <= costeFuturo:
                            vehiculo.energia -= costeHospital
                            coste_total += costeHospital
                            for pasajeros in ruta:
                                if pasajeros in rutaContagiados:
                                    ruta.remove(pasajeros)
                            rutaContagiados.clear()
                            vehiculo.posicionActual = nuevoEstado
                            print("el coste al hospital:",cercano[2][0])
                            print("el coste futuro es.",costeFuturo)
                            print("el coste de volver es.",costeVolver1)
                        else:
                            vehiculo.energia = 50
                            coste_total += costeVolver1
                            vehiculo.posicionActual = parking 
                            print("el coste al hospital:",cercano[2][0])
                            print("el coste futuro es.",costeFuturo)
                            print("el coste de volver es.",costeVolver1)
                    
                else: 
                    hospital = hojaRuta[3] 
                    costeHospital = cercano[2][0]
                    nuevoEstado = hospital[0]
                    distanciaSeguridad = distanciaMinima(datos, dimensiones, nuevoEstado)
                    costeVolver1 = 0
                    for elemento in distanciaSeguridad:
                        if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                            costeVolver1 = elemento[0]
                    costeFuturo = vehiculo.energia - cercano[2][0] 
                    if costeVolver1 <= costeFuturo:
                        vehiculo.energia -= costeHospital
                        coste_total += costeHospital
                        for pasajeros in ruta:
                            if pasajeros in rutaContagiados:
                                ruta.remove(pasajeros)
                        rutaContagiados.clear()
                        vehiculo.posicionActual = nuevoEstado
                        print("el coste al hospital:",cercano[2][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)
                    else:
                        vehiculo.energia = 50
                        coste_total += costeVolver1
                        vehiculo.posicionActual = parking 
                        print("el coste al hospital:",cercano[2][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)

            print("lleva a :",ruta)  
            print("lleva no contagiados:",rutaNoContagiados)
            print("lleva contagiados:",rutaContagiados)
            print("la energia que queda es.",vehiculo.energia) 
        
        else:
            if len(ruta) == 0:
                camino = distanciaMinima(datos, dimensiones, vehiculo.posicionActual)
                costeVolver1 = 0
                for elemento in camino:
                    if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                        costeVolver1 = elemento[0]
                vehiculo.energia -= costeVolver1
                vehiculo.posicionActual = parking
                print(costeVolver1)
                print("la energia que queda es.",vehiculo.energia)
            else:
                if len(rutaContagiados) == 0:
                    hospital = hojaRuta[4] 
                    costeHospital = cercano[3][0]
                    nuevoEstado = hospital[0]
                    distanciaSeguridad = distanciaMinima(datos, dimensiones, nuevoEstado)
                    costeVolver1 = 0
                    for elemento in distanciaSeguridad:
                        if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                            costeVolver1 = elemento[0]
                    costeFuturo = vehiculo.energia - cercano[3][0] 
                    if costeVolver1 <= costeFuturo:
                        vehiculo.energia -= costeHospital
                        rutaNoContagiados.clear()
                        ruta.clear()
                        vehiculo.posicionActual = nuevoEstado
                        print("el coste al hospital:",cercano[3][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)
                    else:
                        vehiculo.energia = 50
                        coste_total += costeVolver1
                        vehiculo.posicionActual = parking
                        print("el coste al hospital:",cercano[3][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)
                else:
                    hospital = hojaRuta[3] 
                    costeHospital = cercano[2][0]
                    nuevoEstado = hospital[0]
                    distanciaSeguridad = distanciaMinima(datos, dimensiones, nuevoEstado)
                    costeVolver1 = 0
                    for elemento in distanciaSeguridad:
                        if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                            costeVolver1 = elemento[0]
                    costeFuturo = vehiculo.energia - cercano[2][0] 
                    if costeVolver1 <= costeFuturo:
                        vehiculo.energia -= costeHospital
                        for pasajeros in ruta:
                            if pasajeros in rutaContagiados:
                                ruta.remove(pasajeros)
                        rutaContagiados.clear()
                        vehiculo.posicionActual = nuevoEstado
                        print("el coste al hospital:",cercano[2][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)
                    else:
                        vehiculo.energia = 50
                        coste_total += costeVolver1
                        vehiculo.posicionActual = parking
                        print("el coste al hospital:",cercano[2][0])
                        print("el coste futuro es.",costeFuturo)
                        print("el coste de volver es.",costeVolver1)

                print("la energia que queda es.",vehiculo.energia)
    return coste_total

                    


        

    


#--------------------------main-----------------------------------------------------    
#aqui es donde ejecutaremos el programa
if __name__ == '__main__':
    #lo primero es cargar el csv donde tenemos el mapa de prueba
    nombre_archivo = 'parte2/entrada.csv'
    #creamos el mapa con ese archivo
    grafo = Mapa(nombre_archivo)
    #realizamos la búsqueda con los datos del ejemplo cargado
    algoritmo = A_estrella(grafo.datos, grafo.parking, grafo.dimensiones)
    print(algoritmo)


