import pygame # type: ignore
import sys

# Инициализация Pygame и ввода текста
pygame.init()

# Константы экрана
WIDTH, HEIGHT = 1100, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Code Academy - v2.0")

# Цветовая палитра
BG_COLOR = (241, 245, 249)        # Светлый фон
CARD_COLOR = (255, 255, 255)      # Панели
TEXT_MAIN = (15, 23, 42)          # Тёмный текст
TEXT_MUTED = (100, 116, 139)      # Серый текст
PRIMARY = (37, 99, 235)           # Синий для кнопок
PRIMARY_HOVER = (29, 78, 216)
SUCCESS = (22, 163, 74)           # Зелёный успех
ERROR = (220, 38, 38)             # Красный крэш
PROGRESS_BG = (226, 232, 240)
EDITOR_BG = (15, 23, 42)          # Тёмная тема для редактора кода
SIDEBAR_BG = (248, 250, 252)

# Шрифты
FONT_TITLE = pygame.font.SysFont("Arial", 22, bold=True)
FONT_TEXT = pygame.font.SysFont("Arial", 16)
FONT_BTN = pygame.font.SysFont("Arial", 14, bold=True)
FONT_CODE = pygame.font.SysFont("Courier New", 16, bold=True) # Моноширинный для кода

# --- ЛОГИЧЕСКИЕ КЛАССЫ ПРОГРАММЫ ---

class User:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.xp_needed = 100

    def add_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_needed:
            self.xp -= self.xp_needed
            self.level += 1
            self.xp_needed = int(self.xp_needed * 1.5)

class Lesson:
    def __init__(self, id, title, desc, hint, expected_code):
        self.id = id
        self.title = title
        self.desc = desc
        self.hint = hint
        self.expected_code = expected_code.strip()

# --- БАЗА ДАННЫХ НА 20 УРОКОВ  ---
user = User()
lessons = [
    Lesson(1, "Вывод текста", "Выведите на экран строку 'Hello'.", "Справка: функция print(). Наводка: не забудьте кавычки для строки.", "print('Hello')"),
    Lesson(2, "Переменные", "Создайте переменную x и присвойте ей значение 10.", "Справка: оператор '='. Наводка: имя переменной пишется слева.", "x = 10"),
    Lesson(3, "Типы данных", "Создайте строковую переменную name со значением 'Zuzya'.", "Справка: строки пишутся в кавычках. Наводка: name = '...' ", "name = 'Zuzya'"),
    Lesson(4, "Математика", "Создайте переменную res равную 5 умножить на 2.", "Справка: оператор умножения — '*'. Наводка: res = 5 ... 2", "res = 5 * 2"),
    Lesson(5, "Списки", "Создайте пустой список с именем иконки 'items'.", "Справка: списки создаются через квадратные скобки []. Наводка: items = ...", "items = []"),
    Lesson(6, "Добавление в список", "Добавьте число 7 в существующий список 'items'.", "Справка: метод .append(). Наводка: items.append(...)", "items.append(7)"),
    Lesson(7, "Условия", "Напишите начало условия: если x больше 5.", "Справка: оператор if и двоеточие в конце. Наводка: if x > 5:", "if x > 5:"),
    Lesson(8, "Проверка равенства", "Проверьте условие: если переменная status равна 'ready'.", "Справка: сравнение — это двойное равно '=='. Наводка: if status == ... :", "if status == 'ready':"),
    Lesson(9, "Иначе", "Напишите блок 'иначе' для ветвления условий.", "Справка: ключевое слово else с двоеточием.", "else:"),
    Lesson(10, "Цикл While", "Напишите начало цикла пока x меньше 100.", "Справка: оператор while. Наводка: while x :", "while x < 100:"),
    Lesson(11, "Цикл For", "Запустите цикл for для переменной i в диапазоне от 0 до 4 включительно.", "Справка: функция range(N) генерирует N чисел. Наводка: for i in range(_):", "for i in range(5):"),
    Lesson(12, "Функции", "Объявите функцию с именем 'start_game' без аргументов.", "Справка: создание функции через 'def'. Наводка: def имя():", "def start_game():"),
    Lesson(13, "Возврат значения", "Верните число 42 из функции.", "Справка: оператор return. Наводка: return ...", "return 42"),
    Lesson(14, "Длина списка", "Найдите длину списка 'items' с помощью встроенной функции.", "Справка: функция len().", "len(items)"),
    Lesson(15, "Словари", "Создайте пустой словарь с именем 'data'.", "Справка: словари создаются через фигурные скобки {}. Наводка: data = ...", "data = {}"),
    Lesson(16, "Словарь: Ключ", "Добавьте в словарь data ключ 'id' со значением 1.", "Справка: обращение по ключу data['ключ']. Наводка: data['имя_ключа'] = 1", "data['id'] = 1"),
    Lesson(17, "Ввод данных", "Считайте текст от пользователя в переменную 'inp'.", "Справка: функция input(). Наводка: имя_переменной = имя_функции_с_аргументом", "inp = input()"),
    Lesson(18, "Преобразование типов", "Преобразуйте строку '5' в целое число.", "Справка: функция int(). Наводка: int('5')", "int('5')"),
    Lesson(19, "Импорт модулей", "Импортируйте встроенную библиотеку для работы со временем.", "Справка: оператор import. Наводка: import time", "import time"),
    Lesson(20, "Классы", "Объявите пустой класс с именем 'Bot'.", "Справка: создание через 'class' и заглушку 'pass'. Наводка: class Bot:\n    pass", "class Bot:")
]

