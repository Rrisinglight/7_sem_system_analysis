import sys
import csv

def get_csv_cell_value(file_path, row_index, column_index):
    """
    Вам дан файл в формате csv (например, такой csv или json), в котором записана таблица из n строк и m столбцов, содержащая числа (допустим, с плавающей точкой).
    
    Необходимо написать программу, которая 
    при запуске принимает в качестве параметров (аргументов): полный путь к csv-файлу, номер строки, номер колонки
    возвращает (в консоль) значение ячейки, находящейся на пересечении заданной строки и столбца.
    """
    try:
        row_index = int(row_index) - 1
        column_index = int(column_index) - 1
        
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            
            rows = list(csv_reader)
            row = rows[row_index]
            
            if row_index < 0 or row_index >= len(rows):
                raise IndexError(f"Слишком большой или маленький номер стоки, в файле {len(rows)} строк.")
            if column_index < 0 or column_index >= len(row):
                raise IndexError(f"Слишком большой или маленький номер столбца, в файле {len(row)} столбцов.")
            
            return row[column_index]
    
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)
        

def main():
    if len(sys.argv) != 4:
        print("Принимает три аргумента: <путь к csv-файлу> <номер строки> <номер колонки>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    row_number = sys.argv[2]
    column_number = sys.argv[3]
    
    cell_value = get_csv_cell_value(file_path, row_number, column_number)
    print(cell_value)

if __name__ == "__main__":
    main()