import pygame
import sys
from classes.board import Board
from classes.menu import Menu
from classes.button import Button


def main():
    # Инициализация Pygame
    pygame.init()

    # Настройки экрана
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main menu")

    # Загрузка фонового изображения
    background = pygame.image.load("images/menu.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Создание меню
    menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Основной цикл
    running = True
    while running:
        # Отрисовка фона
        screen.blit(background, (0, 0))

        # Проверка наведения на кнопки
        mouse_pos = pygame.mouse.get_pos()
        for button in menu.buttons:
            button.check_hover(mouse_pos)

        # Отрисовка меню
        menu.draw(screen)

        # Обновление экрана
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Обработка событий в меню
            result = menu.handle_event(event)
            if result == "Игра против компьютера":
                print("Запуск игры против компьютера")
                select_timer(screen, background, SCREEN_WIDTH, SCREEN_HEIGHT)
            elif result == "Игра против человека":
                print("Запуск игры против человека")
                select_timer(screen, background, SCREEN_WIDTH, SCREEN_HEIGHT)
            elif result == "Выход":
                running = False

    # Завершение работы
    pygame.quit()
    sys.exit()


def select_timer(screen, background, screen_width, screen_height):
    """
    Меню выбора таймера.
    :param screen: Экран, на котором отрисовывается меню.
    :param background: Фоновое изображение.
    :param screen_width: Ширина экрана.
    :param screen_height: Высота экрана.
    """
    pygame.display.set_caption("Select timer")
    # Создание кнопок для выбора таймера
    font = pygame.font.Font(None, 36)
    buttons = [
        Button(200, 200, 50, "5 минут", font, (0, 128, 255), (0, 255, 128), (255, 255, 255), screen_width),
        Button(300, 200, 50, "10 минут", font, (0, 128, 255), (0, 255, 128), (255, 255, 255), screen_width),
        Button(400, 200, 50, "15 минут", font, (0, 128, 255), (0, 255, 128), (255, 255, 255), screen_width),
    ]

    # Основной цикл для меню выбора таймера
    running = True
    while running:
        # Отрисовка фона
        screen.blit(background, (0, 0))

        # Проверка наведения на кнопки
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)

        # Отрисовка кнопок
        for button in buttons:
            button.draw(screen)

        # Обновление экрана
        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Обработка нажатий на кнопки
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        print(f"Выбрано время: {button.text}")
                        # Запуск доски
                        board = Board(screen_width, screen_height)
                        board.run()
                        running = False


# Запуск программы
if __name__ == "__main__":
    main()