current_lesson_idx = 0
user_code_input = ""  # Здесь хранится текст, который пишет пользователь
status_message = "Введите код и нажмите Проверить"
status_color = TEXT_MUTED
show_hint = False

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ИНТЕРФЕЙСА ---

def draw_text(text, font, color, x, y, max_width=None):
    lines = text.split('\n')
    current_y = y
    for line in lines:
        words = line.split(' ')
        current_x = x
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            test_width, _ = font.size(test_line)
            if max_width and test_width > max_width:
                word_surface = font.render(current_line, True, color)
                screen.blit(word_surface, (current_x, current_y))
                current_y += font.get_linesize()
                current_line = word + " "
            else:
                current_line = test_line
        if current_line:
            word_surface = font.render(current_line, True, color)
            screen.blit(word_surface, (current_x, current_y))
            current_y += font.get_linesize()

def draw_button(rect, text, is_hovered, color_base=PRIMARY, color_hover=PRIMARY_HOVER):
    color = color_hover if is_hovered else color_base
    pygame.draw.rect(screen, color, rect, border_radius=6)
    btn_text = FONT_BTN.render(text, True, (255, 255, 255))
    text_rect = btn_text.get_rect(center=rect.center)
    screen.blit(btn_text, text_rect)

# --- ГЛАВНЫЙ ЦИКЛ ---
clock = pygame.time.Clock()
pygame.key.set_repeat(300, 50)  # Поддержка зажатия клавиш для стирания

