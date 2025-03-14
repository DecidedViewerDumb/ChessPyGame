import pygame
import sys
from classes.board import Board
from classes.menu import Menu
from classes.button import Button


def main():
    # Инициализация Pygame
    pygame.init()

    # Настройки экрана
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 840
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
                select_timer(screen, background, SCREEN_WIDTH, SCREEN_HEIGHT, mode="human_vs_ai")
            elif result == "Игра против человека":
                select_timer(screen, background, SCREEN_WIDTH, SCREEN_HEIGHT, mode="human_vs_human")
            elif result == "Выход":
                running = False

    # Завершение работы
    pygame.quit()
    sys.exit()


def select_timer(screen, background, screen_width, screen_height, mode="human_vs_human"):
    """
    Меню выбора таймера.
    :param screen: Экран, на котором отрисовывается меню.
    :param background: Фоновое изображение.
    :param screen_width: Ширина экрана.
    :param screen_height: Высота экрана.
    :param mode: Режим игры ("human_vs_human" или "human_vs_ai").
    """
    pygame.display.set_caption("Select timer")
    # Создание кнопок для выбора таймера
    font = pygame.font.Font(None, 36)
    vertical_spacing = 70  # Расстояние между кнопками
    start_y = 300  # Начальная позиция по Y
    buttons = [
        Button(start_y, "5 минут", font, (0, 128, 255), (0, 255, 128), (255, 255, 255), screen_width),
        Button(start_y + vertical_spacing, "10 минут", font, (0, 128, 255), (0, 255, 128), (255, 255, 255), screen_width),
        Button(start_y + vertical_spacing * 2, "15 минут", font, (0, 128, 255), (0, 255, 128), (255, 255, 255), screen_width),
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
                        # Определяем выбранное время
                        if button.text == "5 минут":
                            timer_minutes = 5
                        elif button.text == "10 минут":
                            timer_minutes = 10
                        elif button.text == "15 минут":
                            timer_minutes = 15

                        # Запуск доски с выбранным таймером
                        board = Board(screen_width, screen_height, mode=mode, timer_minutes=timer_minutes)
                        board.run()
                        running = False


# Запуск программы
if __name__ == "__main__":
    main()
