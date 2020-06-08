import os
import csv
from prepare_avg_marks_datasets import fulfill_frame
from new_transform_from_EIS import all_groups


def merge_english_marks(groups):
    frame = dict()
    mapping = {'F': 0, 'E': 1, 'D': 2, 'C': 3, 'B': 4, 'A': 5}
    for group in groups:
        for i in range(4):
            check_file = os.path.exists(f'new_svod/SvodSession_{group}_{i+1}.csv')
            if check_file:
                file = open(f'new_svod/SvodSession_{group}_{i+1}.csv', 'r')
                for _ in range(5): # deleting 4 first not necessary strings
                    file.readline()
                reader = csv.reader(file, delimiter=',')  # read CSV
                for line in reader:
                    if len(line) > 0 and ('Иностранный язык' in line[-4] or \
                         'Основы профессиональной коммуникации' in line[-4]):
                        family = line[2].split('\n')[0].strip()
                        if family not in frame:
                            frame[family] = list()
                        if len(frame[family]) > 0 and frame[family][-1][0] == i + 1:
                            line[-1] = 'F' if line[-1] == '' else line[-1]
                            frame[family][-1] = (i + 1, mapping[line[-1]])
                        else:
                            line[-1] = 'F' if line[-1] == '' else line[-1]
                            frame[family].append((i + 1, mapping[line[-1]]))
                file.close()
    return frame



if __name__ == '__main__':
    # groups = ['Б14-503', 'Б14-504', 'Б15-502', 'Б16-503', 'Б16-513']
    groups = all_groups()
    j1 = merge_english_marks(groups)
    j2 = fulfill_frame(j1, 0)
    print(j2)