import pygame
import sys
from classes.board import Board
from classes.menu import Menu
from classes.button import Button

def main():
    # Initializes Pygame
    pygame.init()

    # Screen Settings
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 840
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main menu")

    # Loading a Background Image
    background = pygame.image.load("images/menu.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Creating a menu
    menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Main Loop
    running = True
    while running:
        # Background Rendering
        screen.blit(background, (0, 0))

        # Checking button hover
        mouse_pos = pygame.mouse.get_pos()
        for button in menu.buttons:
            button.check_hover(mouse_pos)

        # Menu Rendering
        menu.draw(screen)

        # Screen Refresh
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handling Menu Events
            result = menu.handle_event(event)
            if result == "Play against the computer.":
                select_timer(screen, background, SCREEN_WIDTH, SCREEN_HEIGHT, mode="human_vs_ai")
            elif result == "Play against a person":
                select_timer(screen, background, SCREEN_WIDTH, SCREEN_HEIGHT, mode="human_vs_human")
            elif result == "Exit":
                running = False

    # Exit
    pygame.quit()
    sys.exit()


def select_timer(screen, background, screen_width, screen_height, mode="human_vs_human"):
    """
    Timer selection menu.
    :param screen: The screen on which the menu is drawn.
    :param background: The background image.
    :param screen_width: The width of the screen.
    :param screen_height: The height of the screen.
    :param mode: The game mode ("human_vs_human" or "human_vs_ai").
    """
    pygame.display.set_caption("Select timer")
    # Creation of buttons to select a timer
    font = pygame.font.Font(None, 36)
    buttons = [
        Button(200, 200, 50, "5 minutes", font, (0, 128, 255), (0, 255, 128), (255, 255, 255), screen_width),
        Button(300, 200, 50, "10 minutes", font, (0, 128, 255), (0, 255, 128), (255, 255, 255), screen_width),
        Button(400, 200, 50, "15 minutes", font, (0, 128, 255), (0, 255, 128), (255, 255, 255), screen_width),
    ]

    # Main loop for timer selection menu
    running = True
    while running:
        # Drawing the background
        screen.blit(background, (0, 0))

        # Checking hover over buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)

        # Drawing buttons
        for button in buttons:
            button.draw(screen)

        # Screen refresh
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Handling button clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        # Determining the chosen time
                        if button.text == "5 minutes":
                            timer_minutes = 5
                        elif button.text == "10 minutes":
                            timer_minutes = 10
                        elif button.text == "15 minutes":
                            timer_minutes = 15

                        # Start the board with the selected timer
                        board = Board(screen_width, screen_height, mode=mode, timer_minutes=timer_minutes)
                        board.run()
                        running = False


# Launching the program
if __name__ == "__main__":
    main()
