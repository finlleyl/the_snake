from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс игрового объекта.
    
    Атрибуты:
        position (tuple): Позиция объекта на игровом поле (x, y).
        body_color (tuple): Цвет объекта (RGB).
    """
    def __init__(self, position=None, body_color=None):
        """
        Инициализирует объект.
        
        Args:
            position (tuple): Координаты позиции объекта.
            body_color (tuple): Цвет объекта.
        """
        if position is None:
            # По умолчанию — центральная точка поля.
            position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Отрисовывает объект на экране.
        Должен быть переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс Яблока, наследуемый от GameObject.
    
    Яблоко появляется в случайных координатах на поле.
    """

    def __init__(self):
        """
        Инициализирует яблоко с красным цветом, случайной позицией.
        """
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """
        Устанавливает случайную позицию для яблока в пределах игрового поля.
        """
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """
        Отрисовывает яблоко в одной ячейке заданного цвета.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс Змейки, наследуемый от GameObject.
    
    Змейка — это список координат (positions), каждый элемент — один сегмент тела.
    Изначально состоит из одного сегмента (головы).
    """

    def __init__(self):
        """
        Инициализирует змейку.
        
        Атрибуты:
            length (int): Длина змейки, изначально 1.
            positions (list): Список координат сегментов змейки.
            direction (tuple): Текущее направление движения (dx, dy).
            next_direction (tuple): Следующее направление движения.
            last (tuple): Позиция последнего сегмента перед движением.
        """
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.
        
        Returns:
            tuple: Координаты головы змейки.
        """
        return self.positions[0]

    def update_direction(self):
        """
        Применяет выбранное направление движения, если оно задано.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Двигает змейку на одну клетку в текущем направлении.
        
        Логика:
            1. Определяем новую позицию головы, прибавляя направление к текущим координатам.
            2. Обрабатываем "телепортацию" при выходе за границы поля.
            3. Проверяем столкновение с собой.
            4. Если столкновения нет, обновляем список позиций:
               - вставляем голову
               - при необходимости удаляем хвост (если длина не увеличилась)
        """
        cur = self.get_head_position()
        dx, dy = self.direction
        new_x = (cur[0] + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (cur[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_pos = (new_x, new_y)

        # Проверяем столкновение с собой (кроме самого первого сегмента)
        # Змейка слишком короткая, чтобы проверить первые два сегмента (при длине 1-2 — не страшно)
        if new_pos in self.positions[2:]:
            self.reset()
            return

        # Добавляем новую голову
        self.positions.insert(0, new_pos)

        # Если длина змейки больше фактического кол-ва сегментов, значит надо удалить хвост.
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.last = None
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self):
        """
        Отрисовывает змейку, её тело и голову.
        Затирает последний сегмент, если он исчез.
        """
        # Отрисовка тела (кроме головы)
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш и меняет направление движения змейки.

    Args:
        game_object (Snake): Объект змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            # Меняем направление, только если это допустимо (змейка не может двигаться назад)
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основная функция игры. Инициализирует объекты, запускает игровой цикл.
    """
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Обработка событий клавиатуры
        handle_keys(snake)
        # Обновление направления
        snake.update_direction()
        # Движение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Очистка экрана фоновым цветом, чтобы стереть следы
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка объектов
        apple.draw()
        snake.draw()

        # Обновление дисплея
        pygame.display.update()


if __name__ == '__main__':
    main()
