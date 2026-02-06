import PyInstaller.__main__
import os

# Название выходного файла
APP_NAME = "RAGChat_Assistant"

# Основной файл запуска
ENTRY_POINT = "app_qt.py"

# Команда для PyInstaller
params = [
    ENTRY_POINT,
    '--name=' + APP_NAME,
    '--noconfirm',
    '--onefile',       # Собираем в ОДИН файл .exe
    '--windowed',      # Без консольного черного окна
    '--clean',
    
    # Добавляем пути к модулям (если они в папке rag)
    '--add-data=rag;rag',
    
    # Скрытые импорты, которые PyInstaller может потерять
    '--hidden-import=rank_bm25',
    '--hidden-import=ollama',
    '--hidden-import=pypdf',
    '--hidden-import=bs4',
    '--hidden-import=numpy',
    
    # Иконка (если есть, раскомментируй и положи icon.ico рядом)
    # '--icon=icon.ico',
]

print("Начинаю сборку EXE...")
PyInstaller.__main__.run(params)
print(f"Сборка завершена! Ищите файл в папке dist/{APP_NAME}.exe")