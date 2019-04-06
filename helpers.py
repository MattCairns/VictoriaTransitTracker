import csv

def read_trips(file_name, static = False):
    d = {}
    with open(file_name, encoding='utf8') as tsvin:
        reader = csv.reader(tsvin, delimiter = ',')
        for row in reader:
            if static:
                d[row[4]] = row
            else:
                d[row[2]] = row
    return d

def read_routes(file_name, static = False):
    d = {}
    with open(file_name, encoding='utf8') as tsvin:
        reader = csv.reader(tsvin, delimiter = ',')
        for row in reader:
            if static:
                d[row[1]] = row
            else:
                d[row[0]] = row
    return d

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


def main():
    shapes = read_shapes('data/shapes.txt')


if __name__ == '__main__':
    main()
