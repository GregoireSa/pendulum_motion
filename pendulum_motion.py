import pygame

pygame.init()

width, height = 300, 300
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("pendulum motion")
clock = pygame.time.Clock()