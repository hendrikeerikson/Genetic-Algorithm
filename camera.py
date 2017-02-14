import pygame as pg
import numpy as np
from globals import *


# normalize a numpy vector
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v/norm


class Camera:
    def __init__(self):
        self.pos = np.array([0, 0])
        self.vel = np.array([0, 0])
        self.maxvel = 0.5

    def update(self):
        pressed = pg.key.get_pressed()
        self.vel[0] = 0
        self.vel[1] = 0

        if pressed[pg.K_UP]:
            self.vel[1] = -1

        elif pressed[pg.K_DOWN]:
            self.vel[1] = 1

        if pressed[pg.K_LEFT]:
            self.vel[0] = -1

        elif pressed[pg.K_RIGHT]:
            self.vel[0] = 1

        if pressed[pg.K_UP] and pressed[pg.K_DOWN]:
            self.vel[1] = 0

        if pressed[pg.K_LEFT] and pressed[pg.K_RIGHT]:
            self.vel[0] = 0

        self.vel = normalize(self.vel)
        self.pos = self.pos + self.vel * self.maxvel * Globals.ms
