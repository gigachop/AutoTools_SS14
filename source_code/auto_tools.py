import os
from PIL import ImageGrab
import pyautogui
from pynput.mouse import Listener, Controller

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import random
import time
from pynput import mouse
import threading

# Глобальная переменная для блокировки
block_mouse_movement = False

# TEMPLATES_DIR = "D:\Pet_projects\Automatic_Chemistry_SS14\ll_img"


areas = {}

def on_move(x, y):
    """Функция будет вызвана при каждом движении мыши."""
    if block_mouse_movement:
        # Если движение мыши заблокировано, блокируем все действия мыши
        return False


def mouse_listener():
    with Listener(on_move=on_move) as listener:
        listener.join()

# Запуск слушателя мыши в отдельном потоке
listener_thread = threading.Thread(target=mouse_listener)
listener_thread.start()

def load_sub_templates():
    templates = {}
    main_template_path = os.path.join(TEMPLATES_DIR, 'main_template.jpg')
    main_template = cv2.imread(main_template_path, cv2.IMREAD_COLOR)
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith('.jpg') and filename != 'main_template.jpg':
            key = filename.split('.')[0]
            templates[key] = cv2.imread(os.path.join(TEMPLATES_DIR, filename), cv2.IMREAD_COLOR)
    return templates, main_template


