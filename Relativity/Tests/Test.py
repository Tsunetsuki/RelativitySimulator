import pygame
import math
from pygame import gfxdraw
import numpy as np
pygame.font.init()

font_renderer = pygame.font.SysFont("arial", 30)

cw = 1200
ch = 800

win = pygame.display.set_mode((cw, ch))
clock = pygame.time.Clock()

sun_x = cw / 2
sun_y = ch / 2

c = 600 #Lichtgeschwindigkeit

x = sun_x - 100
y = sun_y - 100
vx = 0
vxHyp = 0
aHyp = 3
#vy = 0

radius = 30

run = True
pygame.event.pump()
frames = 0
fps = 300

t = 0

while run:
    d = clock.tick() / 1000
    t_last = t
    t = pygame.time.get_ticks() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_a]:
        vxHyp -= aHyp * d
    if keys[pygame.K_d]:
        vxHyp += aHyp * d


    #if keys[pygame.K_s]:
    #    sun_y += sun_v * d
    #if keys[pygame.K_w]:
    #    sun_y -= sun_v * d

    vx = np.tanh(vxHyp) * c
    x += vx * d


    if int(t) != int(t_last):
        fps = frames
        frames = 0


    pygame.draw.rect(win, (200, 200, 200), (0, 0, cw, ch)) # cls

    pygame.draw.circle(win, (200, 128, 0), (int(x), int(y)), radius)

    #pygame.draw.line(win, (0, 0, 0), (x, y), (x + vx, y + vy))
    #pygame.draw.line(win, (0, 150, 0), (x, y), (x + ax, y + ay))

    fps_img = font_renderer.render("FPS: " + str(fps), True, (0, 0, 0))
    vx_img = font_renderer.render("VX: " + str(vx), True, (0, 0, 0))
    win.blit(fps_img, (20, 20))
    win.blit(vx_img, (20, 50))


    pygame.display.update()
pygame.quit()








def maprange(s, a, b):
    (a1, a2), (b1, b2) = a, b
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
