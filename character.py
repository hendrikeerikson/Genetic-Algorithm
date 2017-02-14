import numpy as np
from random import randint
from globals import Globals
import pygame as pg
from math import e
from random import choice


# return a sigmoid in the range of -1 to 1 with a large slope
def sigmoid(x):
    return 1 / (1 + e**(-3*x))


# take two sets of two weights from the list and breed them together
def breed(weight_list):
    # choose two random sets of weights, [weights1, weights2]
    weights_A = choice(weight_list)
    weights_B = choice(weight_list)

    size1 = weights_A[0].shape  # size of weights1
    size2 = weights_A[1].shape  # size of weights2

    new_weights = [np.zeros(size1, dtype=np.float32),
                   np.zeros(size2, dtype=np.float32)]

    # breed them together row at a time
    for i in range(size1[0]):
            new_weights[0][i] = choice([weights_A[0][i], weights_B[0][i]])

            # breed them together row at a time
    for i in range(size2[0]):
        new_weights[1][i] = choice([weights_A[1][i], weights_B[1][i]])

    return new_weights


class Animal:
    def __init__(self):
        self.score = 1

        self.pos = np.array([randint(0, 79), randint(0, 59)], dtype=np.float32)
        self.vision = np.zeros([7, 7], dtype=np.float32)

        # set the neurons and weights in such a way as to allow them to be multiplied
        self.layer1 = np.zeros([1, 49], dtype=np.float32)
        self.layer2 = np.zeros([1, 15], dtype=np.float32)
        self.layer3 = np.zeros([1, 4], dtype=np.float32)

        # set the initial values of the weights from -1/sqrt(d) to 1/sqrt(d) where d is the number of inputs
        self.weights1 = np.random.uniform(-0.4, 0.4, [49, 15])
        self.weights2 = np.random.uniform(-0.4, 0.4, [15, 4])

    # the animal sees in 7x7 grid around it, it can only see food sources not other animals
    def update_vision(self):
        self.vision = np.zeros([7, 7], dtype=np.float32)

        for i in range(-3, 4):
            for j in range(-3, 4):
                if self.pos[0]+i < 0 or self.pos[0]+i >= 80 or self.pos[1]+j < 0 or self.pos[1]+j >= 60:
                    self.vision[i + 3][j + 3] = -1
                elif (self.pos[0]+i, self.pos[1]+j, ) not in Globals.food:
                    self.vision[i+3][j+3] = 1

    # called every two frames
    def update(self):
        self.update_vision()

        self.layer1 = self.vision.reshape([1, 49])  # set layer 1 equal to the animals vision
        self.layer2 = sigmoid(np.dot(self.layer1, self.weights1))  # multiply to get the neuron's value

        self.layer3 = np.dot(self.layer2, self.weights2)

        self.layer3 = sigmoid(self.layer3)  # clip the output to -1 or 0 or 1 based on the sigmoid

        vel = np.array([0, 0])

        # choose the largest direction on a single dimension 0 and 1 are x, 2 and 3 are y
        if self.layer3[0][0] > self.layer3[0][1]:
            vel[0] = self.layer3[0][0].round()
        else:
            vel[0] = -self.layer3[0][1].round()

        if self.layer3[0][2] > self.layer3[0][3]:
            vel[1] = self.layer3[0][2].round()
        else:
            vel[1] = -self.layer3[0][3].round()

        # detect collision with walls
        if 0 <= (self.pos[0] + vel[0]) < 80:
            self.pos[0] += vel[0]  # move the animal based on the output

        if 0 <= self.pos[1] + vel[1] < 60:
            self.pos[1] += vel[1]

        # eat food that you bump into
        if (self.pos[0], self.pos[1],) in Globals.food:
            self.score += 10
            Globals.food.pop((self.pos[0], self.pos[1],))

    # draw a regular rect on the screen at the animals position
    def draw(self, scr, campos):
        pg.draw.rect(scr, [255, 20, 50], [self.pos[0]*Globals.tilesize-campos[0],
                                          self.pos[1]*Globals.tilesize-campos[1],
                                          Globals.tilesize, Globals.tilesize])

    def mutate(self):
        '''
        count = randint(4, 20)  # number of mutations
        for i in range(count):
            choice = randint(0, 1)  # choose a layer to mutate

            if choice == 0:
                x = randint(0, 48)
                y = randint(0, 14)

                self.weights1[x][y] += np.random.uniform(-0.1, 0.1)

            elif choice == 1:
                x = randint(0, 14)
                y = randint(0, 1)

                self.weights1[x][y] += np.random.uniform(-0.1, 0.1)
        '''

        self.weights1 += np.random.uniform(-0.02, 0.02, size=self.weights1.shape)
        self.weights2 += np.random.uniform(-0.02, 0.02, size=self.weights2.shape)
