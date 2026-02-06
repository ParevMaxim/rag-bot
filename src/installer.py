import os
import sys
import shutil
import urllib.request
import subprocess
from pathlib import Path
from textwrap import dedent

INSTALL_DIR = Path(r"C:\RAGChat")
OLLAMA_URL = "https://ollama.com/download/OllamaSetup.exe"
OLLAMA_SETUP_NAME = "OllamaSetup.exe"
README_NAME = "README_Ollama.txt"


def ensure_install_dir():
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)


def copy_self():
    """
    Копируем текущий exe в папку установки как RAGChat.exe
    (если уже копия лежит там — не трогаем).
    """
    exe_path = Path(sys.executable)
    target_exe = INSTALL_DIR / "RAGChat.exe"
    if not target_exe.exists():
        try:
            shutil.copy(exe_path, target_exe)
        except Exception as e:
            print(f"Не удалось скопировать exe: {e}")


def download_ollama_setup():
    """
    Скачиваем OllamaSetup.exe в папку установки, если его там ещё нет.
    """
    target = INSTALL_DIR / OLLAMA_SETUP_NAME
    if target.exists():
        return target

    print("Скачиваю OllamaSetup.exe...")
    try:
        urllib.request.urlretrieve(OLLAMA_URL, target)
    except Exception as e:
        print(f"Ошибка загрузки OllamaSetup.exe: {e}")
        return None
    return target


def write_readme():
    """
    Пишем файл-инструкцию с дальнейшими шагами.
    """
    readme_path = INSTALL_DIR / README_NAME
    text = dedent(
        f"""
        RAG Chat — локальный помощник по документации.

        1. Установите Ollama, запустив файл:
           {OLLAMA_SETUP_NAME}
           (он находится в этой же папке: {INSTALL_DIR})

           Официальная страница загрузки:
           {OLLAMA_URL}

        2. После установки Ollama откройте терминал (PowerShell) и, при необходимости,
           скачайте модели (если ваше приложение не делает это автоматически):

             ollama pull llama3.1
             ollama pull nomic-embed-text

        3. Запустите RAG Chat:
             {INSTALL_DIR / "RAGChat.exe"}

           Приложение позволит загрузить вашу документацию и задавать вопросы по ней.
        """
    ).strip()
    readme_path.write_text(text, encoding="utf-8")


def run_ollama_setup(setup_path: Path):
    """
    Запускаем официальный установщик Ollama.
    Пользователь проходит мастера установки.
    """
    try:
        subprocess.Popen([str(setup_path)])
    except Exception as e:
        print(f"Не удалось запустить OllamaSetup.exe: {e}")


def main():
    print("Установка RAG Chat...")

    ensure_install_dir()
    copy_self()
    write_readme()

    setup_path = download_ollama_setup()
    if setup_path is None:
        print("Не удалось скачать OllamaSetup.exe. Смотрите README_Ollama.txt для дальнейших шагов.")
        input("Нажмите Enter для выхода...")
        return

    print(f"OllamaSetup.exe сохранён в: {setup_path}")
    print("Сейчас будет запущен официальный установщик Ollama.")
    print("После завершения установки запустите RAGChat.exe из папки C:\\RAGChat.")
    run_ollama_setup(setup_path)

    input("Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()