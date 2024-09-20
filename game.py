import pygame
from personaje import Cubo
from enemigo import Enemigo
from bala import Bala
import random

pygame.init()

ancho = 1000
alto = 800
ventana = pygame.display.set_mode([ancho, alto])
fps = 120
fuente = pygame.font.SysFont("comic sans", 30)

def juego():
    jugando = True

    reloj = pygame.time.Clock()
    vida = 5
    puntos = 0

    tiempo_pasado = 0  
    tiempo_entre_enemigos = 500 

    cubo = Cubo(ancho / 2, alto - 75)

    enemigos = []  
    balas = []

    ultima_bala = 0  # Aquí definimos la variable 'ultima_bala'
    tiempo_entre_balas = 200

    enemigos.append(Enemigo(ancho / 2, 100)) 

    def crear_bala():
        nonlocal ultima_bala  # Usamos 'nonlocal' en lugar de 'global' porque 'ultima_bala' está en el ámbito de la función 'juego'

        if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
            balas.append(Bala(cubo.rect.centerx, cubo.rect.centery))
            ultima_bala = pygame.time.get_ticks()

    def gestionar_teclas(teclas):
        if teclas[pygame.K_a]:
            cubo.x -= cubo.velocidad
        if teclas[pygame.K_d]:
            cubo.x += cubo.velocidad
        if teclas[pygame.K_SPACE]:
            crear_bala()

    while jugando and vida > 0:
        tiempo_pasado += reloj.tick(fps)

        if tiempo_pasado > tiempo_entre_enemigos:
            enemigos.append(Enemigo(random.randint(0, ancho), -100))
            tiempo_pasado = 0
        
        eventos = pygame.event.get()

        teclas = pygame.key.get_pressed()

        texto_vida = fuente.render(f"vida: {vida}", True, "white")
        texto_puntos = fuente.render(f"puntos: {puntos}", True, "white")

        gestionar_teclas(teclas)

        for evento in eventos:
            if evento.type == pygame.QUIT:
                return False
    
        ventana.fill("black")

        cubo.dibujar(ventana)

        # Manejando los enemigos
        enemigos_a_eliminar = []
        for enemigo in enemigos:
            enemigo.dibujar(ventana)
            enemigo.movimiento()

            if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
                vida -= 1 
                print(f"te quedan {vida} vidas")
                enemigos_a_eliminar.append(enemigo)

            if enemigo.y + enemigo.alto > alto:
                puntos += 1
                enemigos_a_eliminar.append(enemigo)

            # Colisión de balas con enemigos
            balas_a_eliminar = []
            for bala in balas:
                if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                    enemigos_a_eliminar.append(enemigo)  # Eliminar enemigo si la bala lo impacta
                    balas_a_eliminar.append(bala)  # Eliminar bala que impactó
                    puntos += 1

            # Eliminar las balas que colisionaron
            for bala in balas_a_eliminar:
                balas.remove(bala)

        # Eliminar los enemigos que deben desaparecer
        for enemigo in enemigos_a_eliminar:
            enemigos.remove(enemigo)

        # Manejando las balas
        balas_a_eliminar = []
        for bala in balas:
            bala.dibujar(ventana)
            bala.movimiento()
            if bala.y < 0:
                balas_a_eliminar.append(bala)

        # Eliminar las balas que salieron de la pantalla
        for bala in balas_a_eliminar:
            balas.remove(bala)
        
        # Dibujar texto
        ventana.blit(texto_vida, (20, 20))
        ventana.blit(texto_puntos, (20, 50))

        pygame.display.update()

    return True  # Si la vida llega a 0, regresamos True para activar la pantalla de reinicio

def mostrar_pantalla_final():
    ventana.fill("black")
    texto_perder = fuente.render("GameOver, ENTER para volver a jugar", True, "white")
    ventana.blit(texto_perder, (ancho // 2 - texto_perder.get_width() // 2, alto // 2 - texto_perder.get_height() // 2))
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return True

while True:
    if not juego():
        break  # Si el jugador cierra el juego, terminamos el bucle
    if not mostrar_pantalla_final():
        break  # Si el jugador cierra la pantalla final, terminamos el bucle

pygame.quit()

 