while True:
    mouse_pos = pygame.mouse.get_pos()
    cur_lesson = lessons[current_lesson_idx]

    # Координаты кнопок
    btn_check_rect = pygame.Rect(320, 520, 160, 40)
    btn_hint_rect = pygame.Rect(500, 520, 160, 40)
    btn_next_rect = pygame.Rect(680, 520, 160, 40)

    # Определение наведения
    hover_check = btn_check_rect.collidepoint(mouse_pos)
    hover_hint = btn_hint_rect.collidepoint(mouse_pos)
    hover_next = btn_next_rect.collidepoint(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # ОБРАБОТКА ВВОДА С КЛАВИАТУРЫ В РЕДАКТОР
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_code_input = user_code_input[:-1]  # Стирание символа
            elif event.key == pygame.K_RETURN:
                user_code_input += "\n"  # Перенос строки (если нужен)
            elif event.key == pygame.K_TAB:
                user_code_input += "    "  # Табуляция (4 пробела)
            else:
                # Добавление обычных печатных символов
                if event.unicode:
                    user_code_input += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Клик: Проверить код
            if hover_check:
                # Заменяем двойные кавычки на одинарные для гибкой проверки
                normalized_user_code = user_code_input.strip().replace('"', "'")
                if normalized_user_code == cur_lesson.expected_code:

                    status_message = "🟢 Успех! Код скомпилирован без ошибок синтаксиса."
                    status_color = SUCCESS
                    user.add_xp(35)
                else:
                    status_message = f"🔴 Ошибка компиляции! Проверьте синтаксис. Ожидалось: {len(cur_lesson.expected_code)} симв."
                    status_color = ERROR
            
            # Клик: Подсказка
            if hover_hint:
                show_hint = not show_hint

            # Клик: Следующий урок
            if hover_next:
                current_lesson_idx = (current_lesson_idx + 1) % len(lessons)
                user_code_input = ""  # Очищаем поле ввода под новый урок
                status_message = "Введите код и нажмите Проверить"
                status_color = TEXT_MUTED
                show_hint = False

            # КЛИКИ ПО БОКОВОЙ ПАНЕЛИ НАВИГАЦИИ (Выбор любого из 20 уроков)
            for i in range(len(lessons)):
                sidebar_item_rect = pygame.Rect(10, 140 + i * 27, 260, 24)
                if sidebar_item_rect.collidepoint(mouse_pos):
                    current_lesson_idx = i
                    user_code_input = ""
                    status_message = "Введите код и нажмите Проверить"
                    status_color = TEXT_MUTED
                    show_hint = False

    # Отрисовка бэкграунда
    screen.fill(BG_COLOR)

    # --- ВЕРХНЯЯ ПАНЕЛЬ: ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ---
    pygame.draw.rect(screen, CARD_COLOR, (15, 20, 1070, 85), border_radius=8)
    draw_text(f"Уровень: {user.level}", FONT_TITLE, TEXT_MAIN, 40, 35)
    draw_text(f"Набранный опыт: {user.xp} / {user.xp_needed} XP", FONT_TEXT, TEXT_MUTED, 40, 70)
    
    # Графический XP Bar
    pygame.draw.rect(screen, PROGRESS_BG, (350, 50, 700, 16), border_radius=8)
    xp_ratio = min(user.xp / user.xp_needed, 1.0)
    if xp_ratio > 0:
        pygame.draw.rect(screen, PRIMARY, (350, 50, int(700 * xp_ratio), 16), border_radius=8)

    # --- ЛЕВАЯ ПАНЕЛЬ: СПИСОК ВСЕХ 20 КУРСОВ ---
    pygame.draw.rect(screen, SIDEBAR_BG, (15, 120, 280, 580), border_radius=8)
    draw_text("Доступные уроки (20):", FONT_TITLE, TEXT_MAIN, 25, 130)
    for i, les in enumerate(lessons):
    # Подсветка текущего выбранного урока в списке
        item_bg = (219, 234, 254) if i == current_lesson_idx else SIDEBAR_BG
    item_rect = pygame.Rect(20, 165 + i * 26, 260, 24)
    pygame.draw.rect(screen, item_bg, item_rect, border_radius=4)
    text_color = PRIMARY if i == current_lesson_idx else TEXT_MAIN
    draw_text(f"{les.id}. {les.title}", FONT_TEXT, text_color, 30, 167 + i * 26)
    # --- ЦЕНТРАЛЬНОЕ ОКНО УРОКА ---
    pygame.draw.rect(screen, CARD_COLOR, (310, 120, 775, 580), border_radius=8)
    draw_text(f"Урок №{cur_lesson.id}: {cur_lesson.title}", FONT_TITLE, TEXT_MAIN, 330, 140)
    draw_text(cur_lesson.desc, FONT_TEXT, TEXT_MUTED, 330, 180, max_width=730)
    # ИНТЕРАКТИВНЫЙ РЕДАКТОР КОДА (Тёмное поле)
    pygame.draw.rect(screen, EDITOR_BG, (320, 240, 750, 180), border_radius=6)
    # Рендеринг текста, который пишет пользователь с клавиатуры
    if user_code_input == "":
        draw_text("Начните писать код здесь...", FONT_CODE, (71, 85, 105), 340, 260)
    else:
        draw_text(user_code_input, FONT_CODE, (56, 189, 248), 340, 260)
    # --- ЭЛЕМЕНТЫ УПРАВЛЕНИЯ ---
    draw_button(btn_check_rect, "Проверить код", hover_check)
    draw_button(btn_hint_rect, "Умная подсказка", hover_hint, color_base=(100, 116, 139), color_hover=(71, 85, 105))
    draw_button(btn_next_rect, "Следующий урок", hover_next)
    # Вывод статуса проверки компиляции
    draw_text(status_message, FONT_TEXT, status_color, 330, 450)
    # ОКНО УМНОЙ ПОДСКАЗКИ (Появляется по клику)
    if show_hint:
        pygame.draw.rect(screen, (254, 243, 199), (320, 580, 750, 100), border_radius=6) # Жёлтое поле
    pygame.draw.rect(screen, (245, 158, 11), (320, 580, 750, 100), width=2, border_radius=6)
    draw_text("💡 СПРАВКА И НАВОДКА ДЛЯ ИНИЦИАЛИЗАЦИИ:", FONT_BTN, (180, 83, 9), 340, 595)
    draw_text(cur_lesson.hint, FONT_TEXT, (120, 53, 4), 340, 625, max_width=710)
    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)