def find_main_area_and_subareas(img, main_template, sub_templates):
    found_areas = {}

    # Распознавание большой области
    result = cv2.matchTemplate(img, main_template, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    h, w, _ = main_template.shape
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Вычисление масштаба
    scale_x = (bottom_right[0] - top_left[0]) / w
    scale_y = (bottom_right[1] - top_left[1]) / h

    # Обрезка изображения
    cropped_img = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    # Поиск маленьких областей
    for key, sub_template in sub_templates.items():
        resized_sub_template = cv2.resize(sub_template,
                                          (int(sub_template.shape[1] * scale_x), int(sub_template.shape[0] * scale_y)))
        result = cv2.matchTemplate(cropped_img, resized_sub_template, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        h, w, _ = resized_sub_template.shape
        top_left_sub = (max_loc[0] + top_left[0], max_loc[1] + top_left[1])
        bottom_right_sub = (top_left_sub[0] + w, top_left_sub[1] + h)
        center_sub = ((top_left_sub[0] + bottom_right_sub[0]) // 2, (top_left_sub[1] + bottom_right_sub[1]) // 2)
        found_areas[key] = (top_left_sub, bottom_right_sub, center_sub)

    return found_areas


def screenshot_and_scan():
    global areas
    sub_templates, main_template = load_sub_templates()  # Загрузка шаблонов
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    areas = find_main_area_and_subareas(screenshot_cv, main_template, sub_templates)  # Используем локальную переменную main_template
    area1_coords = areas.get('ftor')
    print(area1_coords)
    print(len(areas))


def recipe_bikardin90():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта "Бикардин 90"
    click_order = ['gr15', 'gr15', 'sahar', 'kislorod', 'gr30', 'yglerod', 'yglerod']

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши


def recipe_efedrine60():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта "эфедрин 60"
    click_order = ['gr1', 'gr1', 'azot', 'azot',
                   'gr5', 'yglerod',
                   'gr5', 'etanol', 'gr1', 'etanol', 'etanol', 'etanol',
                   'gr15', 'sahar',
                   'gr25', 'vodorod', 'gr1', 'vodorod']

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши


def recipe_hlorogidrat20():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта
    click_order = ['gr20', 'gr20', 'etanol',
                   'gr30', 'hlor', 'hlor']

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши


def MetalFoam_kislota_metal():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта
    click_order = ['gr1', 'gr1', 'sera', 'sera',
                   'kislorod', 'kislorod', 'kislorod', 'kislorod',
                   'gr5', 'ftor',
                   'kaliy',
                   'vodorod', 'gr1', 'vodorod', 'vodorod',
                   'gr20', 'zelezo', 'zelezo', 'zelezo']

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши


def MetalFoam_pena():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта
    click_order = ['gr10', 'gr10', 'vodorod',
                   'litiy']

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши

def Diloven90():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта
    click_order = ['gr30', 'gr30', 'azot',
                   'kaliy','kremniy']

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши

def Epekak40():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта
    click_order = ['gr25', 'gr25', 'azot',
                   'gr20','kaliy',
                   'gr15','vodorod']

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши

def kognizin5():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта
    click_order = ['gr1', 'gr1', 'yglerod',
                   'vodorod'
                   'kislorod','kislorod','kislorod'
                   ]

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши

def Narko_1foam98():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта
    click_order = ['gr1','gr1','vodorod','vodorod','vodorod','vodorod', 'sera','sera','sera','sera','kislorod','kislorod','kislorod','gr5','kislorod','gr20','yglerod','ftor','gr15', 'gr15', 'litiy','rtut', 'sahar'
                   ]

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши

def Paks45():
    global areas
    global block_mouse_movement
    block_mouse_movement = True  # блокировка движения мыши
    # Порядок кликов для рецепта
    click_order = ['gr1', 'gr1', 'azot','azot',
                    'kaliy','kaliy',
                   'gr5','vodorod', 'litiy','sahar','kremniy'
                   'gr1','kremniy','kremniy'
                   ]

    prev_item = None
    for item in click_order:
        coords = areas.get(item)
        if coords:
            _, _, (center_x, center_y) = coords
            enhanced_click(center_x, center_y)

            # Если текущий элемент совпадает с предыдущим, применяем меньшую задержку
            if prev_item == item:
                random_delay(0.19, 0.3)
            else:
                random_delay(0.65, 1.4)

            prev_item = item
    block_mouse_movement = False  # разблокировка движения мыши

def random_delay(min_seconds=0.5, max_seconds=1.1):
    """Приостанавливает выполнение программы на случайное количество секунд."""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


def enhanced_click(center_x, center_y, offset=5):
    """Осуществляет клик с небольшим случайным смещением относительно указанных координат."""
    x = center_x + random.randint(-offset, offset)
    y = center_y + random.randint(-offset, offset)
    pyautogui.click(x, y)


def choose_directory():
    global TEMPLATES_DIR
    new_dir = filedialog.askdirectory(title="Выберите папку с изображениями")
    if new_dir:  # Проверяем, что пользователь действительно выбрал директорию
        TEMPLATES_DIR = new_dir
    else:
        raise Exception("Папка с изображениями не выбрана. Программа не может продолжить работу без этой папки.")

def updated_main_v2():
    root = ThemedTk(theme="black")  # Применяем тему "Adapta" из библиотеки ttkthemes
    root.title("Мой макрос для крафта")
    root.geometry("740x450")

    # Кастомизация шрифтов
    custom_font = ("Arial", 12)
    group_font = ("Arial", 13)  # Размер шрифта для групп

    button_color = "#FFFFFF"  # Белый цвет для кнопок
    text_color = "#000000"  # Черный цвет для текста

    # Верхняя часть с кнопкой сканирования
    title_label = tk.Label(root, text="AutoTools SS14", font=("Arial", 15), fg=text_color)
    title_label.grid(row=0, column=0, sticky=tk.W)

    scan_button = tk.Button(root, text="Сканировать", command=screenshot_and_scan, font=custom_font, bg=button_color, fg=text_color)
    scan_button.grid(row=0, column=1, sticky=tk.W, padx=10)

     # Добавляем кнопку для выбора директории
    choose_dir_button = tk.Button(root, text="Выбрать папку с изображениями", command=choose_directory, font=custom_font, bg=button_color, fg=text_color)
    choose_dir_button.grid(row=0, column=2, sticky=tk.W, padx=10)

    # Первая группа рецептов
    group1_label = tk.Label(root, text="Медикаменты", font=group_font, fg=text_color)
    group1_label.grid(row=1, column=0, pady=10, sticky=tk.W, padx=5)
    recipe1_btn = tk.Button(root, text="Бикардин 90", command=recipe_bikardin90, font=custom_font, bg=button_color, fg=text_color)
    recipe1_btn.grid(row=2, column=0, pady=10, sticky=tk.W, padx=5)
    recipe2_btn = tk.Button(root, text="Эфедрин 60 + 5 топлива", command=recipe_efedrine60, font=custom_font, bg=button_color, fg=text_color)
    recipe2_btn.grid(row=3, column=0, pady=10, sticky=tk.W, padx=5)
    recipe3_btn = tk.Button(root, text="Хлорогидрат 20 + 20 воды", command=recipe_hlorogidrat20, font=custom_font, bg=button_color, fg=text_color)
    recipe3_btn.grid(row=4, column=0, pady=10, sticky=tk.W, padx=5)
    new_recipe_btn = tk.Button(root, text="Пакс 45 + 20 воды", command=Paks45, font=custom_font, bg=button_color, fg=text_color)
    new_recipe_btn.grid(row=5, column=0, pady=10, sticky=tk.W, padx=5)

    # Добавление трех новых кнопок в первую группу на второй столбец
    new_button1 = tk.Button(root, text="Диловен 90", command=Diloven90, font=custom_font, bg=button_color, fg=text_color)
    new_button1.grid(row=2, column=1, pady=10, sticky=tk.W, padx=5)
    new_button2 = tk.Button(root, text="Ипекак 40", command=Epekak40, font=custom_font, bg=button_color, fg=text_color)
    new_button2.grid(row=3, column=1, pady=10, sticky=tk.W, padx=5)
    new_button3 = tk.Button(root, text="Когнизин 5+ 3 алоэ+ 3 стеллибинина+ 4 топлива+ 5 карпотоксина", command=kognizin5, font=custom_font, bg=button_color, fg=text_color)
    new_button3.grid(row=4, column=1, columnspan=2, pady=10, sticky=tk.W, padx=5)

    # Вторая группа рецептов
    group2_label = tk.Label(root, text="Железная граната", font=group_font, fg=text_color)
    group2_label.grid(row=6, column=0, pady=10, sticky=tk.W, padx=5)  # Обновленное значение row
    recipe4_btn = tk.Button(root, text="1 мензурка 81", command=MetalFoam_kislota_metal, font=custom_font,
                            bg=button_color, fg=text_color)
    recipe4_btn.grid(row=7, column=0, pady=10, sticky=tk.W, padx=5)  # Обновленное значение row
    recipe4_2btn = tk.Button(root, text="2 мензурка 20", command=MetalFoam_pena, font=custom_font, bg=button_color,
                            fg=text_color)
    recipe4_2btn.grid(row=8, column=0, pady=10, sticky=tk.W, padx=5)  # Обновленное значение row

    # Третья группа рецептов
    group3_label = tk.Label(root, text="Граната с наркотической пеной", font=group_font, fg=text_color)
    group3_label.grid(row=6, column=2, pady=10, sticky=tk.W, padx=5)  # Обновленное значение row
    recipe5_btn = tk.Button(root, text="1 мензурка 97", command=Narko_1foam98, font=custom_font, bg=button_color,
                            fg=text_color)
    recipe5_btn.grid(row=7, column=2, pady=10, sticky=tk.W, padx=5)  # Обновленное значение row
    recipe6_label = tk.Label(root, text="2 мензурка 50 воды", font=custom_font, fg=text_color, bg=button_color)
    recipe6_label.grid(row=8, column=2, pady=10, sticky=tk.W, padx=5)  # Обновленное значение row


    root.mainloop()

if __name__ == "__main__":
    choose_directory()  # Сразу вызываем функцию выбора папки при запуске программы
    updated_main_v2()