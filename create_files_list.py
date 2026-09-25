import os

def create_files_list(directory):
    # Рекурсивно обходим все директории
    for root, dirs, files in os.walk(directory):
        # Имя файла, который мы создаем
        list_file_name = "files_list.txt"
        
        # Полный путь к файлу files_list.txt
        files_list_path = os.path.join(root, list_file_name)
        
        # Открываем файл для записи
        with open(files_list_path, 'w') as f:
            # Записываем имена всех файлов в текущей директории, исключая files_list.txt
            for file in files:
                if file != list_file_name:  # Исключаем файл files_list.txt
                    f.write(file + '\n')
        
        print(f"Создан файл: {files_list_path}")

if __name__ == "__main__":
    # Указываем директорию для обхода
    directory = input("Введите путь к директории: ")
    
    # Проверяем, существует ли директория
    if os.path.exists(directory):
        # Запускаем процесс
        create_files_list(directory)
        print("Обработка завершена.")
    else:
        print("Указанная директория не существует.")