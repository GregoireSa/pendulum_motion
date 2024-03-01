import pygame
import math
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
UI_ELEM_COLOUR = (100, 100, 100)
PARTICLE_COLOUR = (255, 0, 0)

class Particle:

    def __init__(self, mass_slider, radius_slider, particles, center, colour=PARTICLE_COLOUR) -> None:

        if particles:
            self.pivot = self.particles[-1].center
        else:
            self.pivot = (sim_width // 2, 100)
        particles.append(self)
        self.particles = particles

        self.mass = mass_slider.value
        self.mass_slider = mass_slider
        self.radius = radius_slider.value
        self.radius_slider = radius_slider
        
        self.colour = colour
        self.center = center
    
    def draw(self, surface) -> None:

        pygame.draw.circle(surface, self.colour, self.center, (self.mass_slider.value * 40) + 10)

text_margin = 50

sliders = {}
def new_slider(name, center) -> basicUI.Slider:
    sld = basicUI.Slider(win, (0, 0), ui_width * 0.5, 40, slider_colour=UI_ELEM_COLOUR)
    sld.set_center(center)
    sliders.update({name: sld})
    return sld
    
mass1 = new_slider("Mass 1:", (text_margin + sim_width + ui_width // 2, 100))
radius1 = new_slider("Radius 1:", (text_margin + sim_width + ui_width // 2, 150))
mass2 = new_slider("Mass 2:", (text_margin + sim_width + ui_width // 2, 200))
radius2 = new_slider("Radius 2:", (text_margin + sim_width + ui_width // 2, 250))

particles = []
particles.append(Particle(mass1, radius1, particles, (sim_width // 2, 300)))

def draw_ui() -> None:

    ui_bg_rect = pygame.Rect(sim_width, 0, ui_width, height)
    pygame.draw.rect(win, UI_BG_COLOUR, ui_bg_rect)
    for slider_id in sliders:
        slider = sliders[slider_id]
        slider.draw()
        x_pos = sim_width + text_margin
        basicUI.text(win, slider_id, (x_pos, slider.bar.centery), UI_ELEM_COLOUR)

def draw_surface() -> None:
    
    win.fill(BG_COLOUR)

    for ptc in particles:
        ptc.draw(win)

    draw_ui()

    pygame.display.update()

def main() -> None:
    
    while True:
        
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        for slider_id in sliders:
            sliders[slider_id].update()

        draw_surface()

if __name__ == '__main__':
    main()