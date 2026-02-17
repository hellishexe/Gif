#!/usr/bin/env python3
"""
Программа для конвертации изображений (GIF, JPEG, PNG, BMP и др.) в черно-белый с оттенками серого
"""

import os
import sys
from PIL import Image, ImageSequence
import argparse

def convert_image_to_grayscale(input_path, output_path=None, make_grayscale=True, flip_horizontal=False):
    """
    Обрабатывает изображение: конвертация в черно-белый и/или отзеркаливание
    Поддерживает: GIF (анимированные), JPEG, PNG, BMP, TIFF и другие
    
    Args:
        input_path (str): Путь к исходному файлу изображения
        output_path (str): Путь для сохранения (опционально)
        make_grayscale (bool): Конвертировать в черно-белый
        flip_horizontal (bool): Отзеркалить горизонтально
    """
    try:
        # Открываем изображение
        with Image.open(input_path) as img:
            # Получаем информацию о файле
            original_format = img.format
            print(f"Обрабатываем {original_format} файл: {os.path.basename(input_path)}")
            
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
                print("Обрабатываем анимированный GIF...")
                processed_frames = []
                
                # Обрабатываем каждый кадр
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
                
                # Сохраняем как анимированный GIF
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
                    print("Ошибка: Не удалось обработать кадры GIF")
                    return False
            
            # Обрабатываем обычные изображения
            else:
                print("Обрабатываем статичное изображение...")
                
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
            
            operations = []
            if make_grayscale:
                operations.append("черно-белый")
            if flip_horizontal:
                operations.append("отзеркалено")
            
            print(f"✅ Успешно обработано ({', '.join(operations)}): {output_path}")
            return True
                
    except Exception as e:
        print(f"Ошибка при обработке {input_path}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Обработка изображений: черно-белый и отзеркаливание')
    parser.add_argument('input', help='Путь к файлу изображения (GIF, JPEG, PNG, BMP и др.)')
    parser.add_argument('-o', '--output', help='Путь для сохранения результата')
    parser.add_argument('-g', '--grayscale', action='store_true', default=True,
                       help='Конвертировать в черно-белый (по умолчанию включено)')
    parser.add_argument('--no-grayscale', action='store_true',
                       help='Не конвертировать в черно-белый')
    parser.add_argument('-f', '--flip', action='store_true',
                       help='Отзеркалить горизонтально')
    
    args = parser.parse_args()
    
    # Проверяем существование файла
    if not os.path.exists(args.input):
        print(f"Ошибка: Файл {args.input} не найден")
        sys.exit(1)
    
    # Определяем опции
    make_grayscale = args.grayscale and not args.no_grayscale
    flip_horizontal = args.flip
    
    if not make_grayscale and not flip_horizontal:
        print("Ошибка: Выберите хотя бы одну опцию обработки (--grayscale или --flip)")
        sys.exit(1)
    
    # Конвертируем
    success = convert_image_to_grayscale(args.input, args.output, make_grayscale, flip_horizontal)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()