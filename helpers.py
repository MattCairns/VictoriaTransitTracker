import csv

# Read our static bus data files 
def read_static_data(file_name, index = 0):
    d = {}
    with open(file_name, encoding='utf8') as tsvin:
        reader = csv.reader(tsvin, delimiter = ',')
        for row in reader:
            d[row[index]] = row
    return d

# Read the path shapes for our bus routes.
def read_shapes(file_name):
    d = {}
    with open(file_name, encoding='utf8') as tsvin:
        reader = csv.reader(tsvin, delimiter = ',')
        for row in reader:
            if row[0] == 'shape_id':
                continue
            if row[0] not in d:
                d[row[0]] = [(float(row[1]), float(row[2]))]
            else:
                d[row[0]].append((float(row[1]), float(row[2])))
    return d

# Test
def main():
    shapes = read_shapes('data/shapes.txt')


if __name__ == '__main__':
    main()
