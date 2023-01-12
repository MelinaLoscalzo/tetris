import random


#CONSTANTES
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1

nombres = ["Cubo","Z","S","I","L","-L","T"]

#FIN DE CONSTANTES

def generar_pieza(piezas,pieza=None):
       
    if pieza == None or pieza not in nombres:
        pieza_al_azar = random.choice(nombres) #La intruccion random.choice elige una pieza al azar.
        return piezas[pieza_al_azar][0]
    else:
        return piezas[pieza][0]




def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    nueva_pieza = []
    for bloque in pieza:
        nueva_pieza.append((bloque[0]+dx,bloque[1]+dy))
    return tuple(nueva_pieza)
     

def crear_tablero():
    tablero = [] 

    for i in range(ALTO_JUEGO): 
        tablero.append(["0"]*ANCHO_JUEGO)  
    
    return tablero

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """

    tablero = crear_tablero()
    pieza_inicial = trasladar_pieza(pieza_inicial,ANCHO_JUEGO // 2,0)

    for posicion in pieza_inicial:
            tablero[posicion[1]][posicion[0]] = "+"

    return tablero

def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return (ANCHO_JUEGO,ALTO_JUEGO)

def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    pieza = []

    for columna in range(ALTO_JUEGO):
        for fila in range(ANCHO_JUEGO):
            if juego[columna][fila] == "+":
                pieza.append((fila,columna))
    
    return tuple(pieza)

def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    if juego[y][x] != "#":
        return False    
    return True

def descender(juego):
    se_puede_bajar = True

    pieza = pieza_actual(juego)
    pieza_movida = trasladar_pieza(pieza,0,1)

    for x,y in pieza_movida:
        if (x > ANCHO_JUEGO-1 or x < 0 or y > ALTO_JUEGO-1 or y < 0) or hay_superficie(juego,x,y):
            se_puede_bajar = False
    
    if se_puede_bajar:
        borrar_pieza_actual(juego)
        dibujar_pieza(juego,pieza_movida)
    
    return juego


def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    se_puede = True
    

    pieza = pieza_actual(juego)
    pieza_movida = trasladar_pieza(pieza,direccion,0)
         

    for x,y in pieza_movida:   
        if (x > ANCHO_JUEGO-1 or x < 0) or hay_superficie(juego,x,y):     #Chequeo que el movimiento es valido.
            se_puede = False

    if se_puede:
        borrar_pieza_actual(juego)
        dibujar_pieza(juego,pieza_movida)        


    return juego 

def buscar_rotaciones(pieza,rotaciones):
    for key,value in rotaciones.items():
        if pieza in value:
            nombre = key
    
    numero_de_rot = (rotaciones[nombre]).index(pieza)
    if numero_de_rot == len(rotaciones[nombre])-1:
        numero_de_rot = 0
    else:
        numero_de_rot += 1
    
    return tuple(rotaciones[nombre][numero_de_rot])
    

def rotar(juego,rotaciones):
    pieza = sorted(pieza_actual(juego))
    x , y = pieza[0]

    pieza = trasladar_pieza(pieza, -x, -y)
    siguiente_rotacion = buscar_rotaciones(pieza,rotaciones)
    siguiente_rotacion = trasladar_pieza(siguiente_rotacion, x, y)

    se_puede_rotar = True
    for x,y in siguiente_rotacion:
        if (x > ANCHO_JUEGO-1 or x < 0 or y > ALTO_JUEGO-1 or y < 0) or hay_superficie(juego,x,y):
            se_puede_rotar = False

    if se_puede_rotar:
        borrar_pieza_actual(juego)
        dibujar_pieza(juego,siguiente_rotacion)

    return juego


def borrar_pieza_actual(juego):
    pieza_a_borrar=pieza_actual(juego)
    for x,y in pieza_a_borrar:
            juego[y][x] = "0"   #Elimino el estado de pieza anterior.

def dibujar_pieza(juego,pieza_a_dibujar):
    for x,y in pieza_a_dibujar:
            juego[y][x] = "+"

    return juego

def buscar_superficies(juego):
    superficies = []

    for columna in range(ALTO_JUEGO):
        for fila in range(ANCHO_JUEGO):
            if juego[columna][fila] == "#":
                superficies.append((fila,columna))
    
    return tuple(superficies)

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """

    se_puede_descender = True
    pieza = pieza_actual(juego)
    pieza_movida = trasladar_pieza(pieza,0,1)
    puntos_acumulados=0

    for x,y in pieza_movida:         #Chequeo que el movimiento es valido.
        if y > ALTO_JUEGO-1 or y < 0 or juego[y][x] == "#":
            se_puede_descender = False

    if se_puede_descender: 
        siguiente_pieza = False
        borrar_pieza_actual(juego)
        dibujar_pieza(juego,pieza_movida)
    else:
        for x,y in pieza:
            juego[y][x] = "#"
    

        juego,puntos_acumulados = eliminar_lineas(juego)

        siguiente_pieza = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2 ,0) #Inicializo la siguiente pieza y la centro.
        puedo_agregar_pieza = True
        for x,y in siguiente_pieza:
            if juego[y][x] == "#":
                puedo_agregar_pieza = False

        if puedo_agregar_pieza:
            juego = dibujar_pieza(juego,siguiente_pieza)

                
    return juego,siguiente_pieza, puntos_acumulados

