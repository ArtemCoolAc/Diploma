import os
import json


def merge_average_marks(groups):
    frame = dict()
    for group in groups:
        for i in range(6):
            check_file = os.path.exists(f'jsons/Grades_json{group}_{i+1}.json')
            if check_file:
                file = open(f'jsons/Grades_json{group}_{i+1}.json')
                j = json.load(file)
                for key, value in j.items():
                    if key not in frame:
                        frame[key] = list()
                    if len(frame[key]) > 0 and frame[key][-1][0] == i + 1:
                        frame[key][-1] = (i + 1, value['average'])
                    else:
                        frame[key].append((i + 1, value['average']))
                file.close()
    return frame


def fulfill_frame(frame, append_correct=0.):
    corrected_frame = dict()
    for key, value in frame.items():
        corrected_frame[key] = list()
        if value[-1][0] == 6 and len(value) != 6:
            for i in range(6 - len(value)):
                corrected_frame[key].append(append_correct)
            for i in range(len(value)):
                corrected_frame[key].append(value[i][1])
        elif len(value) == 6:
            for i in range(6):
                corrected_frame[key].append(value[i][1])
    true_frame = extract_unneccessary_data(corrected_frame)
    return true_frame

def extract_unneccessary_data(frame):
    return {k: v for k, v in frame.items() if len(v) == 6}


if __name__ == '__main__':
    j1 = merge_average_marks(['Б14-503', 'Б14-504', 'Б15-502', 'Б16-503', 'Б16-513'])
    j2 = fulfill_frame(j1)