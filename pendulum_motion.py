import pygame
import basicUI
import random
from math import cos, sin
from time import time

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

g = 9.807

class Particle:

    def __init__(self, mass_slider, radius_slider, particles, angle, force=0, colour=PARTICLE_COLOUR) -> None:

        if particles:
            self.first = False
            self.pivot = particles[-1].center
        else:
            self.first = True
            self.pivot = (sim_width // 2, 100)
            
        particles.append(self)
        self.index = len(particles) - 1
        self.particles = particles

        self.angle = angle
        self.force = force
        
        self.tension = 0

        self.mass_slider = mass_slider
        self.radius_slider = radius_slider
        
        self.min_radius = 25
        
        self.colour = colour
        self.center = (self.min_radius + self.pivot[0] + (self.radius_slider.value*200*cos(self.angle)),
                       self.min_radius + self.pivot[1] + (self.radius_slider.value*200*sin(self.angle)))
        
    
    def draw_line(self, surface) -> None:
        
        pygame.draw.line(surface, (0, 0, 0), self.pivot, self.center, width=2)
    
    def draw_particle(self, surface) -> None:

        pygame.draw.circle(surface, self.colour, self.center, (self.mass_slider.value * 40) + 10)

    def get_angular_velocity(self) -> None:
        
        pass
    
    def get_centre(self) -> None:
        
        pass

    def update(self) -> None:
        
        self.center = (self.min_radius + self.pivot[0] + (self.radius_slider.value*200*math.cos(self.angle)),
                       self.min_radius + self.pivot[1] + (self.radius_slider.value*200*math.sin(self.angle)))

        if not self.first:
            self.pivot = self.particles[self.index - 1].center
        
    
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
Particle(mass1, radius1, particles, 0.1)
Particle(mass2, radius2, particles, 0.9)

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
        ptc.draw_line(win)
    for ptc in particles:
        ptc.draw_particle(win)

    draw_ui()

    pygame.display.update()

def main() -> None:
    
    while True:
        
        clock.tick(60)
        
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                
                if pygame.key.get_pressed()[pygame.K_EQUALS]:
                    particles[-1].angle += 0.1
                if pygame.key.get_pressed()[pygame.K_MINUS]:
                    particles[-1].angle -= 0.1
        
        if particles:
            ptc = particles[0]
            diff = 2
            if keys[pygame.K_RIGHT]:
                ptc.pivot = (ptc.pivot[0] + diff, ptc.pivot[1])
            if keys[pygame.K_LEFT]:
                ptc.pivot = (ptc.pivot[0] - diff, ptc.pivot[1])
            if keys[pygame.K_UP]:
                ptc.pivot = (ptc.pivot[0], ptc.pivot[1] - diff)
            if keys[pygame.K_DOWN]:
                ptc.pivot = (ptc.pivot[0], ptc.pivot[1] + diff)
        
        last_ptc = particles[-1]
        last_ptc.tension = (last_ptc.mass*g) / cos(last_ptc.angle)
        
        for r in reversed(range(1, len(particles) - 2)):
            curr_ptc = particles[r]
            prev_ptc = particles[r + 1]
            next_ptc = particles[r - 1]
            curr_ptc.tension = (prev_ptc.tension*cos(curr_ptc.angle) + curr_ptc.mass) / cos(next_ptc.angle)
            
        for slider_id in sliders:
            sliders[slider_id].update()
            
        for ptc in particles:
            ptc.update()

        draw_surface()

if __name__ == '__main__':
    main()