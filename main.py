import pygame

# define a main function


def main():
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("First Game")

    x = 50
    y = 50
    width = 40
    height = 40
    vel = 5

    run = True

    is_jump = False
    base_jump_count = 7
    jump_count = base_jump_count

    while run:
        pygame.time.delay(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and x > vel: 
            x -= vel

        if keys[pygame.K_RIGHT] and x < 500 - vel - width:  
            x += vel
            
        if not(is_jump): 
            if keys[pygame.K_UP] and y > vel:
                y -= vel

            if keys[pygame.K_DOWN] and y < 500 - height - vel:
                y += vel

            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -base_jump_count:
                y -= (jump_count * abs(jump_count)) * 0.5
                jump_count -= 1
            else: 
                jump_count = base_jump_count
                is_jump = False
        
        win.fill((0,0,0))
        pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
        pygame.display.update() 

    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
