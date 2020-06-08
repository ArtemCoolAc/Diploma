import os
import json
from new_transform_from_EIS import all_groups

def merge_average_marks(groups, terms=6):
    frame = dict()
    for group in groups:
        for i in range(terms):
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


def fulfill_frame(frame, append_correct=0., terms=6):
    corrected_frame = dict()
    for key, value in frame.items():
        corrected_frame[key] = list()
        if value[-1][0] == terms and len(value) != terms:
            for i in range(terms - len(value)):
                corrected_frame[key].append(append_correct)
            for i in range(len(value)):
                corrected_frame[key].append(value[i][1])
        elif len(value) == terms:
            for i in range(terms):
                corrected_frame[key].append(value[i][1])
    true_frame = extract_unneccessary_data(corrected_frame, terms)
    return true_frame

def extract_unneccessary_data(frame, terms=6):
    return {k: v for k, v in frame.items() if len(v) == terms}


if __name__ == '__main__':
    groups = all_groups()
    j1 = merge_average_marks(groups)
    j2 = fulfill_frame(j1)