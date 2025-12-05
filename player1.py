import pygame, random
import socket
import threading
import time

pygame.init()

screen_width = 2240
screen_height = 1260

def homescreen():
    class Button():
        def __init__(self, x, y, image, scale):
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False

        def draw(self, surface):
            action = False
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            surface.blit(self.image, (self.rect.x, self.rect.y))
            return action
    
    screen = pygame.display.set_mode((750, 500))
    pygame.display.set_caption('BallSim2d Deluxe Edition')

    start_img = pygame.image.load('/Users/aarnavdhir/Downloads/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('/Users/aarnavdhir/Downloads/exit_btn.png').convert_alpha()
    display_img = pygame.image.load('/Users/aarnavdhir/Downloads/Screenshots/Screenshot 2025-11-26 at 7.14.26 PM.png')
    
    start_button = Button(100, 200, start_img, 0.8)
    exit_button = Button(450, 200, exit_img, 0.8)
    screen.blit(display_img, (100, 200))
    
    run = True
    while run:
        screen.fill((202, 228, 241))

        if start_button.draw(screen):
            gamescreen()
        if exit_button.draw(screen):
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

def gamescreen():
    soccerball = pygame.image.load('/Users/aarnavdhir/Downloads/soccer.png')
    soccerball = pygame.transform.scale(soccerball, (60, 60))
    pygame.display.set_caption("BallSim2D Deluxe Edition")

    ball_radius = 30
    ball_vel_x = 0
    ball_vel_y = 0
    DRAG = 0.90
    IMPULSE_STRENGTH = 10
    running = True

    inputed = "red"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.1.70", 7900)) 
    server.listen()

    client_socket = None

    def wait_for_client():
        nonlocal client_socket
        print("Waiting for connection...")
        client_socket, addr = server.accept()
        print("Connected:", addr)
        client_socket.setblocking(False)

    threading.Thread(target=wait_for_client, daemon=True).start()

    screen_width = 2240
    screen_height = 1260
    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    pos = pygame.Vector2(screen_width / 2, screen_height / 2)
    pos2 = pygame.Vector2(screen_width / 3, screen_height / 2)
    start_x_top_left = 1190
    start_y_top_left = 630
    soccerpos = pygame.Vector2(start_x_top_left + ball_radius, start_y_top_left + ball_radius)

    color_list = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown"]
    color1 = "red"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if client_socket is not None:
            try:
                data = client_socket.recv(1024)
                if data:
                    inputed = data.decode()
            except BlockingIOError:
                pass
            except OSError:
                pass

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pos.y -= 10
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            pos.x -= 10
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            pos.y += 10
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            pos.x += 10

        if inputed == "w_start":
            pos2.y -= 10
        elif inputed == "w_stop":
            pos2.y += 0
        if inputed == "a_start":
            pos2.x -= 10
        elif inputed == "a_stop":
            pos2.x += 0
        if inputed == "s_start":
            pos2.y += 10
        elif inputed == "s_stop":
            pos2.y += 0
        if inputed == "d_start":
            pos2.x += 10
        elif inputed == "d_stop":
            pos2.x += 0

        screen.fill("white")
    
        if pos.distance_to(soccerpos) <= 130 or pos2.distance_to(soccerpos) <= 130:
            IMPULSE_SPEED = 25
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                ball_vel_y = -IMPULSE_SPEED 
                ball_vel_x = 0
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                ball_vel_x = -IMPULSE_SPEED
                ball_vel_y = 0
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                ball_vel_y = IMPULSE_SPEED
                ball_vel_x = 0
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                ball_vel_x = IMPULSE_SPEED
                ball_vel_y = 0
            elif inputed == "w_start":
                ball_vel_y = -IMPULSE_SPEED 
                ball_vel_x = 0
            elif inputed == "a_start":
                ball_vel_x = -IMPULSE_SPEED
                ball_vel_y = 0
            elif inputed == "s_start":
                ball_vel_y = IMPULSE_SPEED
                ball_vel_x = 0
            elif inputed == "d_start":
                ball_vel_x = IMPULSE_SPEED
                ball_vel_y = 0

        if soccerpos.x + ball_radius >= screen_width:
            soccerpos.x = screen_width - ball_radius
        if soccerpos.x - ball_radius <= 0:
            soccerpos.x = ball_radius
        if soccerpos.y + ball_radius >= screen_height:
            soccerpos.y = screen_height - ball_radius
        if soccerpos.y - ball_radius <= 0:
            soccerpos.y = ball_radius 

        ball_vel_x *= DRAG
        ball_vel_y *= DRAG
        soccerpos.x += ball_vel_x
        soccerpos.y += ball_vel_y
        if abs(ball_vel_x) < 0.1: ball_vel_x = 0
        if abs(ball_vel_y) < 0.1: ball_vel_y = 0

        pygame.draw.circle(screen, color1, pos, 100)
        pygame.draw.circle(screen, "blue", pos2, 100)

        screen.blit(soccerball, (soccerpos.x - ball_radius, soccerpos.y - ball_radius))

        clock.tick(80)
        pygame.display.flip()

    pygame.quit()

homescreen()
