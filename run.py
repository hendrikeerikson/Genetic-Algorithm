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
    surf = Globals.font.render("FPS=" + str(1000//Globals.ms), False, [200, 200, 200])
    scr.blit(surf, [10, 10])


# generate 300 pieces of food
def generate_food():
    Globals.food = {}

    for i in range(150):
        Globals.food[(randint(0, 79), randint(0, 59),)] = 1


# breed and generate new animals and blast them with radiation
def end_cycle():
    scored_animals = {}

    for i in Globals.animals:
        score = Globals.animals[i].score
        scored_animals[score + uniform(-0.3, 0.3)] = i

    ordered_scores = sorted(scored_animals.keys())

    print("This generation's score is : ", round(sum(ordered_scores)), " Generation : ", generation)

    weights1 = []
    weights2 = []

    for i in range(1, 4):
        weights1.append(Globals.animals[scored_animals[ordered_scores[-i]]].weights1)
        weights2.append(Globals.animals[scored_animals[ordered_scores[-i]]].weights2)

    Globals.animals = {}

    for i in range(20):
        new_weights1 = character.breed(weights1)
        new_weights2 = character.breed(weights2)
        Globals.animals[i] = character.Animal()
        Globals.animals[i].weights1 = deepcopy(new_weights1)
        Globals.animals[i].weights2 = deepcopy(new_weights2)
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

    framecount = 0
    generation = 1
    generate_food()

    while True:
        cam.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                # exit the program
                pg.quit()
                sys.exit()

        for i in Globals.animals:
            Globals.animals[i].update()

        if framecount == 150:
            framecount = 0
            end_cycle()
            generation += 1
            cam.pos = np.array([0, 0])

        framecount += 1

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

        display_fps(screen)
        pg.display.flip()  # switch frame buffers