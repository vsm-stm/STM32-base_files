import os

def replace_in_c_files(root_dir, old_str="__end_stack", new_str="_estack"):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".c"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if old_str in content:
                    new_content = content.replace(old_str, new_str)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ Replaced in: {file_path}")

if __name__ == "__main__":
    path_to_folder = input("Введите путь к папке: ").strip()
    if os.path.isdir(path_to_folder):
        replace_in_c_files(path_to_folder)
    else:
        print("❌ Указанный путь не существует или не является папкой.")
