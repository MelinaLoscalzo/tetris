import tetris
import gamelib
import random

 
partidas="partida.txt"
tabla_puntuacion="scores.txt"
teclas="teclas.txt"
piezas_rotadas="piezas.txt"

ESPERA_DESCENDER = 8
TAM_CELDA=30
ANCHO_VENTANA=600
ALTO_VENTANA=700

COLORS = ["red","RoyalBlue1","DarkOrange1","goldenrod1","hot pink","aquamarine","blue violet"]



def dibujar_grilla(juego):
    gamelib.draw_image('img/fondo.gif',4,4)
    ANCHO,ALTO=tetris.dimensiones(juego)
    for x in range(ANCHO):
        for y in range(ALTO):
            gamelib.draw_rectangle(x*TAM_CELDA,y*TAM_CELDA,x*TAM_CELDA+TAM_CELDA,y*TAM_CELDA+TAM_CELDA,fill="black",outline="cyan")                 
    
    return juego


def dibujar_pieza(juego):
        
    for x,y in tetris.pieza_actual(juego):
       gamelib.draw_rectangle(x*TAM_CELDA,y*TAM_CELDA,x*TAM_CELDA+TAM_CELDA,y*TAM_CELDA+TAM_CELDA,fill=(random.choice(COLORS)),outline="black")

def dibujar_pieza_siguiente(siguiente_pieza):
    
    for x,y in siguiente_pieza:        
        gamelib.draw_rectangle(x*TAM_CELDA+350,y*TAM_CELDA+75,x*TAM_CELDA+TAM_CELDA+350,y*TAM_CELDA+TAM_CELDA+75,fill="red",outline="white") 
        


def dibujar_pieza_consolidada(juego):
    
    Ancho,Alto=tetris.dimensiones(juego)
    for x in range(Ancho):
        for y in range(Alto):
            if tetris.hay_superficie(juego,x,y):
               gamelib.draw_rectangle(x*TAM_CELDA,y*TAM_CELDA,x*TAM_CELDA+TAM_CELDA,y*TAM_CELDA+TAM_CELDA,fill="white",outline="black")


def dibujar_puntuacion(score):
        gamelib.draw_text(score,450,200,size=20,fill="white",anchor="nw")

def validar_score(puntaje):
    
    if 0 <= puntaje < 1000:
        return (False,0)
    if 1000 <= puntaje <2000:
        return (True,1)
    if 3000<= puntaje <4000:
        return (False,2)

def level(tiempo, puntaje):
    cambiar_tiempo,porcentaje = validar_score(puntaje)
    if cambiar_tiempo:
        return tiempo-porcentaje*tiempo
    return tiempo 

         
    
def cargar_rotaciones():
    piezas_con_rotaciones = {}

    with open(piezas_rotadas,"r") as f_piezas:
        for linea in f_piezas:
            lista_rotaciones = []

            linea = linea.rstrip("\n").split(" # ")
            pieza,rotaciones = linea[1],linea[0]

            rotaciones = rotaciones.split(" ")
            for rot in rotaciones:
                pieza_en_rotacion = []
                rot = rot.split(";")

                for pos in rot:
                    x , y = pos.split(",")
                    pieza_en_rotacion.append((int(x),int(y)))

                lista_rotaciones.append(tuple(pieza_en_rotacion))

            piezas_con_rotaciones[pieza] = lista_rotaciones
        
        return piezas_con_rotaciones


def cargar_teclas(ruta):
    teclas={}
    
    with open(ruta,"r") as f_teclas:
        for linea in f_teclas:
            if linea.strip():
                linea=linea.rstrip("\n").split(" = ")
                tecla,accion=linea[0],linea[1]
                teclas[tecla]=accion
    return teclas

def mostrar_scores(ruta):
    puntajes=""
    with open(ruta,"r") as archivo:
        for linea in archivo:
            nombre,score=linea.rstrip("\n").split(" ")
            linea=f"{nombre:10} --- {score}\n"
            puntajes+=linea

    gamelib.title("Mostrando Puntajes..")
    gamelib.say(puntajes)    



def main():
    # Inicializar el estado del juego
    gamelib.resize(ANCHO_VENTANA,ALTO_VENTANA)
    piezas = cargar_rotaciones()
    juego=tetris.crear_juego(tetris.generar_pieza(piezas))
    siguiente_pieza=tetris.generar_pieza(piezas)
    gamelib.play_sound('sound/play.wav')
    controles=cargar_teclas(teclas)
    descender_pieza=False
    gamelib.title("MELTRIX")
    score=0    
    

    timer_bajar = ESPERA_DESCENDER   
    salir=False
    while gamelib.loop(fps=30) and not tetris.terminado(juego):
        if descender_pieza:
            siguiente_pieza=tetris.generar_pieza(piezas)
        gamelib.draw_begin()
        # Dibujar la pantalla     
             
        dibujar_grilla(juego)
        dibujar_pieza(juego)
        dibujar_pieza_consolidada(juego)
        dibujar_pieza_siguiente(siguiente_pieza)
        dibujar_puntuacion(score)

        gamelib.draw_end()        
        for event in gamelib.get_events():
          if not event:
              break
          if event.type == gamelib.EventType.KeyPress:
              tecla = event.key
              # Actualizar el juego, según la tecla presionada
              if tecla in controles.keys():
                  if controles[tecla]=="IZQUIERDA":
                      juego=tetris.mover(juego,tetris.IZQUIERDA)
                  if controles[tecla]=="DERECHA":
                      juego=tetris.mover(juego,tetris.DERECHA)
                  if controles[tecla]=="DESCENDER":
                      juego = tetris.descender(juego)
                  if controles[tecla]=="ROTAR":
                      juego=tetris.rotar(juego,piezas)
                  if controles[tecla]=="GUARDAR":
                      tetris.guardar_partida(juego,partidas)
                      gamelib.say(f"¡Has guardado la partida!")
                  if controles[tecla]=="CARGAR":
                      nueva_partida = tetris.cargar_partida(partidas)
                      if nueva_partida != None:
                          juego = nueva_partida
                  if controles[tecla]=="SALIR":
                      return
                      

        if salir:
            break  
                                        
        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = level(ESPERA_DESCENDER,score)
            # Descender la pieza automáticamente
            juego,descender_pieza,puntos_acumulados=tetris.avanzar(juego,siguiente_pieza)
            score+=puntos_acumulados
            
    if not salir:
            gamelib.say(f"¡Has Perdido! y tu puntaje fue: {score}!")
            gamelib.play_sound('sound/perdiste.wav')
            nombre = gamelib.input("¡Ingresa tu nombre!")
            tetris.guardar_score(nombre.capitalize(),score)
            mostrar_scores(tabla_puntuacion)

           

gamelib.init(main)
