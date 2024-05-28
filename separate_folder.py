import os
import shutil


def split_folder(source_folder, target_folders):
    # Проверяем наличие исходной папки
    if not os.path.exists(source_folder):
        print(f"Папка {source_folder} не существует.")
        return

    # Создаем целевые папки, если они не существуют
    for folder in target_folders:
        os.makedirs(folder, exist_ok=True)

    # Получаем список файлов в исходной папке
    files = os.listdir(source_folder)
    num_files = len(files)

    # Распределяем файлы по целевым папкам
    for i, file in enumerate(files):
        source_file_path = os.path.join(source_folder, file)
        target_folder = target_folders[i % len(target_folders)]
        target_file_path = os.path.join(target_folder, file)
        shutil.move(source_file_path, target_file_path)
        print(f"Файл {file} перемещен в папку {target_folder}.")

    print("Распределение завершено.")


# Указываем исходную папку и целевые папки
source_folder = 'imgs'
target_folders = ['imgs1', 'imgs2', 'imgs3', 'imgs4', 'imgs5', 'imgs6', 'imgs7', 'imgs8', 'imgs9', 'imgs10']

# Вызываем функцию для распределения файлов
split_folder(source_folder, target_folders)
