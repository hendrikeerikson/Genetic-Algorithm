import pygame as pg
import numpy as np
import sys
from globals import Globals
import camera, character
from math import floor
from random import randint, uniform
from copy import deepcopy


# draw a grid in the background
def draw_background(scr, campos):
    sqr = 80  # side length of a single tile

    x = floor(campos[0]/sqr)
    y = floor(campos[1]/sqr)

    offsetx = campos[0] - x * sqr
    offsety = campos[1] - y * sqr

    for i in range(Globals.width // sqr + 1):
        for j in range(Globals.height // sqr + 2):
            if (x + i) % 2 == 0 and (y + j) % 2 != 0:
                pg.draw.rect(scr, [25, 25, 25], [i*sqr-offsetx, j*sqr-offsety, sqr, sqr])

            elif (x + i) % 2 != 0 and (y + j) % 2 == 0:
                pg.draw.rect(scr, [25, 25, 25], [i*sqr-offsetx, j*sqr-offsety, sqr, sqr])


def display_fps(scr):
    surf = Globals.font.render("FPS=" + str(1000//Globals.ms), False, [200, 200, 200], [0, 0, 0])
    scr.blit(surf, [10, 10])


# generate 300 pieces of food
def generate_food():
    Globals.food = {}

    for i in range(150):
        Globals.food[(randint(0, 79), randint(0, 59),)] = 1


# breed and generate new animals and blast them with radiation
def end_cycle():
    weights = []

    # add each type of brain to the mix proportionally to its score
    for i in Globals.animals:
        weights += [[Globals.animals[i].weights1, Globals.animals[i].weights2]] * Globals.animals[i].score

    print("Total amount of brains in the pool : ", len(weights), " in generation : ", generation)

    for i in range(20):
        new_weights = character.breed(weights)
        Globals.animals[i] = character.Animal()
        Globals.animals[i].weights1 = deepcopy(new_weights[0])
        Globals.animals[i].weights2 = deepcopy(new_weights[1])
        Globals.animals[i].mutate()

    generate_food()


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((Globals.width, Globals.height))

    clock = pg.time.Clock()
    Globals.ms = clock.tick()

    cam = camera.Camera()

    screen.fill((0, 0, 0))  # fill screen with black
    Globals.font = pg.font.Font(None, 20)

    for i in range(20):
        Globals.animals[i] = character.Animal()

    generation = 1
    generate_food()

    while True:
        cam.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                # exit the program
                pg.quit()
                sys.exit()

        # add the position of every animal to a dict for later lookup
        # lookup from dicts is faster then from lists
        Globals.animal_pos = {}
        for i in Globals.animals:
            Globals.animal_pos[(Globals.animals[i].pos[0], Globals.animals[i].pos[1], )] = 1

        # update the brains and position of every animal
        for i in Globals.animals:
            Globals.animals[i].update()

        # if no one has eaten for 90 frames end cycle
        if Globals.time_left <= 0:
            Globals.time_left = 150
            end_cycle()
            generation += 1
            cam.pos = np.array([0, 0])

        # keep adding frames
        Globals.time_left -= 1

        if pg.key.get_pressed()[pg.K_q]:
            Globals.time_left = 70

        # when space is held down, do not restrict fps and stop rendering
        if not pg.key.get_pressed()[pg.K_SPACE]:
            screen.fill((0, 0, 0))
            draw_background(screen, cam.pos)

            for i in Globals.animals:
                Globals.animals[i].draw(screen, cam.pos)

            for i in Globals.food:
                pg.draw.rect(screen, [0, 255, 20], [i[0] * Globals.tilesize - cam.pos[0],
                                                    i[1] * Globals.tilesize - cam.pos[1],
                                                    Globals.tilesize,
                                                    Globals.tilesize])
            Globals.ms = clock.tick(30)

        else:
            Globals.ms = clock.tick()

        display_fps(screen)
        pg.display.flip()  # switch frame buffers