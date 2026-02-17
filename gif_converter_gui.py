#!/usr/bin/env python3
"""
GUI версия конвертера изображений в черно-белый
Поддерживает: GIF, JPEG, PNG, BMP, TIFF и другие форматы
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from PIL import Image, ImageSequence, ImageTk
import threading

class ImageConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер Изображений в Черно-белый")
        self.root.geometry("500x400")
        
        # Переменные
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.make_grayscale = tk.BooleanVar(value=True)
        self.flip_horizontal = tk.BooleanVar(value=False)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Конвертер Изображений в Черно-белый", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Рамка для выбора файла
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(input_frame, text="Выберите изображение:").pack(anchor="w")
        
        file_frame = tk.Frame(input_frame)
        file_frame.pack(fill="x", pady=5)
        
        tk.Entry(file_frame, textvariable=self.input_file, state="readonly").pack(side="left", fill="x", expand=True)
        tk.Button(file_frame, text="Обзор...", command=self.select_input_file).pack(side="right", padx=(5, 0))
        
        # Рамка для выходного файла
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(output_frame, text="Сохранить как (опционально):").pack(anchor="w")
        
        output_file_frame = tk.Frame(output_frame)
        output_file_frame.pack(fill="x", pady=5)
        
        tk.Entry(output_file_frame, textvariable=self.output_file).pack(side="left", fill="x", expand=True)
        tk.Button(output_file_frame, text="Обзор...", command=self.select_output_file).pack(side="right", padx=(5, 0))
        
        # Опции обработки
        options_frame = tk.Frame(self.root)
        options_frame.pack(pady=15, padx=20, fill="x")
        
        tk.Label(options_frame, text="Опции обработки:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        options_checkboxes = tk.Frame(options_frame)
        options_checkboxes.pack(fill="x", pady=5)
        
        tk.Checkbutton(options_checkboxes, text="Сделать черно-белым", 
                      variable=self.make_grayscale).pack(anchor="w")
        tk.Checkbutton(options_checkboxes, text="Отзеркалить горизонтально", 
                      variable=self.flip_horizontal).pack(anchor="w")
        
        # Кнопка конвертации
        self.convert_button = tk.Button(self.root, text="Конвертировать", 
                                       command=self.convert_gif, bg="#4CAF50", fg="white",
                                       font=("Arial", 12, "bold"))
        self.convert_button.pack(pady=20)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(pady=10, padx=20, fill="x")
        
        # Статус
        self.status_label = tk.Label(self.root, text="Готов к работе", fg="green")
        self.status_label.pack(pady=5)
        
        # Информация
        info_text = "Поддерживаемые форматы: GIF, JPEG, PNG, BMP, TIFF\nВыберите нужные опции обработки"
        tk.Label(self.root, text=info_text, fg="gray", justify="center").pack(pady=10)
    
    def select_input_file(self):
        filename = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Все изображения", "*.gif *.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("GIF files", "*.gif"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("BMP files", "*.bmp"),
                ("TIFF files", "*.tiff *.tif"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)
            # Автоматически предлагаем имя выходного файла
            name, ext = os.path.splitext(filename)
            suffix = ""
            if self.make_grayscale.get():
                suffix += "_grayscale"
            if self.flip_horizontal.get():
                suffix += "_flipped"
            if not suffix:
                suffix = "_processed"
            self.output_file.set(f"{name}{suffix}{ext}")
    
    def select_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Сохранить как",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("GIF files", "*.gif"),
                ("BMP files", "*.bmp"),
                ("TIFF files", "*.tiff"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_file.set(filename)
    
    def convert_gif(self):
        if not self.input_file.get():
            messagebox.showerror("Ошибка", "Пожалуйста, выберите файл изображения")
            return
        
        if not self.make_grayscale.get() and not self.flip_horizontal.get():
            messagebox.showerror("Ошибка", "Выберите хотя бы одну опцию обработки")
            return
        
        # Запускаем конвертацию в отдельном потоке
        self.convert_button.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="Конвертация...", fg="orange")
        
        thread = threading.Thread(target=self.do_conversion)
        thread.daemon = True
        thread.start()
    
    def do_conversion(self):
        try:
            input_path = self.input_file.get()
            output_path = self.output_file.get() if self.output_file.get() else None
            
            # Конвертируем
            success = self.process_image(input_path, output_path, 
                                       self.make_grayscale.get(), 
                                       self.flip_horizontal.get())
            
            # Обновляем UI в главном потоке
            self.root.after(0, self.conversion_complete, success)
            
        except Exception as e:
            self.root.after(0, self.conversion_error, str(e))
    
    def process_image(self, input_path, output_path=None, make_grayscale=True, flip_horizontal=False):
        try:
            with Image.open(input_path) as img:
                original_format = img.format
                
                # Определяем путь для сохранения
                if output_path is None:
                    name, ext = os.path.splitext(input_path)
                    suffix = ""
                    if make_grayscale:
                        suffix += "_grayscale"
                    if flip_horizontal:
                        suffix += "_flipped"
                    if not suffix:
                        suffix = "_processed"
                    output_path = f"{name}{suffix}{ext}"
                
                # Обрабатываем анимированные GIF
                if original_format == 'GIF' and getattr(img, 'is_animated', False):
                    processed_frames = []
                    
                    for frame in ImageSequence.Iterator(img):
                        # Конвертируем в RGB если нужно
                        if frame.mode != 'RGB':
                            frame = frame.convert('RGB')
                        
                        # Применяем обработку
                        processed_frame = frame
                        
                        # Отзеркаливание
                        if flip_horizontal:
                            processed_frame = processed_frame.transpose(Image.FLIP_LEFT_RIGHT)
                        
                        # Конвертация в градации серого
                        if make_grayscale:
                            processed_frame = processed_frame.convert('L')
                        
                        processed_frames.append(processed_frame)
                    
                    if processed_frames:
                        processed_frames[0].save(
                            output_path,
                            save_all=True,
                            append_images=processed_frames[1:],
                            duration=img.info.get('duration', 100),
                            loop=img.info.get('loop', 0),
                            format='GIF'
                        )
                    else:
                        return False
                
                # Обрабатываем обычные изображения
                else:
                    # Конвертируем в RGB если нужно (для PNG с прозрачностью и др.)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Создаем белый фон для изображений с прозрачностью
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Применяем обработку
                    processed_img = img
                    
                    # Отзеркаливание
                    if flip_horizontal:
                        processed_img = processed_img.transpose(Image.FLIP_LEFT_RIGHT)
                    
                    # Конвертация в градации серого
                    if make_grayscale:
                        processed_img = processed_img.convert('L')
                    
                    # Определяем формат для сохранения
                    save_format = original_format
                    if save_format not in ['JPEG', 'PNG', 'BMP', 'TIFF', 'GIF']:
                        save_format = 'PNG'  # По умолчанию PNG для неизвестных форматов
                    
                    # Сохраняем
                    if save_format == 'JPEG':
                        processed_img.save(output_path, format=save_format, quality=95)
                    else:
                        processed_img.save(output_path, format=save_format)
                
                self.output_path = output_path
                return True
                
        except Exception as e:
            raise e
    
    def conversion_complete(self, success):
        self.progress.stop()
        self.convert_button.config(state="normal")
        
        if success:
            self.status_label.config(text=f"Готово! Сохранено: {os.path.basename(self.output_path)}", fg="green")
            messagebox.showinfo("Успех", f"Изображение успешно конвертировано!\nСохранено: {self.output_path}")
        else:
            self.status_label.config(text="Ошибка конвертации", fg="red")
            messagebox.showerror("Ошибка", "Не удалось конвертировать изображение")
    
    def conversion_error(self, error_msg):
        self.progress.stop()
        self.convert_button.config(state="normal")
        self.status_label.config(text="Ошибка", fg="red")
        messagebox.showerror("Ошибка", f"Ошибка при конвертации:\n{error_msg}")

def main():
    root = tk.Tk()
    app = ImageConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()