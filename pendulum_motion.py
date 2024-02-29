import pygame

pygame.init()

width, height = 300, 300
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("pendulum motion")
clock = pygame.time.Clock()

# COLOURS
BG_COLOUR = (255, 250, 220)

def draw_surface() -> None:
    
    win.fill(BG_COLOUR)
    pygame.display.update()
    
def main() -> None:
    
    while True:
        
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        draw_surface()

if __name__ == '__main__':
    main()