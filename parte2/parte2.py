import csv


class Mapa:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo
        self.datos=self.leer_csv()
        self.parking=self.estado_parking()
        self.dimensiones=self.calcular_dimensiones()
        self.filas=self.dimensiones[0]
        self.columnas=self.dimensiones[1]


    def leer_csv(self):
        datos = []

        with open(self.nombre_archivo, 'r') as archivo:
            lector_csv = csv.reader(archivo, delimiter=';')

            for fila in lector_csv:
                datos.append(fila)

        return datos
    
    def estado_parking(self):
        contadorFila=-1
        for fila in self.datos:
            contadorFila+=1
            contadorColumna=-1
            for estado in fila:
                contadorColumna+=1
                if estado=='P':
                    return (contadorFila, contadorColumna) 
    
    def calcular_dimensiones(self):
        contadorFila=-1
        for fila in self.datos:
            contadorFila+=1
            contadorColumna=-1
            for estado in fila:
                contadorColumna+=1
        return (contadorFila, contadorColumna) 
    
class State:
    def __init__ (self, posicion, datos, dimensiones):
        self.posicion=posicion       #lista=[x,y]
        self.datos = datos
        #self.pacientes= pacientes
        self.dimensiones = dimensiones
        self.operadores_disponibles = [self.moverArriba(self.posicion, self.datos), self.moverAbajo(self.posicion, self.datos, self.dimensiones), self.moverDerecha(self.posicion, self.datos, self.dimensiones), self.moverIzquierda(self.posicion, self.datos)]
    
   
    def moverArriba(self, posicion, datos):
        if posicion[0] > 0:
            posicionArriba= [posicion[0]-1, posicion[1]]
            casillaArriba = datos[posicionArriba[0]][posicionArriba[1]]
            if casillaArriba!="X":
                nuevaPosicion = posicionArriba
                return nuevaPosicion
            return None
        return None
    
    def moverAbajo(self, posicion, datos, dimensiones):
        if posicion[0] < dimensiones[0]:
            posicionAbajo= [posicion[0]+1, posicion[1]]
            casillaAbajo = datos[posicionAbajo[0]][posicionAbajo[1]]
            if casillaAbajo!="X":
                nuevaPosicion = posicionAbajo
                return nuevaPosicion
            return None
        return None
    
    def moverDerecha(self, posicion, datos, dimensiones):
        if posicion[1] < dimensiones[1]:
            posicionDerecha= [posicion[0] , posicion[1]+1]
            casillaDerecha = datos[posicionDerecha[0]][posicionDerecha[1]]
            if casillaDerecha!="X":
                nuevaPosicion = posicionDerecha
                return nuevaPosicion
            return None
        return None
    
    def moverIzquierda(self, posicion, datos):
        if posicion[1] > 0:
            posicionIzquierda= [posicion[0] , posicion[1]-1]
            casillaIzquierda = datos[posicionIzquierda[0]][posicionIzquierda[1]]
            if casillaIzquierda!="X":
                nuevaPosicion = posicionIzquierda
                return nuevaPosicion
            return None
        return None

class Vehiculo:
    def __init__(self, datos, posicionActual):
        self.datos = datos
        self.posicionActual= posicionActual
        self.pacientesVehiculo=[] #inicilamente no hay pacientes
        self.energia = 50 #al principio tiene 50 
        self.hojadeRuta= self.pacientesRecoger(self.datos)
    
    def pacientesRecoger(self, datos):
        noContagiados= []
        contagiados=[]
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
        totalPacientes=noContagiados+contagiados
        pacientesNoContagiados=len(noContagiados)
        pacientesContagiados=len(contagiados)
        numeroTotal=pacientesContagiados+pacientesNoContagiados

        return pacientesContagiados, pacientesNoContagiados, numeroTotal, totalPacientes, noContagiados, contagiados


#--------------------------funciones-----------------------------------------------------    
def distanciaMinima(datos, dimensiones, inicio):
    print(dimensiones)
    distanciasMapa=[]
    for fila in datos:
        distancias = [100] * (dimensiones[1]+1)
        distanciasMapa.append(distancias)
    abierta = [(0, inicio)] 
    distanciasMapa[inicio[0]][inicio[1]] =0
    cerrada=[]   
    while len(abierta) !=0:
        contador =0
        primeroLista= abierta[0][1]
        for estado in cerrada:
            if primeroLista == estado[1]:
                contador+=1
        if contador ==0:          
            expandido =State(primeroLista, datos, dimensiones)
            costeExpandido = distanciasMapa[expandido.posicion[0]][expandido.posicion[1]]
            vecinos = expandido.operadores_disponibles
            cerrada.append(abierta[0])
            abierta.remove(abierta[0]) 
            for estado in vecinos:
                if estado!=None:
                    tipo = datos[estado[0]][estado[1]]
                    if tipo=="2":
                        coste=2
                    else:
                        coste=1
                    coste_actual= distanciasMapa[estado[0]][estado[1]]
                    costeAcumulado = costeExpandido+coste #actualizar coste total
                    if costeAcumulado < coste_actual:
                        distanciasMapa[estado[0]][estado[1]] = costeAcumulado
                        abierta.append((costeAcumulado, estado))
                    else:
                        abierta.append((coste_actual, estado))
        else:
            abierta.remove(abierta[0])   

        abierta = sorted(abierta, key = lambda tupla:tupla[0])
        print(distanciasMapa)
        print("lista abierta", abierta)
        print("lista cerrada", cerrada)

            



            

    


#--------------------------main-----------------------------------------------------    

        
if __name__ == '__main__':
    nombre_archivo = 'entrada.csv'
    grafo = Mapa(nombre_archivo)
    vehiculo = Vehiculo (grafo.datos, grafo.parking)
    estado=State(grafo.parking,  grafo.datos, grafo.dimensiones)
    recoger= vehiculo.hojadeRuta
    camino = distanciaMinima(grafo.datos, grafo.dimensiones, grafo.parking)





