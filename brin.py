#! /usr/bin/python

import sys
import pygame
import pygame.camera
from pygame.locals import *

DEVICE = '/dev/video0'
SIZE = (1280, 720)
FILENAME = 'capture.png'


def camstream():
    pygame.init()
    pygame.camera.init()
    display = pygame.display.set_mode(SIZE, 0)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    capture = True

    while capture:
        screen = camera.get_image(screen)
        display.blit(screen, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                capture = False
            elif event.type == KEYDOWN and event.key == K_q:
                camera.stop()
                pygame.quit()
    return

if __name__ == '__main__':
    camstream()
    sys.exit()