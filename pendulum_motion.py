import pygame
import basicUI
from math import cos, sin, tan

pygame.init()

width, height = 1100, 600
sim_width = 800
ui_width = width - sim_width

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("pendulum motion")
clock = pygame.time.Clock()
max_fps = 60

# COLOURS
BG_COLOUR = (255, 250, 220)
UI_BG_COLOUR = (50, 50, 50)
UI_ELEM_COLOUR = (100, 100, 100)
PARTICLE_COLOUR = (255, 0, 0)

g = 9.807

class Particle:

    def __init__(self, mass_slider, radius_slider, particles, angle, colour: tuple=PARTICLE_COLOUR) -> None:

        if particles:
            self.first = False
            self.pivot = particles[-1].center
        else:
            self.first = True
            self.pivot = (sim_width // 2, 100)
        
        self.vel = (0, 0)
        self.acc = 0
        
        particles.append(self)
        self.index = len(particles) - 1
        self.particles = particles

        self.angle = angle
        
        self.tension = 0
        self.angular_vel = 0

        self.mass_slider = mass_slider
        self.radius_slider = radius_slider
        self.mass = self.mass_slider.value
        self.radius = self.radius_slider.value
                
        self.colour = colour
        self.center = (self.pivot[0] + (self.radius*cos(self.angle)),
                        self.pivot[1] + (self.radius*sin(self.angle)))
        
    
    def draw_line(self, surface) -> None:
        
        pygame.draw.line(surface, (0, 0, 0), self.pivot, self.center, width=2)
    
    
    def draw_particle(self, surface) -> None:

        pygame.draw.circle(surface, self.colour, self.center, (self.mass) + 10)
        

    def update(self) -> None:
        
        self.mass = self.mass_slider.value
        self.radius = self.radius_slider.value
        
        self.angle += self.angular_vel * 0.1
        
        self.center = (self.pivot[0] + (self.radius*100*cos(self.angle)),
                       self.pivot[1] + (self.radius*100*sin(self.angle)))

        if not self.first:
            self.pivot = self.particles[self.index - 1].center
        
    
text_margin = 50

sliders = {}
def new_slider(name, center, min_val, max_val) -> basicUI.Slider:
    sld = basicUI.Slider(win, (0, 0), ui_width * 0.5, 40, slider_colour=UI_ELEM_COLOUR, min_val=min_val, max_val=max_val)
    sld.set_center(center)
    sliders.update({name: sld})
    return sld
    
mass1 = new_slider("Mass 1:", (text_margin + sim_width + ui_width // 2, 100), 1, 40)
radius1 = new_slider("Radius 1:", (text_margin + sim_width + ui_width // 2, 150), 1, 4)
radius1.value = 2
mass2 = new_slider("Mass 2:", (text_margin + sim_width + ui_width // 2, 200), 1, 40)
radius2 = new_slider("Radius 2:", (text_margin + sim_width + ui_width // 2, 250), 1, 4)

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
        
        pygame.display.set_caption(f"pendulum motion    fps: {int(clock.get_fps())}")
        clock.tick(max_fps)
        
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

        
        p1 = particles[0]
        p2 = particles[1]
        
        p2.tension = (p2.mass*g) / cos(p2.angle)
        p1.tension = (p2.tension*cos(p2.angle) + p1.mass*g) / cos(p1.angle)
        
        p1.acc = ((-p1.tension*sin(p1.angle) + p2.tension*sin(p2.angle))**2 + (p1.tension*cos(p1.angle)-p1.tension*cos(p2.angle) - p1.mass*g)**2) ** 0.5 / p1.mass
        p2.acc = ((p2.tension*sin(p2.angle))**2) + ((p2.tension*cos(p2.angle) - p2.mass*g)**2)**0.5 / p2.mass

        # p1.angular_vel = (p1.tension*cos(p1.angle) - p2.tension*cos(p2.angle) - p1.mass*g) / p1.mass*p1.radius*sin(p1.angle)
        # p2.angular_vel = (p2.tension*cos(p2.angle) - p2.mass*g) / p2.mass*p2.radius*sin(p2.angle)
        
        
        for slider_id in sliders:
            sliders[slider_id].update()
            
        for ptc in particles:
            ptc.update()

        draw_surface()

if __name__ == '__main__':
    main()