import os
import re

def extract_handlers(s_file_path):
    handlers = []
    with open(s_file_path, 'r') as s_file:
        for line in s_file:
            # Ищем строки, содержащие объявления обработчиков прерываний
            match = re.match(r'\.word\s+(\w+)', line.strip())
            if match:
                handler = match.group(1)
                handlers.append(handler)
    return handlers

def generate_c_file(handlers, c_file_path):
    with open(c_file_path, 'w') as c_file:
        # Записываем стандартный заголовок
        c_file.write("#include <stdint.h>\n\n")
        c_file.write("void Default_Handler(void) {\n")
        c_file.write("	while(1) {}\n")
        c_file.write("}\n\n")
        
        c_file.write("extern uint32_t __end_stack;\n\n")

        # Генерируем weak-алиасы для обработчиков, исключая __end_stack и 0
        for handler in handlers:
            if handler != "__end_stack" and handler != "0" and handler != "_estack":
                c_file.write(f"void {handler}(void)						__attribute__ ((weak, alias(\"Default_Handler\")));\n")
        
        # Генерируем таблицу векторов прерываний
        c_file.write("\n__attribute__ ((section(\".isr_vector\")))\n")
        c_file.write("uint32_t vector_table[] = {\n")
        
        # Первый элемент — __end_stack
        if handlers and ( handlers[0] == "__end_stack" or handlers[0] == "_estack"):
            c_file.write(f"	(uint32_t) &__end_stack,\n")
            handlers = handlers[1:]  # Убираем __end_stack из списка обработчиков
        
        # Остальные элементы таблицы
        for handler in handlers:
            if handler == "0":
                c_file.write("	(uint32_t) 0,\n")
            else:
                c_file.write(f"	(uint32_t) {handler},\n")
        
        c_file.write("};\n")

def process_directory(src_dir, dst_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.s'):
                s_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, src_dir)
                c_file_name = file.replace('.s', '.c')
                c_file_path = os.path.join(dst_dir, relative_path, c_file_name)
                
                # Создаем директорию, если она не существует
                os.makedirs(os.path.dirname(c_file_path), exist_ok=True)
                
                # Извлекаем обработчики и генерируем .c файл
                handlers = extract_handlers(s_file_path)
                generate_c_file(handlers, c_file_path)
                print(f"Converted {s_file_path} to {c_file_path}")

if __name__ == "__main__":
    src_directory = input("Введите путь к исходной папке: ")
    dst_directory = input("Введите путь к папке назначения: ")
    
    if not os.path.exists(src_directory):
        print("Исходная папка не существует.")
    else:
        process_directory(src_directory, dst_directory)
        print("Конвертация завершена.")