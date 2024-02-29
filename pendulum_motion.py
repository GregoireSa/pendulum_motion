import pygame
import basicUI

pygame.init()

width, height = 900, 600
sim_width = 600
ui_width = width - sim_width

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("pendulum motion")
clock = pygame.time.Clock()

# COLOURS
BG_COLOUR = (255, 250, 220)
UI_BG_COLOUR = (50, 50, 50)
PARTICLE_COLOUR = (255, 0, 0)

class Particle:

    def __init__(self, mass, radius, particles, center, colour=PARTICLE_COLOUR) -> None:

        if particles:
            self.pivot = self.particles[-1].center
        else:
            self.pivot = (sim_width // 2, 100)
        particles.append(self)
        self.particles = particles

        self.mass = mass
        self.radius = radius
        self.colour = colour

        self.center = center
    
    def draw(self, surface) -> None:

        pygame.draw.circle(surface, self.colour, self.center, 20)

sliders = []
sliders.append(basicUI.Slider(win, (sim_width + 20, 50), ui_width * 0.75, 40))


def draw_ui() -> None:

    ui_bg_rect = pygame.Rect(sim_width, 0, ui_width, height)
    pygame.draw.rect(win, UI_BG_COLOUR, ui_bg_rect)
    for slider in sliders:
        slider.draw()

def draw_surface() -> None:
    
    win.fill(BG_COLOUR)

    for ptc in particles:
        ptc.draw(win)

    draw_ui()

    pygame.display.update()

particles = []
particles.append(Particle(5, 10, particles, (sim_width // 2, 300)))

def main() -> None:
    
    while True:
        
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        for slider in sliders:
            slider.update()

        draw_surface()

if __name__ == '__main__':
    main()