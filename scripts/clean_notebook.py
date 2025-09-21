#!/usr/bin/env python3
"""
Скрипт для очистки notebook от jetTransient метаданных,
которые мешают экспорту в HTML.

Использование:
    python scripts/clean_notebook.py path/to/notebook.ipynb
"""
import json
import sys
import os

def clean_notebook(notebook_path):
    """Очищает notebook от jetTransient метаданных"""

    if not os.path.exists(notebook_path):
        print(f"❌ Файл не найден: {notebook_path}")
        return False

    # Читаем notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Счетчик очищенных элементов
    cleaned_count = 0

    # Проходим по всем ячейкам
    for cell in notebook.get('cells', []):
        # Проверяем outputs
        for output in cell.get('outputs', []):
            if 'jetTransient' in output:
                del output['jetTransient']
                cleaned_count += 1

        # Проверяем metadata ячейки
        if 'jetTransient' in cell.get('metadata', {}):
            del cell['metadata']['jetTransient']
            cleaned_count += 1

    # Проверяем общие metadata notebook
    if 'jetTransient' in notebook.get('metadata', {}):
        del notebook['metadata']['jetTransient']
        cleaned_count += 1

    # Записываем очищенный notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)

    print(f"✓ Очищено {cleaned_count} jetTransient элементов")
    print(f"✓ Notebook сохранен: {notebook_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python clean_notebook.py path/to/notebook.ipynb")
        print("Пример: python scripts/clean_notebook.py practical_work_3/practical_work_3.ipynb")
        sys.exit(1)

    notebook_file = sys.argv[1]

    print("Очистка notebook от jetTransient метаданных...")
    if clean_notebook(notebook_file):
        print("✅ Готово! Теперь можно экспортировать в HTML.")
    else:
        print("❌ Ошибка при обработке файла.")
        sys.exit(1)