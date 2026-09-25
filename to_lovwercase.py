import os

def rename_to_lowercase(directory):
    # Рекурсивно обходим все файлы и подпапки в директории
    for root, dirs, files in os.walk(directory, topdown=False):
        # Переименовываем файлы
        for file in files:
            # Получаем текущий путь к файлу
            current_file_path = os.path.join(root, file)
            
            # Преобразуем имя файла в lowercase
            new_file_name = file.lower()
            new_file_path = os.path.join(root, new_file_name)
            
            # Переименовываем файл, если имя изменилось
            if new_file_name != file:
                os.rename(current_file_path, new_file_path)
                print(f"Переименован файл: {current_file_path} -> {new_file_path}")
        
        # Переименовываем подпапки
        for dir in dirs:
            # Получаем текущий путь к подпапке
            current_dir_path = os.path.join(root, dir)
            
            # Преобразуем имя подпапки в lowercase
            new_dir_name = dir.lower()
            new_dir_path = os.path.join(root, new_dir_name)
            
            # Переименовываем подпапку, если имя изменилось
            if new_dir_name != dir:
                os.rename(current_dir_path, new_dir_path)
                print(f"Переименована папка: {current_dir_path} -> {new_dir_path}")

if __name__ == "__main__":
    # Указываем директорию для обхода
    directory = input("Введите путь к директории: ")
    
    # Проверяем, существует ли директория
    if os.path.exists(directory):
        # Запускаем процесс переименования
        rename_to_lowercase(directory)
        print("Переименование завершено.")
    else:
        print("Указанная директория не существует.")