def calcular_puntaje(cantidad_a_eliminar):

    if cantidad_a_eliminar==0:
        return 0
    elif cantidad_a_eliminar==1:
        return 40
    elif cantidad_a_eliminar==2:
        return 100
    elif cantidad_a_eliminar==3:
        return 300
    elif cantidad_a_eliminar==4:
        return 1200    


def eliminar_lineas(juego):

    cantidad_a_eliminar = 0
    
    for i in range(len(juego)): ##Elimino Lineas si se completan
        if juego[i].count("#") == (ANCHO_JUEGO):
            cantidad_a_eliminar += 1
          
    for i in range(cantidad_a_eliminar):
        juego.remove(["#"]*ANCHO_JUEGO)

    for i in range(cantidad_a_eliminar):
        juego.insert(0,["0"]*ANCHO_JUEGO)

    puntos=calcular_puntaje(cantidad_a_eliminar)     

    return (juego,puntos)
      
def terminado(juego):

    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """
    return len(pieza_actual(juego))==0

def guardar_partida(juego,ruta):
    with open(ruta,"w") as archivo:
        for fila in juego:
            linea = str(fila).lstrip("[").rstrip("]").replace("'","").replace(",","")
            archivo.write(linea+"\n")
    
    

def cargar_partida(ruta):
    tabla = []
    try:
        with open(ruta,"r") as archivo:
            for linea in archivo:
                if linea.strip():
                    linea = linea.rstrip("\n").split(" ")
                    tabla.append(linea)
    except:
        return None
    return tabla  

def guardar_puntaje(juego,ruta):
    with open(ruta,"w") as archivo:
        for fila in juego:
            linea=fila.lstrip("[").rstrip("]").replace("'","").replace(",","")
            archivo.write(linea+"\n")

def guardar_score(nombre,score):
    puntajes = []
    try:
        with open("scores.txt","r") as archivo:
            for linea in archivo:
                jugador,puntos = linea.rstrip("\n").split(" ")
                puntajes.append([int(puntos),jugador])
                          
            puntajes.insert(0,[int(score),nombre])
            
            puntajes=sorted(puntajes,reverse=True)

            if len(puntajes) > 10:
                puntajes.pop()                
            
        
        with open("scores.txt","w") as archivo2:
            for puntaje,nombres in puntajes:
                archivo2.write(f"{nombres} {puntaje}\n")
    except:
        with open("scores.txt","w") as archivo3: #En caso de fallar al leer el archivo(no existe aun)
            archivo3.write(f"{nombre} {score}\n")

     