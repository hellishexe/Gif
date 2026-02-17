#!/usr/bin/env python3
import subprocess
import sys
import os

# Запускаем GUI без консольного окна
if __name__ == "__main__":
    # Получаем путь к текущей директории
    current_dir = os.path.dirname(os.path.abspath(__file__))
    gui_script = os.path.join(current_dir, "gif_converter_gui.py")
    
    # Запускаем GUI скрипт
    subprocess.Popen([sys.executable, gui_script], 
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)