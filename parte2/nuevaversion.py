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
        return totalPacientes, noContagiados, contagiados, hospitalContagiado, hospitalNoContagiado, parking


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
    return valorMasPequeño

def lugarMasCercano(cerrada, Nocontagiados, Contagiados, hospitalContagiado, hospitalNoContagiado):
    #función que determina cual es el paciente más cercano a la posición actual y determina la distancia al parking
    valorContagiados = recorrerListas(Contagiados, cerrada)
    valorNoContagiados = recorrerListas(Nocontagiados, cerrada)
    valorHospitalContagiados = recorrerListas(hospitalContagiado, cerrada)
    valorHospitalNoContagiados = recorrerListas(hospitalNoContagiado, cerrada)

    return  valorNoContagiados, valorContagiados, valorHospitalContagiados, valorHospitalNoContagiados
    
    
def A_estrella(datos, parking, dimensiones):
    vehiculo = Vehiculo(datos, parking)
    hojaRuta = vehiculo.hojadeRuta
    ruta = vehiculo.pacientesVehiculo 
    rutaContagiados = vehiculo.llevandoContagiados
    rutaNoContagiados = vehiculo.llevandoNoContagiados
    coste_total = 0

    while len(hojaRuta[0]) != 0 or vehiculo.posicionActual != list(parking) or len(rutaContagiados) != 0 or len(rutaNoContagiados) != 0:
        camino = distanciaMinima(datos, dimensiones, vehiculo.posicionActual)
        cercano = lugarMasCercano(camino, hojaRuta[1], hojaRuta[2], hojaRuta[3], hojaRuta[4])

        #para el  caso en el que ya no hay más pacientes No contagiados a recoger
        if cercano[0] != 0: #si ya no hay más que recoger, no devolverá una tupla, si no un 0, indicando que ya no quedan más pacientes a recoger
            pacienteNoContagiado = cercano[0][0] #esto lo iremos modificando para que se vayan actualizando los pesos
            posicionPacienteNoContagiado = cercano[0][1]
            costeRealPacienteNoContagiado = cercano[0][0] #pero este lo utilizaremos para sumar el coste total real
        else: 
            pacienteNoContagiado = 10000
            posicionPacienteNoContagiado = parking
            costeRealPacienteNoContagiado = 10000

        if cercano[1] != 0:
            pacienteContagiado = cercano[1][0]
            posicionPacienteContagiado = cercano[1][1]
            costeRealPacienteContagiado = cercano[1][0]
        else:
            pacienteContagiado = 10000
            posicionPacienteContagiado = parking
            costeRealPacienteContagiado = 10000

        hospitalContagiado = cercano[2][0]
        costeRealHospitalContagiado = cercano[2][0]
        posicionHospitalContagiado = cercano[2][1]
        hospitalNoContagiado = cercano [3][0]
        costeRealHospitalNoContagiado = cercano[3][0]
        posicionHospitalNoContagiado = cercano[3][1]
        distanciaActual = distanciaMinima(datos, dimensiones, vehiculo.posicionActual)
        costeRealAlParking = 0
        distanciaparking = costeRealAlParking
        posicionParking = list(parking)
        for elemento in distanciaActual:
            if elemento[1][0] == parking[0] and elemento[1][1] == parking[1]:
                costeRealAlParking = elemento[0]
        #hasta aqui, se inicializan las 5 nodos que va a extender

        #heurística de que no coja la opción del parking si tiene mucha energía
        distanciaparking += vehiculo.energia

        #en el caso de que lleve a contagiados no podrá coger más NoContagiados y no podrá ir al hospital de NoContagiados
        if len(rutaContagiados) != 0:
            if len(rutaContagiados) == 1:
                pacienteNoContagiado += 1000
                hospitalNoContagiado += 1000
            elif len(rutaContagiados) == 2:
                pacienteNoContagiado += 1000
                hospitalNoContagiado += 1000
                pacienteContagiado += 1000 #en el caso de que ya tenga dos, no puede coger a más

        #en el caso de que el vehiculo esté lleno, no se pueden recoger más pacientes
        if len(ruta) == 10:
            pacienteContagiado += 1000
            pacienteNoContagiado+= 1000
        
        #caso en el que no hay más pacientes que recoger
        if len(hojaRuta[0]) == 0:
            if len(ruta) == 0: #caso en el que solo quede volver al parking
                pacienteContagiado += 1000
                pacienteNoContagiado += 1000
                hospitalContagiado += 1000
                hospitalNoContagiado += 1000
            else: #tiene que dejar a los pacientes en los hospitales 
                if len(rutaContagiados) == 0: #caso en el que tiene que dejar solo a pacientes no contagiados
                    pacienteContagiado += 1000
                    pacienteNoContagiado += 1000
                    hospitalContagiado += 1000
                else: #caso en el que tiene que dejar a pacientes contagiados
                    pacienteNoContagiado += 1000
                    hospitalNoContagiado += 1000
                    pacienteContagiado += 1000
        
        #caso en el que no tiene a pacientes de X tipo en el vehiculo, no puedo ir a ese hospital
        if len(rutaNoContagiados) == 0: #Si no hay pacientes no contagiados
            hospitalNoContagiado += 1000
        
        if len(rutaContagiados) == 0: #Si no hay pacientes Contagiados
            hospitalContagiado += 1000

        #comprobar que tras ir al proximo estado, me quede energía para volver
        #en el primer caso, se mira cuánto costará ir al parking a recargar desde esl paciente No contagioso, y si no le da la energia para volver, no podrá ir a por ese paciente
        expandirPacienteNoContagiado= distanciaMinima(datos, dimensiones, posicionPacienteNoContagiado)
        for elemento in expandirPacienteNoContagiado:
            if elemento[1] == posicionParking:
                distanciaSeguridadPacienteNoContagiado = elemento[0]
        costeFuturoPacienteNoContagiado = vehiculo.energia - distanciaSeguridadPacienteNoContagiado
        if costeFuturoPacienteNoContagiado < pacienteNoContagiado:
            pacienteNoContagiado += 1000

        #segundo caso, para el pacienteContagiado
        expandirPacienteContagiado= distanciaMinima(datos, dimensiones, posicionPacienteContagiado)
        for elemento in expandirPacienteContagiado:
            if elemento[1] == posicionParking:
                distanciaSeguridadPacienteContagiado = elemento[0]
        costeFuturoPacienteContagiado = vehiculo.energia - distanciaSeguridadPacienteContagiado
        if costeFuturoPacienteContagiado < pacienteContagiado:
            pacienteContagiado += 1000

        #tercer caso, para el hospital de No contagiados
        expandirHospitalNoContagiado= distanciaMinima(datos, dimensiones, posicionHospitalNoContagiado)
        for elemento in expandirHospitalNoContagiado:
            if elemento[1] == posicionParking:
                distanciaSeguridadHospitalNoContagiado = elemento[0]
        costeFuturoHospitalNoContagiado = vehiculo.energia - distanciaSeguridadHospitalNoContagiado
        if costeFuturoHospitalNoContagiado < hospitalNoContagiado:
            hospitalNoContagiado += 1000

        #cuarto caso, para el hospital de contagiados 
        expandirHospitalContagiado= distanciaMinima(datos, dimensiones, posicionHospitalContagiado)
        for elemento in expandirHospitalContagiado:
            if elemento[1] == posicionParking:
                distanciaSeguridadHospitalContagiado = elemento[0]
        costeFuturoHospitalContagiado = vehiculo.energia - distanciaSeguridadHospitalContagiado
        if costeFuturoHospitalContagiado < hospitalContagiado:
            hospitalContagiado += 1000

        #restricción para que si quedan pocos pacientes a recoger, los recoja, y luego vaya al hospital
        RecogidosNoContagiados = len(rutaNoContagiados)
        print("ha recogido PacientesNoCOntagiados",RecogidosNoContagiados)

        #comprobación de si recoger a otro paciente le pilla de paso al hospital o no
        #los pongo en la comprobación de arriba
        #expandirPacienteNoContagiado= distanciaMinima(datos, dimensiones, cercano[0][1])
        #expandirPacienteContagiado= distanciaMinima(datos, dimensiones, cercano[0][1])
        distanciaHospitalContagiado = 0
        for elemento in expandirPacienteContagiado:
            if elemento[1][0] == cercano[2][1][0] and elemento[1][1] == cercano[2][1][1]:
                distanciaHospitalContagiado = elemento[0]
        #print(distanciaHospitalContagiado)
        distanciaHospitalNoContagiado = 0
        for elemento in expandirPacienteNoContagiado:
            if elemento[1][0] == cercano[3][1][0] and elemento[1][1] == cercano[3][1][1]:
                distanciaHospitalNoContagiado = elemento[0]
        #print(distanciaHospitalNoContagiado)
        
        if len(rutaContagiados) == 0:
            if distanciaHospitalNoContagiado >= hospitalNoContagiado:
                pacientesEnVehiculo = len(ruta)
                pacienteNoContagiado += pacientesEnVehiculo
        else: 
            if distanciaHospitalContagiado >= hospitalNoContagiado:
                pacientesEnVehiculo = len(ruta)
                pacienteNoContagiado += pacientesEnVehiculo



        print("valor de ir a otra paciente N",pacienteNoContagiado)
        print("valor de ir a otro paciente C",pacienteContagiado)
        print("valor de ir al hospital Contagiado",hospitalContagiado)
        print("valor de ir al hospital No contagiado",hospitalNoContagiado)
        print("distancia al parking",distanciaparking)
        print("el coste real de ir al paciente N es:", costeRealPacienteNoContagiado)
        print("el coste real de ir al paciente C es:", costeRealPacienteContagiado)
        print("el coste real de ir al hospital CN es:", costeRealHospitalNoContagiado)
        print("el coste real de ir al hospital CC es:", costeRealHospitalContagiado)
        print("el coste real de ir al parking es:", costeRealAlParking)                  

        #en el caso de que opte por coger el paciente No contagiado, al declararse primero que lo contagiados, se le prioridad 
        if (pacienteNoContagiado <= min(pacienteContagiado, hospitalContagiado, hospitalNoContagiado, distanciaparking)):
                vehiculo.energia -= pacienteNoContagiado #le resta a la energía lo que le cuesta ir hasta ella
                coste_total += costeRealPacienteNoContagiado #y se lo suma a contador global
                vehiculo.posicionActual = posicionPacienteNoContagiado #el vehiculo se moverá a esa posición
                hojaRuta[0].remove(posicionPacienteNoContagiado) #ya hemos pasado por el, asi que no tendremos que buscarlo más veces en la hojaRuta general
                hojaRuta[1].remove(posicionPacienteNoContagiado) #tampoco en la hoja de ruta de los pacientes No contagiados
                rutaNoContagiados.append(posicionPacienteNoContagiado) #entrará en el vehiculo, en la lista de pacientes No contagiados
                ruta.append(vehiculo.posicionActual) #entra en el vehiculo

        elif (pacienteContagiado <= min(pacienteNoContagiado, hospitalContagiado, hospitalNoContagiado, distanciaparking)):
                vehiculo.energia -= pacienteContagiado #le resta a la energía lo que le cuesta ir hasta ella
                coste_total += costeRealPacienteContagiado #y se lo suma a contador global
                vehiculo.posicionActual = posicionPacienteContagiado #el vehiculo se moverá a esa posición
                hojaRuta[0].remove(posicionPacienteContagiado) #ya hemos pasado por el, asi que no tendremos que buscarlo más veces en la hojaRuta general
                hojaRuta[2].remove(posicionPacienteContagiado) #tampoco en la hoja de ruta de los pacientes contagiados
                rutaContagiados.append(posicionPacienteContagiado) #entrará en el vehiculo, en la lista de pacientes contagiados
                ruta.append(vehiculo.posicionActual) #entra en el vehiculo
        
        elif (hospitalContagiado <= min(pacienteNoContagiado, pacienteContagiado, hospitalNoContagiado, distanciaparking)):
                vehiculo.energia -= hospitalContagiado
                coste_total += costeRealHospitalContagiado
                for pasajeros in ruta:
                    if pasajeros in rutaContagiados:
                        ruta.remove(pasajeros)
                rutaContagiados.clear()
                vehiculo.posicionActual = posicionHospitalContagiado

        elif (hospitalNoContagiado <= min(pacienteNoContagiado, hospitalContagiado, pacienteContagiado, distanciaparking)):
                vehiculo.energia -= hospitalNoContagiado
                coste_total += costeRealHospitalNoContagiado
                rutaNoContagiados.clear()
                ruta.clear()
                vehiculo.posicionActual = posicionHospitalNoContagiado

        elif (distanciaparking <= min(pacienteNoContagiado, hospitalContagiado, hospitalNoContagiado, pacienteContagiado)):
                vehiculo.energia = 50
                coste_total += costeRealAlParking
                vehiculo.posicionActual = posicionParking

        
        print(posicionPacienteNoContagiado)
        print(posicionPacienteContagiado)
        print(posicionHospitalContagiado)
        print(posicionHospitalNoContagiado)
        print(posicionParking)
        print("el coste total es", coste_total)


        print("lleva a :",ruta)  
        print("lleva no contagiados:",rutaNoContagiados)
        print("lleva contagiados:",rutaContagiados)
        print("la energia que queda es.",vehiculo.energia) 
        print("me voy a mover a", vehiculo.posicionActual)
        print("quedan por recoger", hojaRuta[0])




                    
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