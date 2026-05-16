import csv

def save_csv(filename, rows):
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

def load_csv(filename):
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)

def count_csv_rows(filename):
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)
    return len(data)

def sum_column(filename, col_index):
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)

    total = 0
    for row in data[1:]:
        total += int(row[col_index])
    return total

def average_column(filename, col_index):
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)

    total = 0
    count = 0
    for row in data[1:]:
        total += float(row[col_index])
        count += 1
    
    if count == 0:
        return 0
    return total / count
