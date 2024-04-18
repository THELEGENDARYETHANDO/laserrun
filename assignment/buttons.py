import pygame

white = (255, 255, 255)

#buttons
def text(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()

def button(message, x, y, w, h, inactive_colour, active_colour, action, plane):
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()

    #check if mouse is hovering over buttons and triggers the action if the mouse is clicked
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(plane, active_colour, (x, y, w, h))
        if click [0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(plane, inactive_colour, (x, y, w, h))

    #makes the text written on the button centered
    font = pygame.font.SysFont(None, 30)
    text_surf, text_rect = text(message, font)
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    plane.blit(text_surf, text_rect)