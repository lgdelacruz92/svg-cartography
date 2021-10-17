import sys
import json

if __name__ == '__main__':
    filein = sys.argv[1]

    with open(filein, 'r') as in_file:
        max_num = -100000
        min_num = 100000
        for line in in_file:
            file_line = json.loads(line)
            num = float(file_line['properties']['percentage'])
            if num > max_num:
                max_num = num
            if num < min_num:
                min_num = num
        print(max_num, min_num)

